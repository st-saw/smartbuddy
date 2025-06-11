from typing import Iterator

from telebot.types import Message
from config_data.bot_instance import bot
from states.state import waiting_for_address
from database.common.models import User, Analysis


def on_timeout(
    user_id: int,
    chat_id: int,
    message: Message = "Время ожидания истекло."
    "\nЧтобы начать заново, напиши команду или нажми /help.",
) -> None:
    """
    Вызывается по истечении таймера ожидания действия пользователя.
    Очищает состояние и отправляет уведомление в чат.

    Args:
        user_id (int): Telegram ID пользователя.
        chat_id (int): ID чата Telegram.
        message (str, optional): Сообщение для отправки пользователю.
    """
    waiting_for_address.pop(user_id, None)
    bot.send_message(chat_id, message)


def format_result(analysis: Analysis) -> str:
    """
    Форматирует результат анализа для вывода пользователю.

    Args:
        analysis (Analysis): Объект анализа из базы данных.

    Returns:
        str: Готовый к отправке текст результата.
    """
    short_address = shorten_address(analysis.wallet_address)
    return (
        f"Результат анализа по кошельку {short_address} ({analysis.nickname}):\n\n"
        f"{analysis.result}\n\n"
        f"Дата анализа: {analysis.created_at.strftime('%d.%m.%Y %H:%M')}"
    )


def select_history(message: Message) -> Iterator[Analysis]:
    """
    Получает список анализов пользователя по введённому адресу или никнейму.

    Args:
        message (telebot.types.Message): Сообщение Telegram с текстом-запросом.

    Returns:
        Iterator[Analysis]: Итератор по объектам Analysis пользователя,
        отсортированным по дате.
    """
    user_id = message.from_user.id
    user = User.get(telegram_id=user_id)
    query = message.text

    analyses = (
        Analysis.select()
        .where(
            (Analysis.user == user)
            & ((Analysis.wallet_address == query) | (Analysis.nickname == query))
        )
        .order_by(Analysis.created_at.desc())
    )

    return analyses


def shorten_address(address: str, first: int = 6, last: int = 4) -> str:
    """
    Сокращает длинный адрес кошелька для компактного вывода.

    Args:
        address (str): Адрес кошелька.
        first (int): Количество символов в начале.
        last (int): Количество символов в конце.

    Returns:
        str: Сокращённый адрес вида "abcdef...wxyz"
    """
    if len(address) <= first + last:
        return address
    return f"{address[:first]}...{address[-last:]}"
