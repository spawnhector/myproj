import psycopg2
import socket
from datetime import datetime

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

# HOST = '127.0.0.1'
HOST = socket.gethostbyname('trade_socket_server')
PORT = 8080        # Port to listen on (non-privileged ports are > 1023)

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
    print("socket creation failed with error %s" %(err))

try:
    print("[INFO]\listen on host ", HOST)
    s.bind((HOST, PORT))
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

