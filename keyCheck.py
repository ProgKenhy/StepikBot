from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, Message, KeyboardButtonPollType, ReplyKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

kb_builder = ReplyKeyboardBuilder()

contact_btn = KeyboardButton(
    text='Send phone number',
    request_contact=True
)

geo_btn = KeyboardButton(
    text='Send geolocation',
    request_location=True
)

poll_btn = KeyboardButton(
    text='Send poll',
    request_poll=KeyboardButtonPollType()
)

web_app_btn = KeyboardButton(
    text='Start web app',
    web_app=WebAppInfo(url="https://stepik.org/")
)

kb_builder.row(contact_btn, geo_btn, poll_btn, web_app_btn, width=1)

keyboard: ReplyKeyboardMarkup = kb_builder.as_markup(
    resize_keyboard=True,
    one_time_keyboard=True
)


@dp.message(CommandStart())
async def command_start(message: Message):
    await message.answer("experiment",
                         reply_markup=keyboard)


if __name__ == '__main__':
    dp.run_polling(bot)
