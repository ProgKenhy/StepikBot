from random import choice

from lexicon.lexicon import LEXICON_RU


def game_result(user_choice: str) -> bool | None:
    user_choice = user_choice.lower()

    variants = {
        'ножницы': {'бумага': True, 'камень': False},
        'бумага': {'камень': True, 'ножницы': False},
        'камень': {'ножницы': True, 'бумага': False},
    }

    bot_choice = choice(list(variants.keys()))

    if user_choice.lower() == bot_choice:
        return None

    return variants[bot_choice][user_choice]
