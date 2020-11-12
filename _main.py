# import bluetooth
# import serial

# ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
# server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

# port = 1
# server_sock.bind(("",port))
# server_sock.listen(1)

# print("In attesa di una connessione")
# client_sock,address = server_sock.accept()

# ser.write(b"BT")
# print("Connessione accetata da: ",address)

# def serial_flow():
#     serial_value = str(ser.readline())[2:-1]
#     if serial_value == str("SHOOT"):
#         print("SHOOT------------------------------------------------------------")
        
# try:
#     while True:
#         #recv = client_sock.recv(1024)
#         #print("input: ",recv)
#         #send = input()
#         #client_sock.send(str(send))
#         print("")

# except:
#     ser.write(b"BF")
#     print("Connessione scaduta")
#     client_sock.close()
#     server_sock.close()
#     ser.close()

from Game import Game
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
        game.stop()
        # shutdown raspberry