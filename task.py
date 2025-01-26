from aiogram import Bot, Dispatcher, F
import os
from dotenv import load_dotenv
from aiogram.filters import BaseFilter
from aiogram.types import Message

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

admin_ids = [2084948859]

class IsAdmin(BaseFilter):
    def __init__(self, admin_ids: list[int]) -> None:
        self.admin_ids = admin_ids

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids


@dp.message(IsAdmin(admin_ids))
async def is_admin(message: Message):
    await message.answer(text="U admin")

@dp.message()
async def not_admin(message: Message):
    await message.answer(text="U are not admin")
    print(message.from_user.id)

if __name__ == '__main__':
    dp.run_polling(bot)