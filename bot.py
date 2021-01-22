import logging
import os
import config
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from filters import Button

logging.basicConfig(level=logging.INFO)
bot = Bot(token=os.environ['TELEGRAM_TOKEN'])
dp = Dispatcher(bot, storage=MemoryStorage())


class Step(StatesGroup):
    start = State()
    started = State()
    expecting_anonymize = State()
    expecting_feedback = State()
    answering_feedback = State()


@dp.message_handler(commands=['start'])
async def cmd_start(msg: types.Message):
    markup = types.InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row(
        types.InlineKeyboardButton(config.button_chat, callback_data='anochat'),
        types.InlineKeyboardButton(config.button_flood, callback_data='anoflood'),
        # types.InlineKeyboardButton(config.button_feedback, callback_data='feedback')
    )
    if msg.from_user.id in config.admins_id:
        message = config.start_admin.format(msg.from_user.first_name)
    else:
        message = config.start.format(msg.from_user.first_name)
    await bot.send_message(msg.from_user.id, message, reply_markup=markup)
    await Step.started.set()


@dp.message_handler(state=Step.answering_feedback)
async def process_msg_feedback(msg: types.Message, state: FSMContext):
    for id in config.admins_id:
        await bot.forward_message(id, msg.from_user.id, msg.message_id)
    await bot.send_message(msg.from_user.id, config.reply, reply_to_message_id=msg.message_id)
    await Step.started.set()


@dp.callback_query_handler(Button('anochat'), state=Step.started)
async def process_btn_chat(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(chosen=config.chat_id)
    chat_id = callback_query.from_user.id
    await bot.send_message(chat_id, config.enter)
    await Step.expecting_anonymize.set()


@dp.callback_query_handler(Button('anoflood'), state=Step.started)
async def process_btn_flood(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(chosen=config.flood_id)
    chat_id = callback_query.from_user.id
    await bot.send_message(chat_id, config.enter)
    await Step.expecting_anonymize.set()


@dp.message_handler(state=Step.expecting_anonymize)
async def process_msg_anonymize(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    chat_id = data['chosen']
    await bot.send_message(chat_id, msg.text)
    await Step.started.set()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
