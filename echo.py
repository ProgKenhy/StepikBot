from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, ContentType
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}! Это бот для отправки сообщений."
    )

@dp.message(Command(commands=["help"]))
async def process_help_command(message: Message):
    await message.answer(
        "Напиши мне что-нибудь и в ответ " 
        "я пришлю тебе твое сообщение"
    )

async def send_echo(message: Message):
    await message.answer(message.text)

async def send_content_echo(message: Message, content_type: str):
    if content_type == "photo":
        file_id = getattr(message, content_type)[0].file_id
    else:
        file_id = getattr(message, content_type).file_id
    send_function = getattr(message, f"reply_{content_type}")
    await send_function(file_id)


def create_content_handlers(content_type):
    async def handler(message: Message):
        await send_content_echo(message, content_type)
    return handler
    



CONTENT_HANDLERS = {
    "photo": F.photo,
    "document": F.document,
    "audio": F.audio,
    "video": F.video,
    "sticker": F.sticker,
}

for content_type, filter_ in CONTENT_HANDLERS.items():
    dp.message.register(create_content_handlers(content_type), filter_)

dp.message.register(send_echo) 

if __name__ == '__main__':
    dp.run_polling(bot)
