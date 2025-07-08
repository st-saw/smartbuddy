import re

from telebot.types import Message
from config_data.bot_instance import bot
from database.common.models import User, Analysis
from handlers.default_handlers import search_analysis, stop
from states.state import waiting_for_address, pending_address
from utils.ai_helpers import analyze_wallet_with_ai
from utils.bot_helpers import format_result
from utils.wait_timer import cancel_timer
from utils.misc.constants import END_TEXT


def process_analyze_query(message: Message) -> None:
    """
    Обрабатывает этап запроса адреса Solana-кошелька.

    1. Проверяет валидность адреса через регулярное выражение.
    2. Проверяет, был ли этот адрес уже проанализирован данным пользователем.
    3. Если всё хорошо, запрашивает никнейм для этого кошелька.

    Args:
        message (Message): Объект сообщения Telegram от пользователя.
    """
    user_id = message.from_user.id
    user = User.get(telegram_id=user_id)
    chat_id = message.chat.id
    query = message.text
    state = waiting_for_address.get(user_id)

    if query == "/search_analysis":
        waiting_for_address.pop(user_id, None)

    elif state == "analyze_query":
        # Проверяем адрес на валидность
        if re.match(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$", query):
            # Проверяем, был ли этот кошелек уже проанализирован этим пользователем
            wallet_exists = (
                Analysis.select()
                .where((Analysis.user == user) & (Analysis.wallet_address == query))
                .exists()
            )

            if wallet_exists:
                bot.send_message(
                    chat_id,
                    "Ты уже анализировал этот кошелёк.\nПопробуй найти его по команде /search_analysis "
                    "или введи другой кошелёк",
                )

            else:
                pending_address[user_id] = query
                waiting_for_address[user_id] = "nickname_query"
                bot.send_message(chat_id, "Как хочешь назвать этот кошелёк?")

        else:
            bot.send_message(
                chat_id,
                "Адрес не соответствует стандарту Solana base58, проверь адрес и повтори попытку.",
            )


def process_nickname(message: Message) -> None:
    """
    Обрабатывает этап ввода никнейма для Solana-кошелька.

    1. Проверяет уникальность никнейма для этого пользователя.
    2. Получает транзакции по кошельку через Helius API.
    3. Формирует анализ и сохраняет его в базе.
    4. Отправляет результат пользователю.

    Args:
        message (Message): Объект сообщения Telegram от пользователя.
    """
    user_id = message.from_user.id
    user = User.get(telegram_id=user_id)
    chat_id = message.chat.id
    query = message.text
    state = waiting_for_address.get(user_id)

    if state == "nickname_query":
        # Проверяем уникальность никнейма для пользователя
        nickname_exists = (
            Analysis.select()
            .where((Analysis.user == user) & (Analysis.nickname == query))
            .exists()
        )

        if nickname_exists:
            bot.send_message(
                chat_id, "Такой никнейм уже существует, попробуй назвать по другому."
            )

        else:
            # Получаем AI-анализ по кошельку
            wallet_analyze_info = analyze_wallet_with_ai(pending_address[user_id])
            # Сохраняем результат анализа
            analysis = Analysis.create(
                user=user,
                wallet_address=pending_address[user_id],
                nickname=query,
                result=wallet_analyze_info,
            )
            # Отправляем результат пользователю
            bot.send_message(
                chat_id,
                format_result(analysis),
                disable_web_page_preview=True,
                parse_mode="HTML",
            )
            # Чистим временные состояния и таймеры
            waiting_for_address.pop(user_id, None)
            pending_address.pop(user_id, None)
            cancel_timer(user_id)
            bot.send_message(chat_id, END_TEXT)
