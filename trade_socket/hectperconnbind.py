import psycopg2
import threading
import socket
import asyncio
import websockets
from datetime import datetime

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

async def socketAction(websocket, path):
    print('getting message')
    async for message in websocket:
        print(f'Received: {message}')
        await websocket.send(message)

def create_web_socket(port):
    start_server = websockets.serve(socketAction, HOST, port)
    print(f"websocket created and waiting on host: {HOST} port: {port}")
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

def create_socket(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print("socket creation failed with error %s" %(err))

    try:
        print(f"[INFO]\listen on host {HOST} {port} \n")
        s.bind((HOST, port))
        s.listen()
        connection, addr = s.accept()
        print("[INFO]\Connection establish with:", addr)
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

import sys
from pathlib import Path
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

def updateTradeDataBase(msg):
    result = checkMsg(msg,datetime)
    if result['currency']:
        row = getPair(get_connection,psycopg2,result['currency'])
        if row:
            pair_id,pair_symbol = row
            insertSignals(get_connection,psycopg2,pair_id,result)


# Create socket connection
portEnd = 8081 + len(pair_list())
for i in range(8081, portEnd):
    client_socket_thread = threading.Thread(target=create_socket, args=(i,))
    client_socket_thread.start()

# Create websocket connection
websocketPort = 8080
create_web_socket(websocketPort)
# client_websocket_thread = threading.Thread(target=create_web_socket, args=(websocketPort,))
# client_websocket_thread.start()
