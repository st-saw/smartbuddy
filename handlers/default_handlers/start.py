from telebot.types import Message
from database.common.models import User
from config_data.bot_instance import bot
from keyboards.inline.help_button import gen_markup


@bot.message_handler(commands=["start"])
def send_welcome(message: Message) -> None:
    """
    Обрабатывает команду /start.
    Регистрирует пользователя в базе данных (если такого ещё нет) и отправляет приветственное сообщение с inline-кнопкой.

    Args:
        message (telebot.types.Message): Сообщение Telegram от пользователя.

    Notes:
        - User.get_or_create() гарантирует, что пользователь будет добавлен только один раз.
        - После /start пользователь сразу видит кнопку для перехода к справке.
    """
    telegram_id = message.from_user.id
    user, created = User.get_or_create(telegram_id=telegram_id)

    bot.send_message(
        telegram_id,
        "Привет 👋 Я бот для анализа Solana Smart-кошельков. Нажми кнопку ниже, чтобы начать и получить справку.",
        reply_markup=gen_markup(),
    )
