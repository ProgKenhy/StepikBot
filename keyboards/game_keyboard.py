from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

btm_scissors = KeyboardButton(text="ножницы")
btm_stone = KeyboardButton(text="камень")
btm_paper = KeyboardButton(text="бумага")

keyboard = ReplyKeyboardMarkup(keyboard=[[btm_paper, btm_stone, btm_scissors]], resize_keyboard=True,
                               one_time_keyboard=True)
