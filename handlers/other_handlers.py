from aiogram import Router
from aiogram.types import Message
from data.users import get_user
from lexicon.lexicon import LEXICON_RU

router = Router()


@router.message()
async def send_echo(message: Message):
    user = get_user(message.from_user.id)
    if user['in_game']:
        await message.answer(text=LEXICON_RU['incorrect_choice'])
    else:
        await message.answer(text=LEXICON_RU['user_in_game_false'])
