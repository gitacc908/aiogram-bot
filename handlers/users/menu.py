from asyncio import sleep
from unittest.mock import call

from aiogram import types
from aiogram.contrib.middlewares import logging
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, state
from aiogram.types import ReplyKeyboardRemove, CallbackQuery, User

from data.config import ADMINS

from keyboards.default import menu
from keyboards.inline.inline_buttons import choice
from loader import dp, bot

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from states.states import Mailing, Review

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)

sheet = client.open("tutorial").sheet1  # Open the spreadhseet


# data = sheet.get_all_records()  # Get a list of all records
# row = sheet.row_values(3)  # Get a specific row
# col = sheet.col_values(3)  # Get a specific column
# cell = sheet.cell(1,2).value  # Get the value of a specific cell


# sheet.update_cell(1,4,'updated')
# sheet.update_cell(2,2, "CHANGED")  # Update one cell
# numRows = sheet.row_count  # Get the number of rows in the sheet


@dp.message_handler(Command('items'))
async def show_menu(message: types.Message):
    await message.answer('Выберите варианты', reply_markup=choice)


@dp.message_handler(Command('menu'))
async def show_menu(message: types.Message):
    await message.answer('Выберите варианты ниже', reply_markup=menu)


@dp.message_handler(user_id=ADMINS, commands=['tell_everyone'])
async def mailing(message: types.Message):
    await message.answer('Напишите текст рассылки')
    await Mailing.txt.set()


@dp.message_handler(text='Предложение')
async def get_offer(message: types.Message):
    await message.answer('Напишите свое предложение', reply_markup=ReplyKeyboardRemove())
    #sheet.append_row(['Предложения'])
    await Review.offer.set()


@dp.message_handler(state=Review.offer)
async def get_offer(message: types.Message, state=FSMContext):
    offer = message.text
    await state.update_data(offer1=offer)
    f_name = message.from_user.first_name if message.from_user.first_name else 'Empty value'
    l_name = message.from_user.last_name if message.from_user.last_name else 'Empty value'
    sheet.append_row([message.from_user.id, message.from_user.username, f_name,
                      l_name, offer])
    await state.reset_state()
    await message.answer('Спасибо за предложение!')


@dp.message_handler(text='Пожаловаться')
async def get_offer(message: types.Message):
    await message.answer('Напишите свою жаболу', reply_markup=ReplyKeyboardRemove())
    #sheet.append_row(['Жалоба'])
    await Review.complain.set()


@dp.message_handler(state=Review.complain)
async def get_offer(message: types.Message, state=FSMContext):
    complain = message.text
    await state.update_data(complain1=complain)
    f_name = message.from_user.first_name if message.from_user.first_name else 'Empty value'
    l_name = message.from_user.last_name if message.from_user.last_name else 'Empty value'
    sheet.append_row([message.from_user.id, message.from_user.username, f_name,
                      l_name, complain])
    await state.reset_state()
    await message.answer('Спасибо за отзыв!')


@dp.message_handler(user_id=ADMINS, state=Mailing.txt)
async def enter_text(message: types.Message, state=FSMContext):
    text = message.text
    await state.update_data(text=text)
    col = sheet.col_values(1)
    for id in set(col):
        if id not in ADMINS:
            try:
                await bot.send_message(chat_id=id, text=text)
                await sleep(0.3)
            except Exception:
                pass
    await state.finish()
    await message.answer('Рассылка выполнена')


