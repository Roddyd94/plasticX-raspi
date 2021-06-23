import threading
import time
from gpiozero import SmoothedInputDevice


class IRSensor(SmoothedInputDevice):
    def __init__(self, pin, *args, **kwargs):
        print("IRSensor():")
        super().__init__(pin, *args, **kwargs)

    def value(self):
        return super().value

    def run(self):
        print("run():")
        while True:
            try:
                print("Sensor:", self.value())
                time.sleep(1)
            except:
                print("run():error")
                break


def run_qr():
    print("run_qr():")
    while True:
        qr_text = input()
        print("QR:", qr_text)


class SensorThread(threading.Thread):
    def __init__(self, run):
        print("SensorThread():")
        super().__init__()
        self.run = run


def main():
    print("main():")
    ir_sensor = IRSensor(4)

    qr_thread = SensorThread(run_qr)
    ir_thread = SensorThread(ir_sensor.run)

    qr_thread.start()
    ir_thread.start()


if __name__ == '__main__':
    main()
