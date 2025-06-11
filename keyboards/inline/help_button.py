from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def gen_markup() -> InlineKeyboardMarkup:
    """
    Генерирует inline-клавиатуру с одной кнопкой "Справка".

    Returns:
        InlineKeyboardMarkup: Клавиатура с одной inline-кнопкой для запроса справки.

    Example:
        reply_markup = gen_markup()
        bot.send_message(chat_id, "Нажми кнопку ниже для справки.", reply_markup=reply_markup)
    """
    keyboard = InlineKeyboardMarkup()
    help_button = InlineKeyboardButton(text="Справка", callback_data="help")
    keyboard.add(help_button)
    return keyboard
