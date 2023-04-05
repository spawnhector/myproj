import os
import sys
import psycopg2
import threading
import asyncio
import websocket
import json
import websockets
from pathlib import Path
from datetime import datetime
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

current_path = Path(__file__).parent.resolve()
parent_dir = os.path.dirname(current_path)
sys.path.append(str(parent_dir))

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from trade_socket.connection import *

async def start_coroutine(loop, port):
    channel_layer = get_channel_layer()
    # await channel_layer.flush()
    try:
        await create_signal_socket(loop, port, channel_layer)
    except Exception as e:
        print(f"Error on port {port}: {e}")
    finally:
        await asyncio.sleep(0)

def start_threads():
    portEnd = 8082 + 15
    threads = []
    for i in range(8082, portEnd):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            signal_socket_thread = threading.Thread(target=loop.run_until_complete, args=(start_coroutine(loop, i),))
            signal_socket_thread.start()
            threads.append(signal_socket_thread)
        except Exception as e:
            print(f"Error in start_threads: {e}")
    for thread in threads:
        thread.join()

# currencyDataPort = 8081
# currency_data_socket_thread = threading.Thread(target=create_currency_data_socket, args=(currencyDataPort,))
# currency_data_socket_thread.start()
# threads.append(currency_data_socket_thread)
# currency_data_socket_thread.join()
if __name__ == "__main__":
    start_threads()
