import os
import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(ROOT_DIR / "config"))
sys.path.append(str(ROOT_DIR / "myproj"))

import psycopg2
import threading
import socket
import asyncio
import websocket
import json
import websockets
from datetime import datetime
from asgiref.sync import async_to_sync

HOST = socket.gethostbyname('trade_socket_server')
currencyDataFile = "trade_socket/currencyData.txt"

def sendData(data):
    websocket.enableTrace(True)
    ws = websocket.WebSocket()
    ws.connect("ws://172.18.0.6:8000/ws/test_signals/ALL/trade_socket/?token=a02b74b5994a2fd776f19911272266623f87b569049dccee4a96453e606a3909")
    if ws.connected:
        channelData = {'server_name': 'trade_socket','data':data}
        message = json.dumps(channelData)
        ws.send(message)
    else:
        ws.close()
def create_signal_socket(port):
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
            sendData(msg)
        connection.close()
        s.close()
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

# Create socket connection for signals
portEnd = 8082 + 15
for i in range(8082, portEnd):
    signal_socket_thread = threading.Thread(target=create_signal_socket, args=(i,))
    signal_socket_thread.start()

# Create socket connection for currency data
currencyDataPort = 8081
currency_data_socket_thread = threading.Thread(target=create_currency_data_socket, args=(currencyDataPort,))
currency_data_socket_thread.start()
