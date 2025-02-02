from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from game_logic.game import game_result
from lexicon.lexicon import LEXICON_RU
from data.users import save_users, get_user


router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'])


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])


@router.message(Command(commands='play'))
async def process_help_command(message: Message):
    user = get_user(message.from_user.id)
    user['in_game'] = True
    user['total_games'] += 1
    save_users()
    await message.answer(text=LEXICON_RU['/play'])


@router.message(Command(commands='stat'))
async def process_help_command(message: Message):
    user = get_user(message.from_user.id)
    stats_message = (
        f'Игровые статистики:\n'
        f'Всего игр: {user["total_games"]}\n'
        f'Победы: {user["wins"]}\n'
        f'Ничьи: {user["draws"]}\n'
        f'Поражения {user["total_games"] - user["wins"] - user["draws"]}\n'
    )
    if user["total_games"] != 0:
        stats_message += f'Процент побед: {round((user["wins"] / user["total_games"]) * 100, 2)}%\n'
    else:
        stats_message += 'Процент побед: Невозможно вычислить (нет игр)\n'
    await message.answer(stats_message)


@router.message(F.text.lower().in_(['камень', 'ножницы', 'бумага']))
async def process_help_command(message: Message):
    user = get_user(message.from_user.id)
    if not user['in_game']:
        await message.answer(text=LEXICON_RU['user_in_game_false'])
    elif user['in_game']:
        if game_result(message.text):
            user['in_game'] = False
            user['wins'] += 1
            save_users()
            await message.answer(text=LEXICON_RU['win'])
        elif not game_result(message.text):
            user['in_game'] = False
            save_users()
            await message.answer(text=LEXICON_RU['lose'])
        else:
            user['in_game'] = False
            user['draws'] += 1
            save_users()
            await message.answer(text=LEXICON_RU['draw'])
