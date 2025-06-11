from telebot.types import Message
from config_data.bot_instance import bot
from utils.wait_timer import cancel_timer
from states.state import waiting_for_address, pending_address


@bot.message_handler(commands=["stop"])
def handle_stop(message: Message) -> None:
    """
    Обрабатывает команду /stop.
    Останавливает все ожидающие сценарии пользователя: сбрасывает состояние ожидания,
    очищает временные данные, останавливает таймер и уведомляет пользователя об успешной отмене действия.

    Args:
        message (telebot.types.Message): Сообщение Telegram от пользователя.

    Notes:
        - Если для пользователя был активен процесс (ожидание ввода), он сбрасывается.
        - Если нет активных процессов — пользователь получает соответствующее уведомление.
    """
    user_id = message.from_user.id
    chat_id = message.chat.id

    in_dialog = False

    # Удаляем пользователя из состояния ожидания и временного хранилища
    if waiting_for_address.pop(user_id, None) is not None:
        in_dialog = True
    if pending_address.pop(user_id, None) is not None:
        in_dialog = True

    # Останавливаем связанный таймер (если он был запущен)
    cancel_timer(user_id)

    # Уведомляем пользователя о результате
    if in_dialog:
        bot.send_message(chat_id, "Действие отменено. Можешь выбрать новую команду.")
    else:
        bot.send_message(chat_id, "Сейчас нет активного действия для отмены.")
