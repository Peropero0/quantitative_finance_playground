"""
This class contains the trades details, like the price, the volume and the direction (buy/sell).
The order becomes a trade if it is executed. 
"""
class Trade():
    def __init__(self, price, volume, direction, 
                 trader_id_already_in_book,
                 trader_id_coming_in_book,
                 order_id_already_in_book,
                 order_id_coming_in_book):
        
        # price of the trade
        self.price = price

        # volume of the trade
        self.volume = volume

        # direction of the trade (buy/sell)
        self.direction = direction

        # id of trader that already has his order in the book (a limit order)
        self.trader_id_already_in_book = trader_id_already_in_book

        # id of trader that is entering the order in the book (it can be mkt or limit)
        self.trader_id_coming_in_book = trader_id_coming_in_book

        # id of order already in the book, the limit order
        self.order_id_already_in_book = order_id_already_in_book

        # id of the order that has been issued and is being matched with the order already in the book
        self.order_id_coming_in_book = order_id_coming_in_book
        