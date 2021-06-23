import threading
import time
from urllib import request
from urllib import response
from gpiozero import LightSensor


class QRThread(threading.Thread):
    def __init__(self):
        pass

    def run(self):
        while True:
            qr_text = input()
            print("QR:", qr_text)

    def __init__(self):
        super().__init__()

    def send(self):
        #request.urlopen(f'{baseUrl}{}')
        pass


class SensorThread(threading.Thread):
    def __init__(self, run):
        super().__init__()
        self.run = run


def main():
    print("main():")
    ir_sensor = LightSensor(4)

    def run_ir():
        print("run_qr():")
        while True:
            print("IR:", ir_sensor.value)
            time.sleep(1)

    qr_thread = QRThread()
    ir_thread = SensorThread(run_ir)

    qr_thread.start()
    ir_thread.start()


if __name__ == '__main__':
    main()
