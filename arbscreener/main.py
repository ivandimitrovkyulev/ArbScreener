import os
import sys
import json

from time import sleep
from atexit import register
from datetime import datetime
from pprint import pprint

from selenium.webdriver import Chrome

from src.exceptions import exit_handler_driver
from src.driver.driver import chrome_driver
from src.swap import (
    swap_matcha_inch,
    swap_inch_matcha,
)
from src.variables import (
    sleep_time,
    time_format,
)


def scrape_prices(
        driver: Chrome,
        coin1: tuple,
        coin2: tuple,
        debug: bool = False,
) -> None:
    """
    Continuously scrapes spot prices between 2 token/coins.

    :param driver: Chrome webdriver instance
    :param coin1: A tuple of the coin to sell
    :param coin2: A tuple of the coin to buy
    :param debug: If True will print all transactions in terminal
    :return: None
    """
    swap_amount_coin1 = coin1[3]
    min_diff_coin1 = coin1[4]

    swap_amount_coin2 = coin2[3]
    min_diff_coin2 = coin2[4]
    slippage = coin2[5]

    while True:

        # Check for Coin1 --> Coin2 arbitrage
        swap_matcha_inch(driver, swap_amount_coin1, min_diff_coin1, coin1, coin2, slippage, debug=debug)
        swap_inch_matcha(driver, swap_amount_coin1, min_diff_coin1, coin1, coin2, slippage, debug=debug)

        # Check for Coin2 --> Coin1 arbitrage
        swap_matcha_inch(driver, swap_amount_coin2, min_diff_coin2, coin2, coin1, slippage, debug=debug)
        swap_inch_matcha(driver, swap_amount_coin2, min_diff_coin2, coin2, coin1, slippage, debug=debug)

        # Sleep then query again
        sleep(sleep_time)


# Send telegram debug message if program terminates
program_name = os.path.abspath(os.path.basename(__file__))
register(exit_handler_driver, chrome_driver, program_name)
timestamp = datetime.now().astimezone().strftime(time_format)

input_dict = json.loads(sys.argv[-1])

coin_1 = tuple(input_dict['coin1'].values())
coin_2 = tuple(input_dict['coin2'].values())

print(f"{timestamp}\n"
      f"\tStarted arbitrage screening with the following settings:\n"
      f"\t{coin_1[0]}/{coin_2[0]} and {coin_2[0]}/{coin_1[0]}\n"
      f"\thttps://matcha.xyz --> https://app.1inch.io\n"
      f"\thttps://app.1inch.io --> https://matcha.xyz\n")
pprint(input_dict, indent=4)

# Scrape prices for arbitrage opportunity and notify
scrape_prices(driver=chrome_driver, coin1=coin_1, coin2=coin_2)
