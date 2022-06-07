import time
import requests
import functools

from dataclasses import dataclass

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from .exceptions import driver_wait_exception_handler
from .logger import log_error
from .variables import request_wait_time


@dataclass
class AverageTime:
    """Class for keeping track of average time execution."""
    counter: int = 0
    time_sum: float = 0


def timer(func):
    """Print the runtime of the decorated function"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time

        AverageTime.counter += 1
        AverageTime.time_sum += run_time

        print(f"Finished {func.__name__!r} in {run_time:.6f} secs")

        return value

    return wrapper


@driver_wait_exception_handler(wait_time=5)
def query_matcha(
        driver: Chrome,
        amount: float,
        coin1: tuple = ('USDC', '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48', 6),
        coin2: tuple = ('WETH', '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', 18),
) -> dict:
    """
    Queries matcha.xyz for spot price between 2 coin/token addresses.

    :param driver: Chrome webdriver instance
    :param amount: Amount of coin1 to swap
    :param coin1: A tuple of Name & Address, Decimals of coin to ell
    :param coin2: A tuple of Name & Address, Decimals of coin to buy
    :return: Dictionary with swap information
    """

    coin1_name = coin1[0].upper()
    coin1_address = coin1[1].lower()
    coin2_name = coin2[0].upper()
    coin2_address = coin2[1].lower()

    amount = float(amount)

    # Get page to scrape
    url = f"https://matcha.xyz/markets/1/{coin2_address}/{coin1_address}"
    driver.get(url)

    try:
        inp1_xpath = "//*[@id='trading-page-container']/div[2]/div/div/aside/div[1]/div/div/div[4]/div[2]/input"
        input1 = WebDriverWait(driver, request_wait_time).until(ec.presence_of_element_located(
            (By.XPATH, inp1_xpath)))
        # Send amount for query
        input1.send_keys(amount)

        # Wait for swap to calculate
        button_xpath = "rfqm-switch"
        button = WebDriverWait(driver, request_wait_time).until(ec.presence_of_element_located(
            (By.ID, button_xpath)))

        gasless_xpath = "//*[@id='trading-page-container']/div[2]/div/div/aside/div[1]/div/div/div[7]/div[2]"
        gasless = WebDriverWait(driver, request_wait_time).until(ec.presence_of_element_located(
            (By.XPATH, gasless_xpath)))

        # If gasless button not activated - activate it
        if "free" not in gasless.text.lower():
            driver.execute_script("arguments[0].click();", button)

        inp2_xpath = "//*[@id='trading-page-container']/div[2]/div/div/aside/div[1]/div/div/div[6]/div[3]/div[2]/input"
        input2 = WebDriverWait(driver, request_wait_time).until(ec.presence_of_element_located(
            (By.XPATH, inp2_xpath)))

        # Get amount received
        received_amount = float(input2.get_attribute("value"))

        rate = amount / received_amount

        return {
            'fromToken': {'name': coin1_name, 'amount': amount},
            'toToken': {'name': coin2_name, 'amount': received_amount},
            'rate': f"1 {coin2_name} = {rate} {coin1_name}",
        }

    except Exception as e:
        log_error.warning(f"{e}")
        return {}


def query_inch(
        amount: float,
        coin1: tuple = ('USDC', '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48', 6),
        coin2: tuple = ('WETH', '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', 18),
        slippage: float = 0.1,
) -> dict:
    """
    Queries 1inch for spot price between 2 coin/token addresses.

    :param amount: Amount of coin1 to swap
    :param coin1: A tuple of Name & Address, Decimals of coin to ell
    :param coin2: A tuple of Name & Address, Decimals of coin to buy
    :param slippage: Slippage tolerance in %
    :return: Dictionary with swap information
    """

    coin1_name = coin1[0].upper()
    coin1_address = coin1[1].lower()
    coin1_decimals = coin1[2]

    coin2_name = coin2[0].upper()
    coin2_address = coin2[1].lower()

    slippage = float(slippage)

    amount_decimals = int(amount * (10 ** coin1_decimals))

    inch_query = f"https://api.1inch.io/v4.0/1/quote?fromTokenAddress={coin1_address}&toTokenAddress={coin2_address}" \
                 f"&amount={amount_decimals}&slippage={slippage}"

    try:
        inch_data = requests.get(inch_query).json()

        to_token_decimal = float(inch_data['toToken']['decimals'])
        to_token_amount = float(inch_data['toTokenAmount'])
        received_amount = to_token_amount / (10 ** to_token_decimal)

        min_received_amount = received_amount - (received_amount * slippage / 100)

        rate = amount / received_amount

        return {
            'fromToken': {'name': coin1_name, 'amount': amount},
            'toToken': {'name': coin2_name, 'amount': received_amount},
            'rate': f"1 {coin2_name} = {rate} {coin1_name}",
            'min_received': min_received_amount,
        }

    except Exception as e:
        log_error.warning(f"{e}")
        return {}
