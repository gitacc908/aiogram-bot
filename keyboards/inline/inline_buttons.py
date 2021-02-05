from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

choice = InlineKeyboardMarkup(row_width=2,
                              inline_keyboard=[
                                  [
                                      InlineKeyboardButton(
                                          text='Написать жалобу',
                                          callback_data='complaint'
                                      )
                                  ],
                                  [
                                      InlineKeyboardButton(
                                          text='Написать предложение',
                                          callback_data='offer'
                                      )
                                  ],
                                  [
                                    InlineKeyboardButton(
                                          text='Отмена',
                                          callback_data='cancel'
                                    )
                                  ],

                              ])