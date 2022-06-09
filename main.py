import os
import sys
import json

from atexit import register
from datetime import datetime
from pprint import pprint

from src.arbscreener import (
    exit_handler_driver,
    chrome_driver,
    scrape_prices,
    time_format,
    parser,
    args
)


if len(sys.argv) < 2:
    sys.exit(parser.print_help())

if args.debug:
    debugging = args.debug[0]
else:
    debugging = False

# Send telegram debug message if program terminates
program_name = os.path.abspath(os.path.basename(__file__))
register(exit_handler_driver, chrome_driver, program_name)
timestamp = datetime.now().astimezone().strftime(time_format)

input_dict = json.loads(sys.argv[-1])

coin_1 = tuple(input_dict['coin1'].values())
coin_2 = tuple(input_dict['coin2'].values())
slippage_perc = input_dict['settings']['slippage_perc']

print(f"{timestamp}\n"
      f"\tStarted arbitrage screening with the following settings:\n"
      f"\t{coin_1[0]}/{coin_2[0]} and {coin_2[0]}/{coin_1[0]}\n"
      f"\thttps://matcha.xyz --> https://app.1inch.io\n"
      f"\thttps://app.1inch.io --> https://matcha.xyz\n")
pprint(input_dict, indent=4)

# Scrape prices for arbitrage opportunity and notify
scrape_prices(driver=chrome_driver, coin1=coin_1, coin2=coin_2, slippage=slippage_perc, debug=debugging)
