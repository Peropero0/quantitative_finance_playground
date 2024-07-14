from order import Order
from prettytable import PrettyTable
import numpy as np

class OrderBook:

    def __init__(self):
        self.bids = []  # list of (price, quantity)
        self.asks = []  # list of (price, quantity)
        self.transactions_log = [] # list of (time, order_type, price, quantity)
        self.price_mid = []
        self.price_weighted = []
        self.bid_ask_spread = []
        

    def execute_market_order(self, quantity, order_type):
        # execute a market order, getting the first available ask if buying
        # and the first available bid if selling
        # if the first available book level is not sufficient to execute the
        # whole trade, the next level is used 

        if order_type == 'market_buy':
            # market buy
            try:
                best_available_ask_price, best_available_ask_quantity = self.asks.pop(0)
            except Exception:
                # ask is empty
                return
            
            if quantity >= best_available_ask_quantity:
                self.execute_market_order(quantity - best_available_ask_quantity, 'market_buy')
            else:
                self.asks.append((best_available_ask_price, best_available_ask_quantity - quantity))
                self.asks.sort(key=lambda x: x[0])

        elif order_type == 'market_sell':
            # market sell
            try:
                best_available_bid_price, best_available_bid_quantity = self.bids.pop(0)
            except Exception:
                # bid is empty
                return
            if quantity >= best_available_bid_quantity:
                self.execute_market_order(quantity - best_available_bid_quantity, 'market_sell')
            else:
                self.bids.append((best_available_bid_price, best_available_bid_quantity - quantity))
                self.bids.sort(key=lambda x: x[0], reverse=True)
    
    @staticmethod
    def find_order_with_certain_price(order_book, price):
        for index, (p, q) in enumerate(order_book):
            if p == price:
                return index, p, q
        return None, None, None

    def add_limit_order(self, price, quantity, order_type):
        # add a limit order to the order book
        # the rules are the following:
        # - buy limit order with price >= best ask -> you are executed at the best ask
        # - sell limit toder with price <= best bid -> you are executed at the best bid
        # - otherwise the order goes into the order book
    
        if order_type == 'limit_buy':
            # you want to add a limit buy
            # this means that you go into the bid part of the book and place an order.
            # if you place an order with a price >= than the best ask, then you are executed

            try:
                best_available_ask_price, best_available_ask_quantity = self.asks[0] # TODO: add check that the ask actually exists
            except Exception:
                best_available_ask_price = price + 1
                best_available_ask_quantity = 0
                
            if price >= best_available_ask_price:
                if quantity > best_available_ask_quantity:
                    self.execute_market_order(best_available_ask_quantity, 'market_buy')
                    self.add_limit_order(price, quantity - best_available_ask_quantity, 'limit_buy')
                elif quantity <= best_available_ask_quantity:
                    self.execute_market_order(quantity, 'market_buy') 

            elif price < best_available_ask_price:
                try:
                    best_available_bid_price, _ = self.bids[0] # TODO: add check that the ask actually exists
                except Exception:
                    best_available_bid_price = -1

                if price > best_available_bid_price:
                    self.bids.append((price, quantity))
                    self.bids.sort(key=lambda x: x[0], reverse=True)
                else:
                    index, _, q = OrderBook.find_order_with_certain_price(self.bids, price)
                    if index is not None:
                        self.bids.pop(index)
                        quantity = quantity + q

                    self.bids.append((price, quantity))
                    self.bids.sort(key=lambda x: x[0], reverse=True)                       

        elif order_type == 'limit_sell':
            try:
                best_available_bid_price, best_available_bid_quantity = self.bids[0] # TODO: add check that the ask actually exists
            except Exception:
                best_available_bid_price = -1
                best_available_bid_quantity = 0

            if price <= best_available_bid_price:
                if quantity > best_available_bid_quantity:
                    self.execute_market_order(best_available_bid_quantity, 'market_sell')
                    self.add_limit_order(price, quantity - best_available_bid_quantity, 'limit_sell')

                elif quantity <= best_available_bid_quantity:
                    self.execute_market_order(quantity, 'market_sell')    


            elif price > best_available_bid_price:
                try:
                    best_available_ask_price, _ = self.asks[0] # TODO: add check that the ask actually exists
                except Exception:
                    best_available_ask_price = price + 1

                if price < best_available_ask_price:
                    self.asks.append((price, quantity))
                    self.asks.sort(key=lambda x: x[0])
                else:
                    index, _, q = OrderBook.find_order_with_certain_price(self.asks, price)
                    if index is not None:
                        self.asks.pop(index)
                        quantity = quantity + q

                    self.asks.append((price, quantity))
                    self.asks.sort(key=lambda x: x[0])   


    def add_order_to_the_order_book(self, order: Order):
        if order.order_type in ('market_buy', 'market_sell'):
            self.execute_market_order(order.quantity, order.order_type)
        elif order.order_type in ('limit_buy', 'limit_sell'):
            self.add_limit_order(order.price, order.quantity, order.order_type)
        else:
            print(f"order {order.order_type} not supported")


    def cancel_order(self, order_id):
        # advanced stuff, I will not do this for the moment
        # if you want to implement a logic of order cancelling, you should
        # pass an order id attribute to the Order class
        pass

    def print_order_book_state(self):
        table = PrettyTable()
        table.field_names = ['price', 'quantity', 'side']

        asks = self.asks[::-1]
        for _, (price, quantity) in enumerate(asks):
            table.add_row((price, quantity, 'ask'))
        for _, (price, quantity) in enumerate(self.bids):
            table.add_row((price, quantity, 'bid'))

        print(table)
        print("")

    def get_mid_price(self):
        try:
            return (self.asks[0][0] + self.bids[0][0]) / 2
        except Exception:
            return np.nan

    def get_micro_price(self):
        try:
            price_ask = self.asks[0][0]
            volume_ask = self.asks[0][1]

            price_bid = self.bids[0][0]
            volume_bid = self.bids[0][1]

            return ((volume_bid * price_ask) + (volume_ask * price_bid)) / (volume_ask + volume_bid)
        except Exception:
            return np.nan

