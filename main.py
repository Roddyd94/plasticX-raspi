import threading
import sys
import time
from urllib import request
from urllib import parse
import json
import env
import smbus
from gpiozero import TonalBuzzer
from gpiozero.tones import Tone

class QRThread(threading.Thread):
    def __init__(self, config):
        super().__init__()
        self.id = config.id if config else env.id
        self.baseUrl = config.baseUrl if config else env.baseUrl
        self.path = config.pathTumbler if config else env.pathTumbler
        self.buzzer = TonalBuzzer(env.pin_buzz)

    def run(self):
        while True:
            qr_text = input()
            self.send(qr_text)

    def send(self, id='60d2c06885142b1264c81cb7'):
        print(id)
        data = parse.urlencode({'to_id': self.id})
        req = request.Request(f'{self.baseUrl}{self.path}{id}', data=bytes(data, 'UTF-8'), method='PUT')
        try:
            with request.urlopen(req) as response:
                res = json.loads(response.read().decode('utf-8'))
                if res['RESULT'] == 401:
                    print('Invalid QR Code')
                    self.buzzer.play(Tone("G4"))
                    time.sleep(0.4)
                    self.buzzer.stop()
                    time.sleep(0.2)
                    self.buzzer.play(Tone("G4"))
                    time.sleep(0.4)
                    self.buzzer.stop()
                elif res['RESULT'] == 200:
                    print('Tumbler Returned')
                    self.buzzer.play(Tone("C5"))
                    time.sleep(0.2)
                    self.buzzer.play(Tone("E5"))
                    time.sleep(0.2)
                    self.buzzer.play(Tone("G5"))
                    time.sleep(0.4)
                    self.buzzer.stop()
                else:
                    print(res)
                    self.buzzer.play(Tone("G4"))
                    time.sleep(1)
                    self.buzzer.stop()
        except:
            print(sys.exc_info()[0])

class I2CThread(threading.Thread):
    def __init__(self, config):
        super().__init__()
        self.id = config.id if config else env.id
        self.baseUrl = config.baseUrl if config else env.baseUrl
        self.path = config.pathReturnBoxUpdate if config else env.pathReturnBoxUpdate
        self.addr = config.addr if config else env.addr
        self.bus = smbus.SMBus(config.bus if config else env.bus)
        self.buf = [0,0,0,0,0,0,0,0,0,0]
        self.state = False

    def run(self):
        while True:
            for i in range(len(self.buf)):
                self.bus.write_i2c_block_data(self.addr, 0, [0x40])
                self.buf[i] = self.bus.read_i2c_block_data(self.addr, 0, 2)[1]
            adc = sum(self.buf) / len(self.buf)
            print(adc)
            if adc < 90 and self.state == False:
                self.state = True
                self.send(True)
            elif adc > 110 and self.state == True:
                self.state = False
                self.send(False)
            time.sleep(0.1)

    def send(self, is_full):
        print(f'ReturnBox {self.id} is ' + ('full' if is_full else 'not full'))
        data = parse.urlencode({'isWorking': 'true' if is_full else 'false'})
        req = request.Request(f'{self.baseUrl}{self.path}{self.id}', data=bytes(data, 'UTF-8'), method='PUT')
        try:
            with request.urlopen(req) as response:
                res = json.loads(response.read().decode('utf-8'))
                print(res)
        except:
            print(sys.exc_info()[0])


def main():
    print("main():")

    qr_thread = QRThread(env)
    ir_thread = I2CThread(env)

    qr_thread.start()
    ir_thread.start()
    while True:
        #qr_thread.send()
        data = parse.urlencode({'isConnected': 'true'})
        req = request.Request(f'{env.baseUrl}{env.pathReturnBoxUpdate}{env.id}', data=bytes(data, 'UTF-8'), method='PUT')
        try:
            with request.urlopen(req) as response:
                res = json.loads(response.read().decode('utf-8'))
                print(res)
        except:
            print(sys.exc_info()[0])
        time.sleep(600)



if __name__ == '__main__':
    main()
