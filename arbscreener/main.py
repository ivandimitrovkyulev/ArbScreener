import os

from time import sleep
from datetime import datetime
from pprint import pprint
from atexit import register

from selenium.webdriver import Chrome

from src.exceptions import exit_handler_driver
from src.driver.driver import chrome_driver
from src.price_query import (
    query_inch,
    query_matcha,
)
from src.variables import (
    sleep_time,
    time_format,
)


# Send telegram debug message if program terminates
program_name = os.path.abspath(os.path.basename(__file__))
#register(exit_handler_driver, chrome_driver, program_name)


def scrape_prices(
        driver: Chrome,
        amount: float,
        min_difference: float,
        coin1: tuple = ('USDC', '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48', 6),
        coin2: tuple = ('ETH', '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee', 18),
        slippage: float = 0.1,
) -> None:
    """
    Continuously scrapes spot prices between 2 token/coins.

    :param driver: Chrome webdriver instance
    :param amount: Amount of coin1 to swap
    :param min_difference: Min difference required for Arbitrage
    :param coin1: A tuple of Name & Address of coin to sell
    :param coin2: A tuple of Name & Address of coin to buy
    :param slippage: Slippage tolerance in %
    :return: None
    """

    while True:

        matcha_info = query_matcha(driver, amount, coin1, coin2)
        coin2_received = matcha_info['toToken']['amount']

        inch_info = query_inch(coin2_received, coin2, coin1, slippage)

        coin1_received = inch_info['toToken']['amount']
        coin1_min_received = inch_info['min_received']

        arb_opportunity = coin1_received - amount
        min_arb_opportunity = coin1_min_received - amount

        timestamp = datetime.now().astimezone().strftime(time_format)

        print(f"{timestamp}\n"
              f"\tSell {amount} {coin1[0]} for {coin2_received} {coin2[0]} on Matcha ->\n"
              f"\tSell {coin2_received} {coin2[0]} for {coin1_received} {coin1[0]} on 1inch\n"
              f"\tArbitrage opportunity: {arb_opportunity}")

        # Sleep then query again
        sleep(sleep_time)


USDC = ('USDC', '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48', 6)
WETH = ('WETH', '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', 18)
swap_amount = 100000
difference = 100

scrape_prices(chrome_driver, swap_amount, difference, USDC, WETH)
