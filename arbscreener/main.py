from time import sleep
from pprint import pprint

from selenium.webdriver import Chrome

from src.driver.driver import chrome_driver
from src.price_query import (
    query_inch,
    query_matcha,
)
from src.variables import sleep_time


def scrape_prices(
        driver: Chrome,
        amount: float,
        coin1: tuple = ('USDC', '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48', 6),
        coin2: tuple = ('ETH', '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee', 18),
        slippage: float = 0.1,
) -> None:
    """
    Continuously scrapes spot prices between 2 token/coins.

    :param driver: Chrome webdriver instance
    :param amount: Amount of coin1 to swap
    :param coin1: A tuple of Name & Address of coin to sell
    :param coin2: A tuple of Name & Address of coin to buy
    :param slippage: Slippage tolerance in %
    :return: None
    """

    while True:
        # Query matcha.xyz
        matcha_info = query_matcha(driver, amount, coin1, coin2)
        # Query 1inch.io
        inch_info = query_inch(amount, coin1, coin2, slippage)

        pprint(f"Matcha: {matcha_info}")
        pprint(f"1inch: {inch_info}")

        # Sleep then query again
        sleep(sleep_time)


coin_1 = ('USDC', '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48', 6)
coin_2 = ('ETH', '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee', 18)
swap_amount = 100000

scrape_prices(chrome_driver, swap_amount, coin_1, coin_2)
