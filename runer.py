from pool_api import PoolProcessor
from time import sleep
from threading import Thread
from trade_mode import Trader
from config import *


class Runer:
    def __init__(self, trader):
        self.trader = trader
        self.pool = trader.pool
        self.miner = trader.miner
        self.threads = {}
        self.commands = {'help': self.show_commands,
                         'pool info': self.pool.show_info,
                         'pool speed': self.pool.show_speed,
                         'market prices': self.trader.show_pricelist,
                         'market profit': self.trader.show_profit_list,
                         }
        self.status = True

    def show_commands(self):
        print('pool info: show information about coins on pool\n'
              'pool speed: show mining speed coins/Gigahash per hour\n'
              'market prices: show Ask Prises on market\n'
              'market profit: show approximate profit in satoshi per hour\n'
              'stop: stopping program')

    def pool_updater(self, timeout):
        while True:
            if self.status:
                try:
                    self.pool.update_info()
                    print('pool update sucsess')
                except Exception as e:
                    print(e)
                sleep(timeout*60)

    def trader_updater(self, timeout):
        while True:
            if self.status:
                try:
                    self.trader.update_pricelist()
                    self.trader.get_profit()
                    self.trader.plaсe_orders()
                    print('trader update sucsess')
                except Exception as e:
                    print(e)
                sleep(timeout*60)

    def work_miner(self, miner, timeout):
        while True:
            if self.status:
                try:
                    self.miner.stop()
                    self.trader.create_bat(miner)
                    self.miner.run()
                    print('miner update sucsess')
                except Exception as e:
                    print(e)
                sleep(timeout*60)

    def listen_comands(self):
        while True:
            if self.status:
                command = input()
                if command in self.commands.keys():
                    self.commands[command]()
                else:
                    print('wrong command')

    def run(self):
        pool_timeout = int(input('pool time interval'))
        trader_timeout = int(input('trader time interval'))
        miner_timeout = int(input('miner time interval'))
        pt = Thread(target=self.pool_updater, args=(pool_timeout,))
        tt = Thread(target=self.trader_updater, args=(trader_timeout,))
        mt = Thread(target=self.work_miner, args=(MINER, miner_timeout))
        lc = Thread(target=self.listen_comands)
        pt.start()
        tt.start()
        lc.start()
        sleep(15)
        mt.start()
        self.threads.update([('pool', pt), ('trader', tt), ('miner', mt)])

    def stop(self):
        self.status = False


if __name__ == '__main__':
    pool = PoolProcessor('http://api.bsod.pw/api/currencies', 'stratum+tcp://eu.bsod.pw')
    trader = Trader(TOKEN, pool)
    program = Runer(trader)
    program.run()
