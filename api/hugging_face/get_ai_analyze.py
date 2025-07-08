import requests

from config_data.env import HUGGING_FACE_TOKEN
from config_data.bot_instance import bot
from telebot.types import Message


def mixtral_hf_analysis(prompt: str, message: Message = None) -> str | None:
    """
    Отправляет текстовый запрос (prompt) в Hugging Face (Mixtral 8x7B) и возвращает сгенерированный ответ.

    Args:
        prompt (str): Текстовый промт для языковой модели.
        message (Message, optional): Объект сообщения Telegram для уведомления пользователя об ошибках.

    Returns:
        str | None: Сгенерированный моделью ответ или None в случае ошибки.
    """
    api_token = HUGGING_FACE_TOKEN
    chat_id = message.chat.id if message else None

    if not api_token:
        if chat_id:
            bot.send_message(chat_id, "Ошибка: Hugging Face токен не найден.")
        return None

    url = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
    headers = {"Authorization": f"Bearer {api_token}"}
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 256, "temperature": 0.7},
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        if response.status_code == 200:
            output = response.json()

            if isinstance(output, list) and "generated_text" in output[0]:
                return output[0]["generated_text"]

            if isinstance(output, dict) and "generated_text" in output:
                return output["generated_text"]

            return str(output)

        elif response.status_code == 429:
            if chat_id:
                bot.send_message(
                    chat_id, "Лимит Hugging Face API превышен. Попробуй позже."
                )
            return None

        else:
            if chat_id:
                bot.send_message(
                    chat_id,
                    f"Ошибка Hugging Face API: {response.status_code} — {response.text}",
                )
            return None

    except Exception as e:
        if chat_id:
            bot.send_message(chat_id, f"Ошибка соединения с Hugging Face: {e}")
        return None
