import MetaTrader5 as mt5

# connect to the MetaTrader 5 terminal
async def channelSignalData(currency,magic_number):
    mt5.initialize()
    # retrieve the positions with the specified magic number
    positions = mt5.positions_get(symbol=currency, magic=magic_number)
    # loop through the positions and print the relevant data
    # for position in positions:
    #     print("Symbol:", position.symbol)
    #     print("Type:", position.type)
    #     print("Entry Price:", position.price_open)
    #     print("Current Price:", position.price_current)
    # disconnect from the MetaTrader 5 terminal
    mt5.shutdown()
    return positions
