import os
import config
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

bot = Bot(token=os.environ['TELEGRAM_TOKEN'])
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler()
async def process_msg_anonymize(msg: types.Message):
    await bot.send_message(config.chat_id, msg.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
