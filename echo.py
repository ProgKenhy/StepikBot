from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, BaseFilter
from aiogram.types import Message
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

class NumberInMessage(BaseFilter):
    async def __call__(self, message: Message) -> bool | dict[str, list[int]] :
        numbers = []
        for word in message.text.split():
            normalized_word = word.replace('.','').replace(',', '').strip()
            if normalized_word.isdigit():
                numbers.append(int(normalized_word))
        if numbers:
            return {'numbers': numbers}
        return False


@dp.message(F.text.lower().startwith('найди числа'), NumberInMessage())
async def process_if_numbers(message: Message, numbers: list[int]):
    await message.answer(
        text=f'Нашел: {", ".join(str(num) for num in numbers)}')

@dp.message(F.text.lower().startwith('найди числа'))
async def process_if_not_numbers(message: Message):
    await message.answer(text='Not numbers')

if __name__ == '__main__':
    dp.run_polling(bot)