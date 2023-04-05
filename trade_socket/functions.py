channel_name = "hectper_scalper"

from myproj.schannels.models import SChannel
from myproj.signals.models import Signals
from myproj.users.api.serializers import ChannelSerializer
from myproj.users.api.serializers import SignalsSerializer
from channels.db import database_sync_to_async

def checkMsg(msg,datetime):
    currency = False
    trade_type = ''
    trade_price = ''
    take_profit = ''
    trade_ticket = ''

    x = msg.split(",")
    for signal in x:
        xy = signal.split(':')
        if xy[0] == 'currency':
            currency = xy[1]
        if xy[0] == 'trade_type':
            trade_type = xy[1]
        if xy[0] == 'trade_price':
            trade_price = xy[1]
        if xy[0] == 'take_profit':
            take_profit = xy[1]
        if xy[0] == 'trade_ticket':
            trade_ticket = xy[1]

    return {
        'currency': currency,
        'trade_type': trade_type,
        'trade_price': trade_price,
        'take_profit': take_profit,
        'trade_date': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
        'trade_status': 'Open',
        'trade_ticket': trade_ticket
    }

def convertToObject(data):
    data = data.strip(',')
    data = data.split(',')
    data_dict = {}
    for item in data:
        if not item:
            break
        key, value = item.split(':')
        data_dict[key] = float(value)
    return data_dict

async def send_message_to_group(channel_layer,group_name, message):
    try:
        await channel_layer.group_send(group_name, {
            'type': 'updated_signal',
            'message': message
        })
    except Exception as e:
        print(f"Error sending message to channel: {e}")

async def create_signal_channel_group(channel_layer,group_name):
    group_exists = await channel_layer.is_group_exists(group_name)
    if not group_exists:
        try:
            # Create a new channel with the custom channel name

            print(f"created new channel for: {group_name}")
            channel = await channel_layer.new_channel()
            await channel_layer.group_add(group_name, channel)
        except Exception as e:
            print(f"Error creating signal channel: {e}")
            return False
        return True
    return True

def handleData(message):
    _message = eval(message)
    if _message['trade_status'] == 'Open':
        return addChannelSignals(_message)
    elif _message['trade_status'] == 'Close':
        return updateChannelSignals(_message)

async def messageAction(connection,channel_layer,msg):
    message = eval(msg)
    group_name = "signals_%s" % message['currency']
    if message['type'] == 'init':
        if not await create_signal_channel_group(channel_layer,group_name):
            # error creating group
            connection.send(b"error creating signal group")
        else:
            # get group settings
            connection.send(b"signal group created.")
    elif message['type'] == 'signal':
        resultData = await database_sync_to_async(handleData)(msg)
        await send_message_to_group(channel_layer,group_name, resultData)


def addChannelSignals(message):
    channel_by_name = SChannel.objects.get(channel_name=message['currency'])
    if channel_by_name:
        result_id = channel_by_name.id
        app_channel = SChannel(id=result_id)
        signal = Signals.objects.add_signal(result_id,message)
        app_channel.signals.add(signal.id)
        app_channels = ChannelSerializer(channel_by_name)
        return app_channels.data

def updateChannelSignals(message):
    print('signal updated')
    channel_by_name = SChannel.objects.get(channel_name=message['currency'])
    if channel_by_name:
        signal_by_ticket = Signals.objects.get(magic_number=message['magic'])
        if signal_by_ticket:
            signal_by_ticket.trade_status = message['trade_status']
            signal_by_ticket.save()
        app_channels = ChannelSerializer(channel_by_name)
        return app_channels.data

