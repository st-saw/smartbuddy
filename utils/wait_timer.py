import threading
from typing import Callable, Dict

timers: Dict[int, threading.Timer] = dict()


def start_waiting_timer(
    user_id: int,
    chat_id: int,
    timeout: float,
    on_timeout: Callable[[int, int], None],
) -> None:
    """
    Запускает таймер ожидания для пользователя. Если таймер уже был запущен для этого пользователя, он будет отменён.

    Args:
        user_id (int): Telegram ID пользователя.
        chat_id (int): ID чата, в котором идёт диалог.
        timeout (float): Время ожидания в секундах.
        on_timeout (Callable[[int, int], None]): Функция, вызываемая при истечении таймера, с аргументами user_id и chat_id.
    """
    if timers.get(user_id):
        timers[user_id].cancel()

    timer = threading.Timer(timeout, on_timeout, args=[user_id, chat_id])
    timers[user_id] = timer
    timer.start()


def cancel_timer(user_id: int) -> None:
    """
    Отменяет таймер ожидания для пользователя, если он был запущен.

    Args:
        user_id (int): Telegram ID пользователя.
    """
    if timers.get(user_id):
        timers[user_id].cancel()
        timers.pop(user_id, None)
