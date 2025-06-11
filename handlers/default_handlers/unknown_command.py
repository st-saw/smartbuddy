from telebot.types import Message
from config_data.bot_instance import bot


@bot.message_handler(func=lambda message: True)
def handle_unknown_command(message: Message) -> None:
    """
    Обработчик неизвестных команд вне активного диалога (FSM).

    Args:
        message (Message): Сообщение пользователя.
    """
    bot.send_message(
        message.chat.id,
        "❓ Неизвестная команда. Используй /help, чтобы посмотреть список доступных команд.",
    )
