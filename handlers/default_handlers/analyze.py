from telebot.types import Message
from config_data.bot_instance import bot
from utils.wait_timer import start_waiting_timer
from utils.bot_helpers import on_timeout
from utils.misc.constants import TIMEOUT_SECONDS
from states.state import waiting_for_address


@bot.message_handler(commands=["analyze"])
def ask_for_address(message: Message) -> None:
    """
    Обрабатывает команду /analyze. Запрашивает у пользователя адрес Solana-кошелька
    и переводит пользователя в состояние ожидания ввода адреса.

    Args:
        message (telebot.types.Message): Объект входящего сообщения Telegram.
    """
    user_id = message.from_user.id
    chat_id = message.chat.id
    waiting_for_address[user_id] = "analyze_query"
    bot.send_message(
        chat_id, "Пришли адрес Solana - кошелька или нажми /stop, если передумал."
    )
    start_waiting_timer(user_id, chat_id, TIMEOUT_SECONDS, on_timeout)
