import json

USERS_FILE = "users.json"

try:
    with open(USERS_FILE, 'r') as file:
        users = json.load(file)
except FileNotFoundError:
    users = {}


def save_users() -> None:
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)


def get_user(user_id: int):
    user_id = str(user_id)  # Преобразование в строку для корректной работы JSON
    if user_id not in users:
        users[user_id] = {
            'in_game': False,
            'total_games': 0,
            'wins': 0,
            'draws': 0,
        }
        save_users()
    return users[user_id]
