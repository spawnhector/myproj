import os
import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(ROOT_DIR / "config"))
sys.path.append(str(ROOT_DIR / "myproj"))

# from schannels.models import SChannel
# from responder import test

import psycopg2
import threading
import socket
import asyncio
import json
import websockets
from datetime import datetime
from asgiref.sync import async_to_sync

class RateLimiter:
    def __init__(self, rate, per):
        self.rate = rate
        self.per = per
        self.tokens = rate
        self.last_check = None

    async def acquire(self):
        now = asyncio.get_event_loop().time()
        if self.last_check is not None:
            elapsed = now - self.last_check
            self.tokens += elapsed * (self.rate / self.per)
            self.tokens = min(self.tokens, self.rate)
        self.last_check = now
        if self.tokens < 1:
            await asyncio.sleep((1 - self.tokens) * self.per)
            self.tokens = 1
        else:
            self.tokens -= 1

async def echo(websocket, path):
    rate_limiter = RateLimiter(10, 1) # 10 messages per second
    async for message in websocket:
        await rate_limiter.acquire()
        await websocket.send(message)

currencyDataFile = "trade_socket/currencyData.txt"
HOST = socket.gethostbyname('trade_socket_server')
def get_connection():
    try:
        return psycopg2.connect(
            database="myproj",
            user="MPYzyNUJMZCyzCVdzvItYfIBzoXODgUT",
            password="rpc99B22yoHZJgHczZXxV5uyZDpekj0j6vVsx444xPEMUmJAXSieiGrhbSGVCino",
            host="postgres", port="5432"
        )
    except:
        return False

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
            updateTradeDataBase(msg)
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

file = Path(__file__). resolve()
package_root_directory = file.parents [1]
sys.path.append(str(package_root_directory))

# from trade_socket.connection import *
from trade_socket.commands import *
from trade_socket.pairList import *
from trade_socket.query import *
from trade_socket.functions import *

conn = None
# create tables
conn = get_connection()
if conn:
    createTables(get_connection,psycopg2,commands())
else:
    print("Connection to the PostgreSQL encountered and error.")

# insert pairs
conn = get_connection()
if conn:
    insertPairs(get_connection,psycopg2,pair_list())
else:
    print("Connection to the PostgreSQL encountered and error.")

def getSignals():
    conn = get_connection()
    if conn:
        return tradeSignal(get_connection)
    else:
        return {
            'error': "Connection to the PostgreSQL encountered and error.",
        }

async def socketAction(websocket, path):
    # rate_limiter = RateLimiter(10, 1) # 10 messages per second
    async for message in websocket:
        if not message:
            break
        with open(currencyDataFile, "r") as file:
            contents = file.read()
            data = json.dumps({
                'pairs': getSignals(),
                'currencyData': convertToObject(contents)
            })
            # await rate_limiter.acquire()
            await websocket.send(data)

def create_web_socket(port):
    start_server = websockets.serve(socketAction, HOST, port)
    print(f"websocket created and waiting on host: {HOST} port: {port}")
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

def updateTradeDataBase(msg):
    result = checkMsg(msg,datetime)
    if result['currency']:
        row = getPair(get_connection,psycopg2,result['currency'])
        if row:
            pair_id,pair_symbol = row
            insertSignals(get_connection,psycopg2,pair_id,result)
        else:
            print("Connection to the PostgreSQL encountered and error.")


# Create socket connection for signals
portEnd = 8082 + len(pair_list())
for i in range(8082, portEnd):
    signal_socket_thread = threading.Thread(target=create_signal_socket, args=(i,))
    signal_socket_thread.start()

# Create socket connection for currency data
currencyDataPort = 8081
currency_data_socket_thread = threading.Thread(target=create_currency_data_socket, args=(currencyDataPort,))
currency_data_socket_thread.start()

# Create websocket connection for frontend communication
websocketPort = 8080
create_web_socket(websocketPort)
# client_websocket_thread = threading.Thread(target=create_web_socket, args=(websocketPort,))
# client_websocket_thread.start()
