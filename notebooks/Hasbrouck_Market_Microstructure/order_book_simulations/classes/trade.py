"""
This class contains the trades details, like the price, the volume and the direction (buy/sell).
It can be furtherly expanded with attributes like the order id and the trader that submitted the order. 

The order becomes a trade if it is executed. 
"""
class Trade():
    def __init__(self, price, volume, direction, 
                 trader_id_already_in_book,
                 trader_id_coming_in_book,
                 order_id_already_in_book,
                 order_id_coming_in_book):
        self.price = price
        self.volume = volume
        self.direction = direction
        self.trader_id_already_in_book = trader_id_already_in_book
        self.trader_id_coming_in_book = trader_id_coming_in_book
        self.order_id_already_in_book = order_id_already_in_book
        self.order_id_coming_in_book = order_id_coming_in_book
        