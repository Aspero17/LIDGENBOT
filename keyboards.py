from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def main_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="СМС-Рассылка", callback_data="СМС-Рассылка")],
        [InlineKeyboardButton(text="WhatsApp-Рассылка", callback_data="WhatsApp-Рассылка")],
        [InlineKeyboardButton(text="Другой вопрос", callback_data="Другой вопрос")]
    ])
    return keyboard
