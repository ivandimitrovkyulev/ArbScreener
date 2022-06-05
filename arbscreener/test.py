import requests
from pprint import pprint


coin1 = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
coin2 = "0xfe9A29aB92522D14Fc65880d817214261D8479AE"
amount = 1000000000
slippage = 0.1

inch_query = f"https://api.1inch.io/v4.0/1/quote?fromTokenAddress={coin1}&toTokenAddress={coin2}" \
    f"&amount={amount}&slippage={slippage}"

inch_data = requests.get(inch_query).json()

pprint(inch_data)

toToken_decimal = float(inch_data['toToken']['decimals'])
toTokenAmount = float(inch_data['toTokenAmount'])
amount_received = toTokenAmount / (10 ** toToken_decimal)

amount_after_slippage = amount_received - (amount_received * slippage / 100)
print(amount_received)
print(amount_after_slippage)
