from Game.Game import Game
import asyncio

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    game = Game()

    try:
        asyncio.ensure_future(game.ser_io())
        asyncio.ensure_future(game.ble_io())
        loop.run_forever()
    except:
        loop.stop()
        loop.close()