import json
import sys


input_dict = json.loads(sys.argv[-1])

coin_1 = tuple(input_dict['coin1'].values())
coin_2 = tuple(input_dict['coin2'].values())

print(coin_1)
print(coin_2)