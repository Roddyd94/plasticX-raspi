import threading
import time
from gpiozero import SmoothedInputDevice


class IRSensor(SmoothedInputDevice):
    def __init__(self, pin, *args, **kwargs):
        super().__init__(pin, *args, **kwargs)

    def run_sensor(self):
        while True:
            print("Sensor:", self.value())
            time.sleep(1)


def run_qr():
    while True:
        qr_text = input()
        print("QR:", qr_text)


class SensorThread(threading.Thread):
    def __init__(self, run):
        super().__init__()
        self.run = run


ir_sensor = IRSensor(4)

ir_thread = SensorThread(ir_sensor.run_sensor)
qr_thread = SensorThread(run_qr)

ir_thread.start()
qr_thread.start()
