from datetime import datetime

from selenium.webdriver import Chrome

from .message import telegram_send_message
from .logger import log_arbitrage
from .price_query import (
    query_matcha,
    query_inch,
)
from .variables import time_format


def swap_matcha_inch(
        driver: Chrome,
        amount: float,
        min_difference: float,
        coin1: tuple = ('USDC', '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48', 6),
        coin2: tuple = ('WETH', '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', 18),
        slippage: float = 0.1,
        rounding: int = 5,
        debug: bool = False,
):
    """
    Continuously scrapes spot prices between 2 token/coins.

    :param driver: Chrome webdriver instance
    :param amount: Amount of coin1 to swap
    :param min_difference: Min difference required for Arbitrage
    :param coin1: A tuple of Name & Address of coin to sell
    :param coin2: A tuple of Name & Address of coin to buy
    :param slippage: Slippage tolerance in %
    :param rounding: Number of decimals to round to
    :param debug: If True will print all transactions in terminal
    :return: None
    """

    matcha_info = query_matcha(driver, amount, coin1, coin2)
    # If dict is empty - return
    if not matcha_info:
        return

    coin2_received = matcha_info['toToken']['amount']

    inch_info = query_inch(coin2_received, coin2, coin1, slippage)
    # If dict is empty - return
    if inch_info:
        return

    coin1_received = inch_info['toToken']['amount']
    arb_opportunity = round((coin1_received - amount), rounding)

    # coin1_min_received = inch_info['min_received']
    # min_arb_opportunity = coin1_min_received - amount

    timestamp = datetime.now().astimezone().strftime(time_format)

    message = f"{timestamp}\n" \
              f"\thttps://matcha.xyz --> https://app.1inch.io\n" \
              f"\tSell {amount:,} {coin1[0]} for {coin2_received:,} {coin2[0]} on Matcha ->\n" \
              f"\tSell {coin2_received:,} {coin2[0]} for {coin1_received:,} {coin1[0]} on 1inch\n" \
              f"\tArbitrage: {arb_opportunity:,} {coin1[0]}"

    # If debug True - only print to terminal
    if debug:
        print(message)
    # If arbitrage is at least the min required
    elif arb_opportunity >= min_difference:
        # Log, send Telegram message and print to terminal
        log_arbitrage.info(message)
        telegram_send_message(message)
        print(message)


def swap_inch_matcha(
        driver: Chrome,
        amount: float,
        min_difference: float,
        coin1: tuple = ('USDC', '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48', 6),
        coin2: tuple = ('WETH', '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', 18),
        slippage: float = 0.1,
        rounding: int = 5,
        debug: bool = False,
):
    """
    Continuously scrapes spot prices between 2 token/coins.

    :param driver: Chrome webdriver instance
    :param amount: Amount of coin1 to swap
    :param min_difference: Min difference required for Arbitrage
    :param coin1: A tuple of Name & Address of coin to sell
    :param coin2: A tuple of Name & Address of coin to buy
    :param slippage: Slippage tolerance in %
    :param rounding: Number of decimals to round to
    :param debug: If True will print all transactions in terminal
    :return: None
    """

    inch_info = query_inch(amount, coin1, coin2, slippage)
    # If dict is empty - return
    if not inch_info:
        return

    coin2_received = inch_info['toToken']['amount']

    matcha_info = query_matcha(driver, coin2_received, coin2, coin1)
    # If dict is empty - return
    if not matcha_info:
        return

    coin1_received = matcha_info['toToken']['amount']
    arb_opportunity = round((coin1_received - amount), rounding)

    # coin1_min_received = inch_info['min_received']
    # min_arb_opportunity = coin1_min_received - amount

    timestamp = datetime.now().astimezone().strftime(time_format)
    message = f"{timestamp}\n" \
              f"\thttps://app.1inch.io --> https://matcha.xyz\n" \
              f"\tSell {amount:,} {coin1[0]} for {coin2_received:,} {coin2[0]} on 1inch ->\n" \
              f"\tSell {coin2_received:,} {coin2[0]} for {coin1_received:,} {coin1[0]} on Matcha\n" \
              f"\tArbitrage: {arb_opportunity:,} {coin1[0]}"

    # If debug True - only print to terminal
    if debug:
        print(message)
    # If arbitrage is at least the min required
    elif arb_opportunity >= min_difference:
        # Log, send Telegram message and print to terminal
        telegram_send_message(message)
        log_arbitrage.info(message)
        print(message)
