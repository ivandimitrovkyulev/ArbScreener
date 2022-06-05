import os
import sys
import json

from time import sleep
from atexit import register

from selenium.webdriver import Chrome

from src.exceptions import exit_handler_driver
from src.driver.driver import chrome_driver
from src.price_query import (
    swap_matcha_inch,
    swap_inch_matcha,
)
from src.variables import sleep_time


# Send telegram debug message if program terminates
program_name = os.path.abspath(os.path.basename(__file__))
register(exit_handler_driver, chrome_driver, program_name)


def scrape_prices(
        driver: Chrome,
        coin1: tuple,
        coin2: tuple,
) -> None:
    """
    Continuously scrapes spot prices between 2 token/coins.

    :param driver: Chrome webdriver instance
    :param coin1: A tuple of the coin to sell
    :param coin2: A tuple of the coin to buy
    :return: None
    """
    swap_amount_coin1 = coin1[3]
    min_diff_coin1 = coin1[4]

    swap_amount_coin2 = coin2[3]
    min_diff_coin2 = coin2[4]
    slippage = coin2[5]

    while True:

        # Check for Coin1 --> Coin2 arbitrage
        swap_matcha_inch(driver, swap_amount_coin1, min_diff_coin1, coin1, coin2, slippage)
        swap_inch_matcha(driver, swap_amount_coin1, min_diff_coin1, coin1, coin2, slippage)

        # Check for Coin2 --> Coin1 arbitrage
        swap_matcha_inch(driver, swap_amount_coin2, min_diff_coin2, coin2, coin1, slippage)
        swap_inch_matcha(driver, swap_amount_coin2, min_diff_coin2, coin2, coin1, slippage)

        # Sleep then query again
        sleep(sleep_time)


input_dict = json.loads(sys.argv[-1])

coin_1 = tuple(input_dict['coin1'].values())
coin_2 = tuple(input_dict['coin2'].values())

# Scrape prices for arbitrage opportunity and notify
scrape_prices(driver=chrome_driver, coin1=coin_1, coin2=coin_2)
