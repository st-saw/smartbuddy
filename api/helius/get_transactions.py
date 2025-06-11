import requests
import json
import re
from datetime import datetime, timezone

from config_data.env import HELIUS_API_KEY
from utils.bot_helpers import shorten_address
from typing import Iterator, Optional


def replace_address_in_description(description: str) -> str:
    """
    Заменяет полный адрес кошелька на сокращённый вид в начале описания транзакции.

    Args:
        description (str): Описание транзакции, содержащее полный адрес.

    Returns:
        str: Описание с сокращённым адресом (если найден), иначе исходное описание.
    """
    match = re.match(r"([1-9A-HJ-NP-Za-km-z]{32,44})", description)
    if match:
        addr = match.group(1)
        short = shorten_address(addr)
        return description.replace(addr, short, 1)
    return description


def extract_sol_amount(description: str) -> Optional[float]:
    """
    Извлекает сумму SOL из описания транзакции.

    Args:
        description (str): Описание транзакции.

    Returns:
        Optional[float]: Сумма в SOL, если найдена, иначе None.
    """
    match = re.search(r"(\d+\.?\d*) SOL", description)
    if match:
        return float(match.group(1))
    return None


def get_transactions(address: str) -> Iterator[str]:
    """
    Получает и форматирует историю транзакций для указанного Solana-кошелька.

    Args:
        address (str): Адрес Solana-кошелька.

    Yields:
        str: Отформатированный отчёт по каждой транзакции (HTML-разметка для Telegram).
    """
    url = f"https://api.helius.xyz/v0/addresses/{address}/transactions"
    # в limit указывается количество транзакций для анализа (максимум 100)
    querystring = {"api-key": HELIUS_API_KEY, "limit": "2"}

    response = json.loads(requests.request("GET", url, params=querystring).text)

    for item in response:
        dt = datetime.fromtimestamp(item["timestamp"], tz=timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        number = extract_sol_amount(item["description"])
        quantity = len(item["nativeTransfers"])

        receivers_quantity = (
            f"{quantity} получателей" if quantity > 1 else f"{quantity} получателя"
        )

        amount = (
            f"{number:.6f} SOL для {receivers_quantity}" if number is not None else "0"
        )

        desc = item["description"]
        desc_short = replace_address_in_description(desc)

        fee_sol = item["fee"] / 1_000_000_000

        tx_link = f'https://solscan.io/tx/{item["signature"]}'

        report = (
            f"\n🕒 <b>{dt}</b> 🕒\n\n"
            f"➡️ <b>Количество</b>: {amount}\n"
            f"📃 <b>Описание</b>: {desc_short}\n"
            f"💸 <b>Комиссия</b>: {fee_sol:.9f} SOL\n"
            f'🔗 <b>Подробнее</b>: <a href="{tx_link}">solscan.io</a>'
        )

        yield report
