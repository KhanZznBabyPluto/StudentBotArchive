from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text

def get_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/Authorize'))
    kb.add(KeyboardButton('/Display_Subjects'))
    kb.add(KeyboardButton('/Upload_Document'))
    kb.add(KeyboardButton('/Cancel'))
    
    return kb

recieve_document_kb = ReplyKeyboardMarkup(resize_keyboard = True)
recieve_document_kb.add(KeyboardButton('/Receive_Document'))

reactivate_kb = ReplyKeyboardMarkup(resize_keyboard=True)
reactivate_kb.add(KeyboardButton('/Reactivate_bot'))