import requests


class PoolProcessor:
    def __init__(self, pool_coin_api, pool_host):
        self.pool_host = pool_host
        self.pool_coin_api = pool_coin_api
        self.coin_info = {}
        self.coin_speed = {}

    def update_info(self):
        self.coin_info = requests.get(self.pool_coin_api).json()
        for coin, info in self.coin_info.items():
            if info['hashrate'] and info['difficulty']:
                full_hashrate =(info['network_hashrate'] + info['hashrate'])
                avg_block_time = info['difficulty'] / full_hashrate * 10 ** 10
                avg_coins_per_hour = 3600 / avg_block_time * float(info['reward'])
                coins_per_ghash = (full_hashrate * 10 ** -9) / avg_coins_per_hour
                self.coin_speed[coin] = round(coins_per_ghash, 10)
            else:
                self.coin_speed[coin] = 0

    def show_info(self):
        for coin, info in self.coin_info.items():
            print(coin)
            for key, walue in info.items():
                print('     ', key, walue)

    def show_speed(self):
        print('speed = coins/Gigahash per hour')
        for coin, speed in self.coin_speed.items():
            if speed:
                print(coin, speed)



