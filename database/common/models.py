from datetime import datetime
import os

import peewee as pw


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "memebase.db")

# Инициализация базы данных SQLite
db = pw.SqliteDatabase(db_path)


class BaseModel(pw.Model):
    """
    Базовая модель для всех таблиц проекта.

    Атрибуты:
        Meta.database (peewee.Database): Ссылка на объект базы данных.
    """

    class Meta:
        database = db


class User(BaseModel):
    """
    Модель пользователя Telegram-бота.

    Атрибуты:
        telegram_id (int): Уникальный идентификатор пользователя Telegram.
    """

    telegram_id = pw.IntegerField(unique=True)


class Analysis(BaseModel):
    """
    Модель анализа кошелька пользователя.

    Атрибуты:
        user (User): Ссылка на пользователя (внешний ключ).
        wallet_address (str): Адрес Solana-кошелька.
        nickname (str): Никнейм кошелька, заданный пользователем.
        created_at (datetime): Дата и время создания анализа.
        result (str): Текстовый результат анализа (например, отчёт по транзакциям).
    """

    user = pw.ForeignKeyField(User, backref="analyses")
    wallet_address = pw.CharField()
    nickname = pw.CharField()
    created_at = pw.DateTimeField(default=datetime.now)
    result = pw.TextField()
