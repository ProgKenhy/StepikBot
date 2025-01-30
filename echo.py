import os
from aiogram import Bot, Dispatcher
from aiogram.filters import BaseFilter
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


class NumberInMessage(BaseFilter):
    async def __call__(self, message: Message) -> bool | dict[str, list[int]]:
        numbers = []
        for word in message.text.split():
            normalized_word = word.strip(',.')
            if normalized_word.isdigit():
                numbers.append(int(normalized_word))
        if numbers:
            return {'numbers': numbers}
        return False


@dp.message(NumberInMessage())
async def process_if_numbers(message: Message, numbers: list[int]):
    if message.text.lower().startswith('найди числа'):
        await message.answer(
            text=f'Нашел: {", ".join(str(num) for num in numbers)}'
        )


@dp.message()
async def process_if_not_numbers(message: Message):
    if message.text.lower().startswith('найди числа'):
        await message.answer(text='Не нашел чисел')


if __name__ == '__main__':
    dp.run_polling(bot)
