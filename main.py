from gpiozero import SmoothedInputDevice

sensor_ir = SmoothedInputDevice(2)

while True:
    print("Sensor:", sensor_ir.value())
    qr_text = input()
    print("QR:", qr_text)
