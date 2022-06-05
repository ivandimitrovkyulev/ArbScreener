from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    WebDriverException,
    TimeoutException
)

from .logger import log_error


def wait_history_table(
        driver: Chrome,
        element_name: str,
        wait_time: int = 30,
        max_wait_time: int = 50,
        infinite: bool = False,
) -> None:
    """
    Waits infinitely for the presence of a HTML element located by its name.

    :param driver: Web driver instance
    :param element_name: Element name to search for
    :param wait_time: Seconds to wait before refreshing
    :param max_wait_time: Max seconds to wait before refreshing
    :param infinite: If True re-tries infinitely to retrieve response, default False
    :returns: None
    """

    while True:
        try:
            WebDriverWait(driver, wait_time).until(ec.presence_of_element_located(
                (By.CLASS_NAME, element_name)))

        except WebDriverException or TimeoutException:
            # Refresh page and log error
            driver.refresh()
            log_error.warning(f"Error while loading page.")

            # If query infinitely continue loop
            if infinite:
                continue

            # If no response is returned break
            if wait_time >= max_wait_time:
                # wait_time = max_wait_time
                break

            # Wait for longer periods
            wait_time += 10

        # If response returned - break
        else:
            break
