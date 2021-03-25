#!/usr/bin/python
import config as cfg
import websocket
import json
from os import system, name
from termcolor import colored
from pyfiglet import figlet_format

last_price = -1
ticker = ''


def on_message(ws, message):
    try:
        message = json.loads(message)
        price = message['data'][0]['p']
        clear()
        if last_price > price:
            print(colored(figlet_format(ticker + '\t'+price), color="red"))
        else:
            print(colored(figlet_format(price), color="green"))
    except:
        pass


def on_error(ws, error):
    print(error)
    exit()


def on_open(ws):
    ws.send('{"type":"subscribe","symbol":"'+ticker+'"}')


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def main():
    ticker = input("Ticker: ")
    key = cfg.keys["finnhub"]
    system('setterm -cursor off')
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=" + key,
                                on_message=on_message,
                                on_error=on_error)
    ws.on_open = on_open
    ws.run_forever()


if __name__ == "__main__":
    main()