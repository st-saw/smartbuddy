"""
main.py
Главная точка входа для Telegram-бота анализа Solana-кошельков.

Импортирует все обработчики команд, состояний и запускает polling.
"""

import logging

from database.common.models import db, User, Analysis
from config_data.bot_instance import bot

# Импорт обработчиков команд и общих хэндлеров, чтобы они зарегистрировались в TeleBot
from handlers.default_handlers import (
    start,  # /start — приветствие и регистрация пользователя
    stop,  # /stop — отмена текущего диалога
    help,  # /help — справка
    common_handler,  # обработка состояний (fsm-like логика)
    analyze,  # /analyze — запуск анализа кошелька
    search_analysis,  # /search_analysis — поиск по истории анализов
    history,  # /history — история анализов
    clear_history,  # /clear_history — удалить историю анализов
    unknown_command,  # обработка неизвестных команд
)

from utils.wait_timer import start_waiting_timer, cancel_timer


def main() -> None:
    """
    Точка входа в приложение. Запускает polling для обработки сообщений.
    """
    # Автоматически создаём таблицы, если их нет
    with db:
        db.create_tables([User, Analysis], safe=True)

    logging.basicConfig(level=logging.INFO)
    print("Бот запущен")
    bot.infinity_polling(skip_pending=True)


if __name__ == "__main__":
    main()
