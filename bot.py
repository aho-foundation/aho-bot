import config
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

bot = Bot(token=config.token)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler()
async def process_msg_anonymize(msg: types.Message):
    if(not msg.reply_to_message and not msg.text.startswith('/start')):
        await bot.send_message(config.chat_id, msg.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
