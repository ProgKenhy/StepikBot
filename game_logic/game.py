def game_result(user_choice: str, bot_choice: str) -> bool | None:
    user_choice = user_choice.lower()
    bot_choice = bot_choice.lower()

    variants = {
        'ножницы': {'бумага': False, 'камень': True},
        'бумага': {'камень': False, 'ножницы': True},
        'камень': {'ножницы': False, 'бумага': True},
    }

    if user_choice == bot_choice:
        return None

    return variants[bot_choice][user_choice]