import asyncio
import time

class Obj():
    def __init__(self):
        self.a = [0,0]
        self.reload = False
        time.sleep(5)
        print("OK")


async def ser_io(obj):
    while True:
        try:
            await asyncio.sleep(1)
            obj.a[0] += 1
            if obj.a[0] == 6:
                print(1/0)
        except:
            obj.reload = True
            obj.__init__()
            #break
            

async def ble_io(obj):
    while True:
        try:
            await asyncio.sleep(5)
            obj.a[1] += 1
            # if obj.a[1] == 3:
            #     print(1/0)
        except:
            obj.reload = True
            break

async def state(obj):
    while True:
        if not obj.reload:
            await asyncio.sleep(0.1)
            print(obj.a)
        else:
            print("ERRORE")
            break

if __name__ == "__main__":
    # main loop
    # loop = asyncio.get_event_loop()
    
    # # variabili e oggetti
    # obj = Obj()

    # # chiamata in loop alle funzioni I/O 
    # try:
    #     asyncio.ensure_future(ser_io(obj))
    #     asyncio.ensure_future(ble_io(obj))
    #     asyncio.ensure_future(state(obj))
    #     loop.run_forever()
    # except:
    #     loop.stop()
        # shutdown raspberry

    try:
        print(1/0)
    except:
        pass
    try:
        print(2)
    except:
        pass
    try:
        print(1/0)
    except:
        pass
    try:
        print(9)
    except:
        pass