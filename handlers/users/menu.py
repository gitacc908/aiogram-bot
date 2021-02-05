from aiogram import types
from aiogram.contrib.middlewares import logging
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove, CallbackQuery

from keyboards.default import menu
from keyboards.inline.inline_buttons import choice
from loader import dp


@dp.message_handler(Command('items'))
async def show_menu(message: types.Message):
    await message.answer('Выберите варианты', reply_markup=choice)


@dp.message_handler(Command('menu'))
async def show_menu(message: types.Message):
    await message.answer('Выберите варианты ниже', reply_markup=menu)


@dp.message_handler(text='Предложение')
async def get_offer(message: types.Message):
    await message.answer('Напишите свое предложение', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(text='Пожаловаться')
async def get_complains(message: types.Message):
    await message.answer('Напишите свою жалобу', reply_markup=ReplyKeyboardRemove())


@dp.callback_query_handler(text_contains='Offer')
async def get_inline_offer(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=5)
    logging.info(f'callback data dict = {callback_data}')
    await call.message.answer('Вы можете написать свое предложение')
