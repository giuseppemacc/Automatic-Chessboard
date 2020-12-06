from picamera import PiCamera
from time import sleep

c = PiCamera()
c.start_preview()
def shoot():
    sleep(0.5)
    c.capture("image/shoot.jpg")
    #c.stop_preview()