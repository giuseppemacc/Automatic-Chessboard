import asyncio
import time

class Obj():
    def __init__(self):
        self.a = [0,0]


async def ser_io(obj):
    while True:
        await asyncio.sleep(1)
        obj.a[0] += 1

async def ble_io(obj):
    while True:
        await asyncio.sleep(5)
        obj.a[1] += 1

async def state(obj):
    while True:
        await asyncio.sleep(0.1)
        print(obj.a)

if __name__ == "__main__":
    # main loop
    loop = asyncio.get_event_loop()
    
    # variabili e oggetti
    obj = Obj()

    # chiamata in loop alle funzioni I/O 
    try:
        asyncio.ensure_future(ser_io(obj))
        asyncio.ensure_future(ble_io(obj))
        asyncio.ensure_future(state(obj))
        loop.run_forever()
    except:
        loop.stop()
        # shutdown raspberry
