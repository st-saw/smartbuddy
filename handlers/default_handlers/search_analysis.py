from telebot.types import Message
from config_data.bot_instance import bot
from utils.wait_timer import start_waiting_timer
from utils.bot_helpers import on_timeout
from utils.misc.constants import TIMEOUT_SECONDS
from states.state import waiting_for_address


@bot.message_handler(commands=["search_analysis"])
def ask_for_address_or_nickname(message: Message) -> None:
    """
    Обрабатывает команду /search_analysis.
    Переводит пользователя в состояние ожидания ввода адреса или никнейма для поиска анализа.
    Запускает таймер ожидания.

    Args:
        message (telebot.types.Message): Сообщение Telegram от пользователя.

    Notes:
        - После вызова этой команды бот ожидает ввода адреса или никнейма для поиска анализа.
        - Если пользователь не введёт данные за отведённое время, будет вызвана функция on_timeout.
    """
    user_id = message.from_user.id
    chat_id = message.chat.id
    waiting_for_address[user_id] = "search_query"
    bot.send_message(chat_id, "Пришли адрес кошелька или никнейм для поиска")
    start_waiting_timer(user_id, chat_id, TIMEOUT_SECONDS, on_timeout)
