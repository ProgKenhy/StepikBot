from random import randint

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import ReplyKeyboardMarkup, CallbackQuery, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, Message
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# Reply Keyboard
reply_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/start")],
        [KeyboardButton(text="/help"), KeyboardButton(text="/stat")],
        [KeyboardButton(text="/letsGO"), KeyboardButton(text="/cancel")],
    ],
    resize_keyboard=True
)

# Inline Keyboard
inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Начать игру', callback_data='start')]
    ]
)


ATTEMPTS = 7

user = {
    'in_game': False,
    'secret_number': 0,
    'attempts': 0,
    'total_games': 0,
    'wins': 0
}


def get_random_number() -> int:
    return randint(1, 100)


@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        'Привет!\nДавайте сыграем в игру "Угадай число"?\n\n'
        'Чтобы получить правила игры и список доступных '
        'команд - отправьте команду /help',
        reply_markup=reply_keyboard
    )


@dp.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer(
        'Правила игры:\n\nЯ загадываю число от 1 до 100, '
        f'а вам нужно его угадать\nУ вас есть {ATTEMPTS} '
        'попыток\n\nДоступные команды:\n/help - правила '
        'игры и список команд\n/cancel - выйти из игры\n'
        '/stat - посмотреть статистику\n\nДавай сыграем?\n'
        '/letsGO - начать!',
        reply_markup=inline_keyboard
    )


@dp.message(Command(commands='stat'))
async def process_stat_command(message: Message):
    stats_message = (
        f'Игровые статистики:\n'
        f'Всего игр: {user["total_games"]}\n'
        f'Победы: {user["wins"]}\n'
    )
    if user["total_games"] != 0:
        stats_message += f'Процент побед: {round((user["wins"] / user["total_games"]) * 100, 2)}%\n'
    else:
        stats_message += 'Процент побед: Невозможно вычислить (нет игр)\n'

    await message.answer(stats_message)


@dp.message(Command(commands='cancel'))
async def process_cancel_command(message: Message):
    if user['in_game']:
        user['in_game'] = False
        await message.answer(
            'Вы вышли из игры. Если захотите сыграть '
            'снова - напишите об этом'
        )
    else:
        await message.answer(
            'А мы и так с вами не играем. '
            'Может, сыграем разок?'
        )


@dp.message(Command(commands='letsGO'))
async def process_positive_answer(message: Message):
    if not user['in_game']:
        user['in_game'] = True
        user['secret_number'] = get_random_number()
        user['attempts'] = ATTEMPTS
        user['total_games'] += 1
        await message.answer(
            'Ура!\n\nЯ загадал число от 1 до 100, '
            'попробуй угадать!'
        )
    else:
        await message.answer(
            'Пока мы играем в игру я могу '
            'реагировать только на числа от 1 до 100 '
            'и команды /cancel и /stat'
        )


@dp.message(F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду']))
async def process_negative_answer(message: Message):
    if not user['in_game']:
        await message.answer(
            'Жаль :(\n\nЕсли захотите поиграть - просто '
            'напишите об этом'
        )
    else:
        await message.answer(
            'Мы же сейчас с вами играем. Присылайте, '
            'пожалуйста, числа от 1 до 100'
        )


@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_number_answer(message: Message):
    if user['in_game']:
        if int(message.text) == user['secret_number']:
            user['in_game'] = False
            user['total_games'] += 1
            user['wins'] += 1
            await message.answer(
                'Ура!!! Вы угадали число!\n\n'
                'Может, сыграем еще?'
            )
        elif int(message.text) > user['secret_number']:
            user['attempts'] -= 1
            await message.answer(f"Моё число меньше\nЧисло попыток: {user['attempts']}")
        elif int(message.text) < user['secret_number']:
            user['attempts'] -= 1
            await message.answer(f"Моё число больше\nЧисло попыток: {user['attempts']}")

        if user['attempts'] == 0:
            user['in_game'] = False
            user['total_games'] += 1
            await message.answer(
                'К сожалению, у вас больше не осталось '
                'попыток. Вы проиграли :(\n\nМое число '
                f'было {user["secret_number"]}\n\nДавайте '
                'сыграем еще?\n/letsGO - начать!'
            )
    elif not user['in_game']:
        await message.answer(f'Мы ещё не играем. Хотите сыграть?\n'
                             f'/help - правила игры и список команд\n/letsGO - начать!')

@dp.message()
async def process_other_answer(message: Message):
    if user['in_game']:
        await message.answer(
            'Мы же сейчас с вами играем. '
            'Присылайте, пожалуйста, числа от 1 до 100'
        )
    else:
        await message.answer(
            'Я довольно ограниченный бот, давайте '
            'просто сыграем в игру?\n'
            '/help - правила игры и список команд'
        )


@dp.callback_query(lambda c: c.data.startswith('start'))
async def process_start_callback(callback_query: CallbackQuery):
    if not user['in_game']:
        user['in_game'] = True
        user['secret_number'] = get_random_number()
        user['attempts'] = ATTEMPTS
        user['total_games'] += 1
        await callback_query.message.answer(
            'Ура!\n\nЯ загадал число от 1 до 100, '
            'попробуй угадать!'
        )
    await callback_query.answer()

if __name__ == '__main__':
    dp.run_polling(bot)