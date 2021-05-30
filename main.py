import threading
from gpiozero import SmoothedInputDevice


class IRSensor(SmoothedInputDevice):
    def __init__(self, pin, *args, **kwargs):
        super().__init__(pin, *args, **kwargs)

    def run(self):
        while True:
            print("Sensor:", self.value())


def run_qr():
    while True:
        qr_text = input()
        print("QR:", qr_text)


class SensorRunner(threading.Thread):
    def __init__(self, run):
        super().__init__()
        self.run = run


ir_sensor = IRSensor(4)

SensorRunner(ir_sensor.run)
SensorRunner(run_qr)
