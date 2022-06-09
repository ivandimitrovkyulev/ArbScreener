<h1>Arbitrage Screener</h1>
<h3>version 0.1.0</h3>

Screener that looks for arbitrage opportunities between 2 tokens and notifies about the spot price difference via a Telegram message.

<br> 

## Installation

This project uses **Python 3.9** and requires a
[Chromium WebDriver](https://chromedriver.chromium.org/getting-started/) installed.

Clone the project:
```
git clone https://github.com/ivandimitrovkyulev/ArbScreener.git

cd ArbScreener
```

This project uses poetry as a distribution package. To install poetry:
```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

To install project dependencies and activate a virtual env with poetry:
```
poetry install

poetry shell
```

You will also need to save the following variables in a **.env** file in ./ArbScreener:
```
CHROME_LOCATION=<your/web/driver/path/location> 

TOKEN=<telegram-token-for-your-bot>

CHAT_ID_ALERTS=<id-of-telegram-chat-for-alerts>

CHAT_ID_DEBUG=<id-of-telegram-chat-for-debugging>

```
<br/>

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

<br/>

## Docker deployment
<br/>

Build a docker image named **arbscreener**:
Inside the ./ArbScreener directory run:
```
docker build . -t <image-name>
```
Run docker container:
```
var="$(cat docs/input.json)"

docker run --shm-size="2g" -it <image-id> python3 main.py <mode> "$var"  
```

where **--shm-size="2g"** docker argument is provided to prevent Chromium from the **"from tab crashed"** error.

<br/>

Email: ivandkyulev@gmail.com