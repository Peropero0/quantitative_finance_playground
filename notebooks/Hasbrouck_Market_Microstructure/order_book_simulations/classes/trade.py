"""
This class contains the trades details, like the price, the volume and the direction (buy/sell).
It can be furtherly expanded with attributes like the order id and the trader that submitted the order. 

The order becomes a trade if it is executed. 
"""
class Trade():
    def __init__(self, price, volume, direction):
        self.price = price
        self.volume = volume
        self.direction = direction
        # you can add trade id and trader id