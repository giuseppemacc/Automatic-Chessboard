from picamera import PiCamera
from time import sleep

def shoot():
    c = PiCamera()
    c.start_preview()
    sleep(0.5)
    c.capture("image/shoot.jpg")
    c.stop_preview()