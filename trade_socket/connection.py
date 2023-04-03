import socket
from trade_socket.functions import *

HOST = socket.gethostbyname('trade_socket_server')
currencyDataFile = "trade_socket/currencyData.txt"

async def create_signal_socket(loop, port, channel_layer):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print("socket creation failed with error %s" %(err))
    try:
        print(f"[INFO]\listen for signals on {HOST}:{port} \n")
        s.bind((HOST, port))
        s.listen()
        connection, addr = s.accept()
        print("[INFO]\Connection establish with signal server on :", addr)
        msg = ""
        while not "END CONNECTION\0" in msg:
            msg = connection.recv(1024).decode()
            if not msg:
                break
            await messageAction(connection,channel_layer,msg)
        connection.close()
    except socket.error:
        print("there was an error resolving the host")
        sys.exit()

def create_currency_data_socket(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print("socket creation failed with error %s" %(err))
    try:
        print(f"[INFO]\listen for currency data on {HOST}:{port} \n")
        s.bind((HOST, port))
        s.listen()
        connection, addr = s.accept()
        print("[INFO]\Connection establish with currency data server on :", addr)
        msg1 = ""
        while not "END CONNECTION\0" in msg1:
            msg1 = connection.recv(1024).decode()
            if not msg1:
                    break
            with open(currencyDataFile, "w") as file:
                file.write(msg1)
        connection.close()
        s.close()
    except socket.error:
        print("there was an error resolving the host")
        sys.exit()
