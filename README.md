<h1>Arbitrage Screener</h1>
<h3>version 0.0.1</h3>

Screener that looks for arbitrage opportunities between 2 tokens and notifies about the spot price difference via a Telegram message.

<br> 

## Installation

This project uses **Python 3.9** and requires a
[Chromium WebDriver](https://chromedriver.chromium.org/getting-started/) installed.

<br> 

## Run script

To start screening for arbitrage:
```
var="$(cat docs/input.json)"
python3 main.py -s "$var"
```
To run in debug mode:
```
var="$(cat docs/input.json)"
python3 main.py -s "$var"
```
