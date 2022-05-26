from statistics import median

from tinkoff.invest import Client

from lib.func import Qt
from tfdata import Token

TOKEN = Token.broker_full
FIGI = 'FUTSBRF06220'
DEPTH = 50  # max = 50
MIN_DELTA = 10  # min multiplier for find max volume


class FindBigVolumeForInstrument:
    '''
    Возвращаем список кортежей аск и бид с повышенными объёмами
    формат вывода:
        ask = [(band_num, band_price, band_volume), ]
        bid = [(band_num, band_price, band_volume), ]
    '''

    def __init__(self, client, figi, depth=50):
        self.client = client
        self.figi = figi
        self.depth = depth

    def __GetDepthMarket(self):
        r = self.client.market_data.get_order_book(figi=self.figi, depth=self.depth)
        self.ask_price = tuple(map(lambda x: Qt(x.price), r.asks))
        self.ask_volume = tuple(map(lambda x: x.quantity, r.asks))
        self.bid_price = tuple(map(lambda x: Qt(x.price), r.bids))
        self.bid_volume = tuple(map(lambda x: x.quantity, r.bids))

    def FindBigVolume(self):
        self.__GetDepthMarket()

        min_ask_volume = median(self.ask_volume) * MIN_DELTA
        min_bid_volume = median(self.bid_volume) * MIN_DELTA

        ask = [(k, self.ask_price[k], v) for k, v in enumerate(self.ask_volume) if v >= min_ask_volume]
        bid = [(k, self.bid_price[k], v) for k, v in enumerate(self.bid_volume) if v >= min_bid_volume]
        return ask, bid


def main():
    with Client(token=TOKEN) as client:
        instr = FindBigVolumeForInstrument(client, FIGI)
        ask, bid = instr.FindBigVolume()
        print(ask)
        print(bid)


if __name__ == '__main__':
    main()
