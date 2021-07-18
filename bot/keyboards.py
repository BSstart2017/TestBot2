from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


inline_btn_1 = InlineKeyboardButton('Текущий баланс', callback_data='button1')
inline_btn_2 = InlineKeyboardButton('Создать карточку', callback_data='button2')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1, inline_btn_2)

inline_btn_3 = InlineKeyboardButton('Сегодня', callback_data='button3')
inline_btn_4 = InlineKeyboardButton('Календарь', callback_data='button4')
inline_btn_5 = InlineKeyboardButton('Отмена', callback_data='button5')
inline_kb2 = InlineKeyboardMarkup().add(inline_btn_3, inline_btn_4, inline_btn_5)