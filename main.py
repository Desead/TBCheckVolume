import statistics as st

from tinkoff.invest import Client

from lib.func import Qt
from tfdata import Token, AccountNum

TOKEN = Token.broker_full
ACCOUNT_ID = AccountNum.broker
SANDBOX = True
FIGI = 'FUTSBRF06220'
DEPTH = 50  # max = 50


def GetDepthMarket(client, figi, depth):
    r = client.market_data.get_order_book(figi=figi, depth=depth)
    ask_price = tuple(map(lambda x: Qt(x.price), r.asks))
    ask_volume = tuple(map(lambda x: x.quantity, r.asks))
    bid_price = tuple(map(lambda x: Qt(x.price), r.bids))
    bid_volume = tuple(map(lambda x: x.quantity, r.bids))

    return ask_price, ask_volume, bid_price, bid_volume


def CalcBigVolume(price, volume):
    min_volime = min(volume)
    max_volume = max(volume)
    mean = st.mean(volume)
    mediana = st.median(volume)

    print(min_volime)
    print(max_volume)
    print(mean)
    print(mediana)


def main():
    with Client(token=TOKEN) as client:
        ask_price, ask_volume, bid_price, bid_volume = GetDepthMarket(client, FIGI, DEPTH)
        print(ask_price)
        print(ask_volume)
        CalcBigVolume(ask_price, ask_volume)
        print(ask_price)
        print(ask_volume)


if __name__ == '__main__':
    main()
