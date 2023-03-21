import asyncio
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()

async def send_message_to_consumer(consumer_id, message):
    """
    Send a message to a WebSocket consumer with the specified ID.
    """
    channel_name = f"chat_{consumer_id}"
    await channel_layer.group_send(
        channel_name,
        {
            "type": "chat_message",
            "message": message
        }
    )

def send_message(consumer_id, message):
    """
    Synchronous wrapper around the send_message_to_consumer function.
    """
    asyncio.run(async_to_sync(send_message_to_consumer)(consumer_id, message))

def test():
    print('testing')
