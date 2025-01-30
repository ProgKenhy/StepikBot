from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

buttons: list[list[KeyboardButton]] = [[KeyboardButton(
    text=f'Button {j * 3 + i}') for i in range(1, 4)] for j in range(3)]

keyboard = ReplyKeyboardMarkup(keyboard=buttons, one_time_keyboard=True, resize_keyboard=True)


@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text='Чего кошки боятся больше?',
        reply_markup=keyboard
    )


@dp.message(F.text == 'Dogs')
async def process_dog_answer(message: Message):
    await message.answer(
        text='Да, несомненно, кошки боятся собак. '
             'Но вы видели как они боятся огурцов?',
    )


@dp.message(F.text == 'cucumbers')
async def process_cucumber_answer(message: Message):
    await message.answer(
        text='Да, иногда кажется, что огурцов '
             'кошки боятся больше',
    )


if __name__ == '__main__':
    dp.run_polling(bot)
