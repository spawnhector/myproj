def checkMsg(msg,datetime):
    currency = False
    trade_type = ''
    trade_price = ''
    take_profit = ''

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

    return {
        'currency': currency,
        'trade_type': trade_type,
        'trade_price': trade_price,
        'take_profit': take_profit,
        'trade_date': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    }

def convertToObject(data):
    data = data.strip(',')
    data = data.split(',')
    data_dict = {}
    for item in data:
        key, value = item.split(':')
        data_dict[key] = float(value)
    return data_dict
