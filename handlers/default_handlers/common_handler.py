from telebot.types import Message
from config_data.bot_instance import bot
from states.state import waiting_for_address
from utils.analysis_helpers import process_analyze_query, process_nickname
from utils.search_helpers import process_search_query


@bot.message_handler(func=lambda m: waiting_for_address.get(m.from_user.id))
def common_handler(message: Message) -> None:
    """
    FSM-хендлер: обрабатывает все сообщения пользователя в активном диалоге (анализ, ввод никнейма, поиск).
    Если пользователь введёт команду (начинается с "/"), получит предупреждение о необходимости завершить диалог.

    Args:
        message (telebot.types.Message): Входящее сообщение пользователя.
    """
    user_id = message.from_user.id
    state = waiting_for_address.get(user_id)

    # Если пользователь пытается ввести любую команду во время диалога
    if message.text and message.text.startswith("/"):
        bot.send_message(
            message.chat.id,
            "⚠️ Пожалуйста, заверши текущий диалог или используй /stop для отмены.",
        )
        return

    if state == "analyze_query":
        process_analyze_query(message)
    elif state == "nickname_query":
        process_nickname(message)
    elif state == "search_query":
        process_search_query(message)
