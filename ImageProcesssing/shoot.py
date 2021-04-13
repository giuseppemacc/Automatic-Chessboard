from picamera import PiCamera
from time import sleep

c = PiCamera()
c.start_preview()
def shoot():
    sleep(0.2)
    c.capture("image/shoot.jpg")
    #c.stop_preview()