import requests
from datetime import datetime
from collections import Counter
from typing import List

from config_data.env import HELIUS_API_KEY


def get_transactions(address: str) -> List[dict]:
    """
    Получает последние транзакции Solana-кошелька через Helius API.

    Args:
        address (str): Адрес Solana-кошелька.

    Returns:
        list[dict]: Список транзакций в формате, возвращаемом Helius API.
    """
    url = f"https://api.helius.xyz/v0/addresses/{address}/transactions"
    # в limit указывается количество транзакций для анализа (максимум 100)
    querystring = {"api-key": HELIUS_API_KEY, "limit": "100"}
    response = requests.request("GET", url, params=querystring)

    return response.json()


def parse_transactions(response: List[dict]) -> dict:
    """
    Строит summary по последним транзакциям: агрегирует топ токены, входящие/исходящие, крупные сделки, комиссии и другую активность.

    Args:
        response (list[dict]): Список транзакций (response из Helius API).

    Returns:
        dict: Словарь-резюме для дальнейшего анализа или формирования prompt.
    """
    top_tokens = Counter()
    nft_ops = 0
    swaps = 0
    airdrops = 0
    big_trades = []
    tx_in = 0
    tx_out = 0
    total_sol = 0
    total_fee = 0
    tx_list = []

    for item in response:
        # 1. Дата
        dt = datetime.fromtimestamp(item.get("timestamp")).strftime("%Y-%m-%d %H:%M")
        # 2. Описание
        desc = item.get("description", "нет описания")
        # 3. Тип транзакции
        tx_type = item.get("type", "")
        # 4. Суммы
        sol_amount = 0
        for transfer in item.get("nativeTransfers", []):
            amt = transfer.get("amount", 0)
            if amt > 0:
                tx_in += 1
            if amt < 0:
                tx_out += 1
            sol_amount += (
                abs(amt) / 1e9
            )  # Helius выдаёт amount в лампортах (1 SOL = 1e9)

        # 5. Токены
        for transfer in item.get("tokenTransfers", []):
            mint = transfer.get("mint", "")
            if mint:
                top_tokens[mint] += abs(transfer.get("tokenAmount", 0))
        # 6. NFT/Swap/Airdrop/Reward
        if "nft" in item.get("events", {}):
            nft_ops += 1
        if "swap" in item.get("events", {}):
            swaps += 1
        if "airdrop" in desc.lower() or tx_type == "AIRDROP":
            airdrops += 1
        # 7. Крупные сделки
        if sol_amount > 3:  # Порог для "крупной сделки"
            big_trades.append(f"{sol_amount:.3f} SOL ({dt})")
        # 8. Суммарный объём и комиссии
        total_sol += sol_amount
        total_fee += item.get("fee", 0) / 1e9

        # 9. Строим текст для LLM
        tx_list.append(
            f"{dt}: {desc} | {sol_amount:.4f} SOL, fee {item.get('fee', 0) / 1e9:.7f}"
        )

    top_5 = [k for k, v in top_tokens.most_common(5)]
    summary = {
        "top_tokens": top_5,
        "balance": round(total_sol, 4),
        "tx_in": tx_in,
        "tx_out": tx_out,
        "tx_list": tx_list[:5],  # Для prompt берём 5 последних
        "big_trades": ", ".join(big_trades) or "нет",
        "airdrops": f"{airdrops} за период" if airdrops else "нет",
        "nft_ops": nft_ops,
        "swaps": swaps,
        "avg_fee": round(total_fee / len(response), 7) if response else 0,
        "total_ops": len(response),
    }

    return summary
