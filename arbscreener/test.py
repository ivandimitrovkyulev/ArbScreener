import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

driver = webdriver.Chrome(
    executable_path="./chromedriver.exe"
)
# Designating which site to open to
driver.get("https://matcha.xyz/markets/1/0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2/0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48")
# Pausing for a second
time.sleep(1)
# Typing into search and hitting enter
driver.find_element_by_xpath(
    "//input[@class='Input__StyledInput-jrcd0l-0 MarketPairEntrypoint__PrimaryInput-y3jjai-0 itcvxa oBMLO']"
).send_keys(
    "100000",
    Keys.ENTER
)

time.sleep(5)

checkbox = driver.find_element_by_id(
    "rfqm-switch"
)

driver.execute_script("arguments[0].click();", checkbox)

for i in range(0,100):
    x = driver.find_element_by_xpath("//*[@id='trading-page-container']/div[2]/div/div/aside/div[1]/div/div/div[6]/div[3]/div[2]/input").get_attribute("value")
    print(x)
    time.sleep(1)

# Pausing again
time.sleep(10)
# Closing the browser
driver.quit()