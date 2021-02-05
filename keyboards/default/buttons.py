from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(

    keyboard = [
        [
            KeyboardButton(text='Предложение')
        ],
        [
            KeyboardButton(text='Пожаловаться')
        ]
    ],
    resize_keyboard=True
)