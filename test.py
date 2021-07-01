import threading
import time
from urllib import request
from urllib import parse
#from urllib import response
import env
import smbus
from gpiozero import LightSensor


class QRThread(threading.Thread):
    def __init__(self, config):
        super().__init__()
        self.id = config.id if config else env.id
        self.baseUrl = config.baseUrl if config else env.baseUrl
        self.path = config.pathTumbler if config else env.pathTumbler

    def run(self):
        while True:
            qr_text = input()
            self.send(qr_text)

    def send(self, id='60d2c06885142b1264c81cb7'):
        print(id)
        data = parse.urlencode({'to_id': self.id, 'state': 'false'})
        req = request.Request(f'{self.baseUrl}{self.path}{id}', data=bytes(data, 'UTF-8'), method='PUT')
        with request.urlopen(req) as response:
            res = response.read()
            print(res)


class I2CThread(threading.Thread):
    def __init__(self, config):
        super().__init__()
        self.id = config.id if config else env.id
        self.baseUrl = config.baseUrl if config else env.baseUrl
        self.path = config.pathReturnBoxUpdate if config else env.pathReturnBoxUpdate
        self.addr = config.addr if config else env.addr
        self.bus = smbus.SMBus(config.bus if config else env.bus)
        self.buf = [0,0,0,0,0,0,0,0,0,0]

    def run(self):
        while True:
            for i in range(len(self.buf)):
                self.bus.write_i2c_block_data(self.addr, 0, [0x40])
                self.buf[i] = self.bus.read_i2c_block_data(self.addr, 0, 2)[1]
            adc = sum(self.buf) / len(self.buf)
            if adc > 110:
                self.send(False)
            elif adc < 100:
                self.send(True)
            time.sleep(10)

    def send(self, is_full):
        print(f'ReturnBox {self.id} is ' + ('full' if is_full else 'not full'))
        data = parse.urlencode({'isFull': 'true' if is_full else 'false', 'isWorking': 'true'})
        req = request.Request(f'{self.baseUrl}{self.path}{self.id}', data=bytes(data, 'UTF-8'), method='PUT')
        with request.urlopen(req) as response:
            res = response.read()
            print(res)


def main():
    print("main():")

    qr_thread = QRThread(env)
    ir_thread = I2CThread(env)

    qr_thread.start()
    ir_thread.start()
    while True:
        #qr_thread.send()
        time.sleep(5)



if __name__ == '__main__':
    main()
