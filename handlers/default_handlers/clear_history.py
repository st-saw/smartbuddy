from telebot.types import Message
from config_data.bot_instance import bot
from database.common.models import User, Analysis


@bot.message_handler(commands=["clear_history"])
def clear_history(message: Message) -> None:
    """
    Обрабатывает команду /clear_history.
    Удаляет все записи анализа пользователя из базы данных и уведомляет пользователя о результате.

    Args:
        message (telebot.types.Message): Входящее сообщение Telegram от пользователя.
    """
    user_id = message.from_user.id
    user = User.get_or_none(telegram_id=user_id)
    if not user:
        bot.send_message(message.chat.id, "Пользователь не найден.")
        return

        # Удаляем все анализы пользователя
    deleted = Analysis.delete().where(Analysis.user == user).execute()
    if deleted > 0:
        bot.send_message(
            message.chat.id, f"История ({deleted} записей) успешно удалена."
        )
    else:
        bot.send_message(message.chat.id, "История уже пуста.")
