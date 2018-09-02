from miner_adjuster import MinerAdjuster


class Trader:
    def __init__(self, token, pool):
        self.pool = pool
        self.market = token
        self.miner = MinerAdjuster()
        self.profit_list = {}
        self.pricelist = {}

    def update_pricelist(self):
        for key, value in self.market.fetch_tickers().items():
            if key.endswith('BTC'):
                self.pricelist[key] = value['info']['AskPrice']

    def get_profit(self):
        for coin, speed in self.pool.coin_speed.items():
            if coin + '/BTC' in self.pricelist.keys() and speed:
                self.profit_list[coin] = self.pricelist[coin + '/BTC'] * speed * 10 ** 8

    def get_deposit(self, symbol):
        return self.market.fetchDepositAddress(symbol)['address']

    def create_deposit(self, symbol):
        self.market.createDepositAddress(symbol)

    def create_bat(self, miner):
        coin = max(self.profit_list.items(), key=lambda i: i[1])[0]
        info = self.pool.coin_info
        wallet = self.get_deposit(coin)
        if not wallet:
            self.create_deposit(coin)
            wallet = self.get_deposit(coin)
        self.miner.create(miner, info[coin]['algo'], self.pool.pool_host, info[coin]['port'], wallet)
        print(f'Mining {coin}')

    def plaсe_orders(self):
        for coin, balanse in self.market.fetch_balance()['free'].items():
            if coin in self.profit_list and balanse:
                price = self.pricelist[coin + '/BTC']
                self.market.create_order(coin+'/BTC', 'limit', 'sell', balanse, price)

    def show_pricelist(self):
        print('Ask price on  market')
        for coin, price in self.pricelist.items():
            print(coin,price)

    def show_profit_list(self):
        print('Profit per hour in Satoshi')
        for coin, profit in self.profit_list.items():
            print(coin, profit)


