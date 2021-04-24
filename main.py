from Game.Game import Game
import asyncio
import os
from os import system
import time



if __name__ == "__main__":
    system("./home/pi/Utility/bluetooth_adv")
    os.chdir("/home/pi/Automatic-Chessboard")
    
    time.sleep(2)
    
    loop = asyncio.get_event_loop()
    game = Game()

    try:
        asyncio.ensure_future(game.ser_io())
        asyncio.ensure_future(game.ble_io())
        loop.run_forever()
    except:
        loop.stop()
        loop.close()