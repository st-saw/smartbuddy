from telebot.types import Message
from config_data.bot_instance import bot
from states.state import waiting_for_address
from utils.bot_helpers import format_result, select_history
from utils.wait_timer import cancel_timer
from utils.misc.constants import END_TEXT


def process_search_query(message: Message) -> None:
    """
    Обрабатывает запрос пользователя на поиск анализа по адресу кошелька или никнейму.
    Получает историю анализов, выводит их по одному. Если истории нет — сообщает об этом.
    Завершает сессию пользователя.

    Args:
        message (Message): Объект сообщения Telegram, инициировавший поиск.
    """
    user_id = message.from_user.id
    chat_id = message.chat.id
    state = waiting_for_address.get(user_id)
    if state == "search_query":
        analyses = select_history(message)

        analyses_count = analyses.count()
        if analyses_count:
            for analysis in analyses:
                bot.send_message(
                    chat_id,
                    format_result(analysis),
                    disable_web_page_preview=True,
                    parse_mode="HTML",
                )

        else:
            bot.send_message(chat_id, "Не удалось найти такой кошелёк или никнейм")
        # Очистка состояния пользователя и завершение диалога
        waiting_for_address.pop(user_id, None)
        cancel_timer(user_id)
        bot.send_message(chat_id, END_TEXT)
