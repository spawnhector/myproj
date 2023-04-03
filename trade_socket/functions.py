channel_name = "hectper_scalper"

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
    # await channel_layer.flush()
    group_exists = await channel_layer.is_group_exists(group_name)
    if not group_exists:
        try:
            # Create a new channel with the custom channel name
            channel = await channel_layer.new_channel(channel_name)
            await channel_layer.group_add(group_name, channel)
        except Exception as e:
            print(f"Error creating signal channel: {e}")
            return False
        return True
    return True

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
        await send_message_to_group(channel_layer,group_name, msg)

def sendData(data):
    pass
    # websocket.enableTrace(True)
    # ws = websocket.WebSocket()
    # ws.connect("ws://172.18.0.6:8000/ws/test_signals/ALL/trade_socket/?token=a02b74b5994a2fd776f19911272266623f87b569049dccee4a96453e606a3909")
    # if ws.connected:
    #     channelData = {'server_name': 'trade_socket','data':data}
    #     message = json.dumps(channelData)
    #     ws.send(message)
    # else:
    #     ws.close()
