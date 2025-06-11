# 🧠 SmartBuddy — твой напарник в мире Solana

## О проекте

**SmartBuddy** — это Telegram-бот для анализа Solana-кошельков с помощью API Helius.  
Бот сохраняет и показывает историю анализов, позволяет искать по кошельку или никнейму, легко очищает историю и поддерживает удобный диалог (FSM).  
SmartBuddy помогает новичкам и трейдерам быстро ориентироваться в активностях кошельков, не требуя глубоких знаний кода и блокчейна.

---

## 📁 Структура проекта

<details>
<summary>Развернуть дерево проекта</summary>

```
📦 python_basic_diploma/
├── api/
│   └── helius/
│       ├── __init__.py
│       └── get_transactions.py
├── config_data/
│   ├── __init__.py
│   ├── bot_instance.py
│   └── env.py
├── database/
│   └── common/
│       ├── __init__.py
│       └── models.py
├── handlers/
│   └── default_handlers/
│       ├── __init__.py
│       ├── analyze.py
│       ├── clear_history.py
│       ├── common_handler.py
│       ├── help.py
│       ├── history.py
│       ├── search_analysis.py
│       ├── start.py
│       └── stop.py
├── keyboards/
│   └── inline/
│       ├── __init__.py
│       └── help_button.py
├── states/
│   ├── __init__.py
│   └── state.py
├── utils/
│   └── misc/
│       ├── __init__.py
│       ├── analysis_helpers.py
│       ├── bot_helpers.py
│       ├── constants.py
│       ├── search_helpers.py
│       └── wait_timer.py
├── .env
├── main.py
├── requirements.txt
└── .gitignore
```
</details>

---

## 🗂️ Описание основных файлов

- `api/helius/get_transactions.py`  
  🔹 Получение истории транзакций через REST API Helius  
  🔹 Функции для парсинга, форматирования и сокращения адресов

- `config_data/env.py`  
  🔹 Загрузка переменных окружения (`TELEGRAM_BOT_TOKEN`, `HELIUS_API_KEY`) из `.env`

- `database/common/models.py`  
  🔹 Peewee-модели:
  - `User` — Telegram-пользователь  
  - `Analysis` — анализ кошелька (адрес, никнейм, результат, дата)

- `handlers/default_handlers/`  
  🔹 Обработчики команд Telegram-бота:  
  `/start`, `/help`, `/analyze`, `/search_analysis`, `/history`, `/clear_history`, `/stop`

- `handlers/default_handlers/common_handler.py`  
  🔹 FSM-логика диалогов (ожидание адреса, никнейма и др.)

- `keyboards/inline/help_button.py`  
  🔹 Кнопка для вызова справки

- `states/state.py`  
  🔹 Словарь состояний:  
  `waiting_for_address`, `pending_address`

- `utils/misc/constants.py`  
  🔹 Константы:
  - `TIMEOUT_SECONDS = 600` — ожидание пользователя (сек)  
  - `END_TEXT = "Можешь отправить новую команду или /help."` — сообщение по завершении анализа

- `main.py`  
  🔹 Точка входа. Создаёт БД и таблицы, запускает polling

- `.env`  
  🔒 Секретные ключи (**не загружай в публичные репозитории**)

- `requirements.txt`  
  📦 Список зависимостей проекта

- `.gitignore`  
  🧾 Исключения для Git:
  - `*.pyc` — служебные файлы Python  
  - `*.db` — база данных  
  - `.env` — конфиденциальные ключи


---

## 🚀 Быстрый старт

1. **Склонируйте репозиторий и перейдите в директорию проекта:**
    ```bash
    git clone https://github.com/st-saw/smartbuddy.git
    cd python_basic_diploma
    ```

2. **Создайте виртуальное окружение (рекомендуется):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # или .\venv\Scripts\activate для Windows
    ```

3. **Установите зависимости:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Создайте файл `.env` и добавьте ваши ключи:**
    ```
    TELEGRAM_BOT_TOKEN=ваш_токен_бота
    HELIUS_API_KEY=ваш_ключ_helius
    ```

5. **Запустите бота:**
    ```bash
    python main.py
    ```

    При первом запуске база данных и таблицы создадутся автоматически.

---

## ⚡ Основные команды бота

- `/start` — Запуск бота и регистрация пользователя
- `/help` — Справка и список команд
- `/analyze` — Анализировать Solana-кошелёк по адресу
- `/search_analysis` — Поиск анализа по кошельку или никнейму
- `/history` — Ваша история анализов
- `/clear_history` — Удаление истории анализов
- `/stop` — Прервать текущий диалог

---

## 🧩 FSM и обработка сообщений

Бот поддерживает FSM (finite state machine) — последовательное общение:
- Ожидание адреса
- Ожидание никнейма
- Поиск анализа по адресу/никнейму  
В любой момент можно прервать диалог командой `/stop`.

---

## 👨‍💻 Автор и поддержка

Telegram: [@uyrivihodnoy](https://t.me/uyrivihodnoy)

---

## 🛡️ Важно

- **Не публикуйте свои секретные ключи!**  
- Файл `.env` должен быть добавлен в `.gitignore`.
- Проект развивай и кастомизируй под свои задачи!

---

**Удачи в анализе Solana-кошельков с SmartBuddy! 🚀**
