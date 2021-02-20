from binance.client import Client
import json
import datetime
api_key = 'XXXXXXXXXXXXXXX'
api_secret = 'XXXXXXXXXXXXXX'
client = Client(api_key, api_secret)

class Event(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.TargetObject = None
        if self.e == 'kline':
            self.TargetObject = Kline(**(kwargs["k"]))

class Kline(object):
    def __init__(self, **kwargs):

#{'e': 'kline', 'E': 1613751802137, 's': 'BNBUSDT','k': {'t': 1613750400000, 'T': 1613752199999, 's': 'BNBUSDT',
# 'i': '30m', 'f': 138510317, 'L': 138574854, 'o': '311.78990000', 'c': '309.05960000', 'h': '317.90000000', 'l': '299.43800000',
# 'v': '292645.72100000', 'n': 64538, 'x': False, 'q': '90322489.31057840', 'V': '140859.50600000','Q': '43570112.95141780', 'B': '0'}
        self.__dict__.update(kwargs)
        self.IslemTarihi = datetime.datetime.fromtimestamp(self.t / 1000)

KlineBefore: Kline = None

from binance.websockets import BinanceSocketManager
from binance.enums import *
def process_message(msg):
    global KlineBefore
    #print(msg)
    event = Event(**msg)
    if type(event.TargetObject) is Kline:
        KlineObj = event.TargetObject
        if KlineBefore != None:
            if KlineObj.c > KlineBefore.c:
                print(f"{KlineObj.IslemTarihi} +++ UP {KlineBefore.c} - {KlineObj.c} - Volume: {KlineObj.v}")
            elif KlineObj.c == KlineBefore.c:
                print(f"{KlineObj.IslemTarihi} === EQ {KlineBefore.c} - {KlineObj.c} - Volume: {KlineObj.v}")
            else:
                print(f"{KlineObj.IslemTarihi} --- DOWN {KlineBefore.c} - {KlineObj.c} - Volume: {KlineObj.v}")
        KlineBefore = KlineObj


bm = BinanceSocketManager(client,user_timeout=60)
conn_key = bm.start_kline_socket('BNBUSDT', process_message, interval=KLINE_INTERVAL_1HOUR)
bm.start()













