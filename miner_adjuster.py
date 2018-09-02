import os
from subprocess import Popen
from time import sleep
import os

class MinerAdjuster:
    def __init__(self):
        self.process = None

    @staticmethod
    def create(miner, algo, pool, port, wallet):
        text = f'{miner} -a {algo} -o {pool}:{port} -u {wallet}'
        with open('new.bat', 'tw', encoding='utf-8') as file:
            file.write(text)
            file.close()

    def run(self):
        if not self.process:
            process = Popen('new.bat')
            self.process = process

    def stop(self):
        if self.process:
            self.process.kill()
            #os.killpg(process.pid, signal.SIGKILL)



