from telebot.types import Message

from utils.misc.constants import END_TEXT
from config_data.bot_instance import bot
from database.common.models import User, Analysis


@bot.message_handler(commands=["history"])
def send_history(message: Message) -> None:
    """
    Обрабатывает команду /history.
    Ищет в базе данных все анализы пользователя и отправляет их краткую историю в виде сообщения.
    Если история пуста — информирует пользователя.

    Args:
        message (telebot.types.Message): Входящее сообщение Telegram от пользователя.

    Notes:
        - Дата и время каждого анализа форматируются как 'дд.мм.гггг чч:мм'.
        - Если у пользователя нет анализов — отправляется сообщение "История запросов пуста".
    """
    user_id = message.from_user.id
    user = User.get_or_none(telegram_id=user_id)

    analyses = (
        Analysis.select()
        .where(Analysis.user == user)
        .order_by(Analysis.created_at.desc())
    )

    if analyses:
        text = "История анализов:\n\n"

        for analysis in analyses:
            text += (
                f"Дата: {analysis.created_at.strftime('%d.%m.%Y %H:%M')}\n"
                f"Кошелёк: {analysis.wallet_address}\n"
                f"Никнейм: ({analysis.nickname})\n\n"
            )

        bot.send_message(message.chat.id, text)

    else:
        bot.send_message(message.chat.id, "История запросов пуста")

    bot.send_message(message.chat.id, END_TEXT)
