"""
This class is the core of the order book simulator. This class allows a Trader object to place some
Order objects as orders in the book. If the demand and the offer match, a Trade object is generated.

This class allows to:
- place limit orders
- execute market orders
- print the state of the order book
- return various quantities (mid price, micro price, bid ask spread, traded price, traded volumes)

Additional features that can be implemented in this simulator are the following:
- order canceling
- stop loss / take profit
- implement ticks
- order modifying

"""

from classes.order import Order
from prettytable import PrettyTable
import numpy as np
from classes.trade import Trade


class OrderBook():

    def __init__(self):
        self.bids = []  # list of (price, quantity)
        self.asks = []  # list of (price, quantity)

        self.trades = {} # dictionary where the key is the time (you can see this as a snapshot number) and the value is the Trade object
        self.time = 0 # time of the simulation, you can see this as an order book snapshot number

        self.price_sequence = [] # contains the sequence of executed prices
        self.mid_price_sequence = [] # sequence of mid prices
        self.volumes_sequence = [] # sequence of volumes of the executed prices
        self.buy_sequence = [] # 1 if the trade was a buy, 0 otherwise
        self.sell_sequence = [] # 1 if the trade was a sell, 0 otherwise
        self.book_state_sequence = [] # wrapper for the book state
        self.bid_ask_spread_sequence = [] # sequence of bid ask spreads
        self.volume_imbalance_sequence = [] # sequence of volume imbalances
        self.order_flow_imbalance_sequence = [] # sequence of order flow imbalances
        self.last_best_bid_price = np.nan
        self.last_best_ask_price = np.nan
        self.last_best_bid_volume = np.nan
        self.last_best_ask_volume = np.nan
        self.depth_sequence_size = [] # sequence of depth of the book
        self.depth_sequence_volumes = [] # sequence of depth of the book

    def execute_market_order(self, quantity, order_type):
        # execute a market order, getting the first available ask if buying
        # and the first available bid if selling
        # if the first available book level is not sufficient to execute the
        # whole trade, the next level is used 

        if order_type == 'market_buy':
            # market buy
            try:
                # pop the best ask
                best_available_ask_price, best_available_ask_quantity = self.asks.pop(0)
            except Exception:
                # ask is empty
                return
            
            # if traded quantity > available quantity...
            if quantity >= best_available_ask_quantity:
                # ...the trade happens at the ask and all the available volumes at ask are traded
                self.trades[self.time].append(
                        Trade(
                            price=best_available_ask_price, 
                            volume=best_available_ask_quantity,
                            direction='buy')
                            ) 
                
                # add another market order for the remaining quantity.
                # this will call the function again and execute it on the new best ask
                self.execute_market_order(quantity - best_available_ask_quantity, 'market_buy')
            else:
                # if the quantity is less than the available quantity...
                if quantity != 0:  # <- this is useful to stop the recursion if the market order executes exactly the ask volumes
                    # ... then trade 
                    self.trades[self.time].append(
                        Trade(
                            price=best_available_ask_price, 
                            volume=quantity,
                            direction='buy')
                            )
                # since we popped the best ask, now we want to put it again the the asks sequence,
                # with the updated volume 
                self.asks.append((best_available_ask_price, best_available_ask_quantity - quantity))
                self.asks.sort(key=lambda x: x[0])

        elif order_type == 'market_sell':
            # market sell
            # the code is similar to market buy, but with the bids
            try:
                best_available_bid_price, best_available_bid_quantity = self.bids.pop(0)
            except Exception:
                # bid is empty
                return
            if quantity >= best_available_bid_quantity:
                self.trades[self.time].append(
                    Trade(
                        price=best_available_bid_price, 
                        volume=best_available_bid_quantity,
                        direction='sell')
                        )
                            
                self.execute_market_order(quantity - best_available_bid_quantity, 'market_sell')
            else:
                if quantity != 0:
                    self.trades[self.time].append(
                        Trade(
                            price=best_available_bid_price, 
                            volume=quantity,
                            direction='sell')
                            ) 

                self.bids.append((best_available_bid_price, best_available_bid_quantity - quantity))
                self.bids.sort(key=lambda x: x[0], reverse=True)
    

    @staticmethod
    def find_order_with_certain_price(order_book, price):
        # this method finds the orders with a certain price
        # this is useful to update the volumes of the orders when dealing with a limit order
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
                # get the best ask
                best_available_ask_price, best_available_ask_quantity = self.asks[0]
            except Exception:
                # if there is no ask add a fake one, in reality probably a dealer would execute your trade
                best_available_ask_price = price + 1
                best_available_ask_quantity = 0
                
            # if your limit buy has a price greater than the best ask, you are executed at the best ask
            if price >= best_available_ask_price:
                # you are executed at the best ask for the volumes in the best ask
                if quantity > best_available_ask_quantity:
                    self.execute_market_order(best_available_ask_quantity, 'market_buy')

                    # then you are either executed at the next best ask or a limit buy is added
                    # this does this logic recursively
                    self.add_limit_order(price, quantity - best_available_ask_quantity, 'limit_buy')
                
                # if the quantity is less than the available quantity, you are executed on the best ask
                elif quantity <= best_available_ask_quantity:
                    self.execute_market_order(quantity, 'market_buy') 

            # if your price is less than the best ask, then your order goes in the book
            elif price < best_available_ask_price:
                # now check for the best bid
                try:
                    best_available_bid_price, _ = self.bids[0]
                except Exception:
                    best_available_bid_price = -1

                # find the price level to add your limit order to.
                # if no price level is found, then add a new one
                index, _, q = OrderBook.find_order_with_certain_price(self.bids, price)
                if index is not None:
                    self.bids.pop(index)
                    quantity = quantity + q

                self.bids.append((price, quantity))
                self.bids.sort(key=lambda x: x[0], reverse=True)                       

        elif order_type == 'limit_sell':
            # this is similar to the limit buy situation
            try:
                best_available_bid_price, best_available_bid_quantity = self.bids[0]
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
                    best_available_ask_price, _ = self.asks[0]
                except Exception:
                    best_available_ask_price = price + 1

                index, _, q = OrderBook.find_order_with_certain_price(self.asks, price)
                if index is not None:
                    self.asks.pop(index)
                    quantity = quantity + q

                self.asks.append((price, quantity))
                self.asks.sort(key=lambda x: x[0])   


    def add_order_to_the_order_book(self, order: Order):
        # method used to add (or execute) an order in the order book 
        self.time += 1
        self.trades[self.time] = []

        if order.order_type in ('market_buy', 'market_sell'):
            self.execute_market_order(order.quantity, order.order_type)
        elif order.order_type in ('limit_buy', 'limit_sell'):
            self.add_limit_order(order.price, order.quantity, order.order_type)

        # if no orders we want to update the book anyway

        # update the lists useful to track various quantities

        self.update_mid_price_sequence()
        self.update_bid_ask_spread_sequence()
        self.update_price_volume_sequences()
        self.update_volume_imbalance_sequence()
        self.update_order_flow_imbalance_sequence()
        self.update_depth_sequence()


        # last thing I do is updating the book state sequence
        self.update_book_state_sequence()


    def print_order_book_state(self):
        # print the bid and the asks, with prices and volumess
        print(f"\nOrder book at time {self.time}")

        table = PrettyTable()
        table.field_names = ['price', 'quantity', 'side']

        asks = self.asks[::-1]
        for _, (price, quantity) in enumerate(asks):
            table.add_row((price, quantity, 'ask'))
        for _, (price, quantity) in enumerate(self.bids):
            table.add_row((price, quantity, 'bid'))

        print(table)
        print("")

    def return_mid_price(self):
        # return the mid price, that is in the middle of the bid ask spread
        try:
            return (self.asks[0][0] + self.bids[0][0]) / 2
        except Exception:
            return np.nan

    def return_micro_price(self):
        # return the microprice
        try:
            price_ask = self.asks[0][0]
            volume_ask = self.asks[0][1]

            price_bid = self.bids[0][0]
            volume_bid = self.bids[0][1]

            return ((volume_bid * price_ask) + (volume_ask * price_bid)) / (volume_ask + volume_bid)
        except Exception:
            return np.nan

    def return_bid_ask_spread(self):
        # return the bid ask spread
        try:
            price_ask = self.asks[0][0]
            price_bid = self.bids[0][0]

            return price_ask - price_bid
        except Exception:
            return np.nan


    def update_price_volume_sequences(self):
        trades = self.trades[self.time]

        if trades:
            sum_of_volume = 0
            price_executed = 0
            direction = ''
            for trade in trades:
                sum_of_volume += trade.volume
                price_executed = trade.price
                direction = trade.direction
            
            self.price_sequence.append(price_executed)
            self.volumes_sequence.append(sum_of_volume)

            if direction == 'buy':
                self.buy_sequence.append(1)
                self.sell_sequence.append(0)
            elif direction == 'sell':
                self.buy_sequence.append(0)
                self.sell_sequence.append(1)

        else:
            if self.price_sequence:
                self.price_sequence.append(self.price_sequence[-1])
            else:
                self.price_sequence.append(self.return_mid_price())

            self.volumes_sequence.append(0)
            self.buy_sequence.append(0)
            self.sell_sequence.append(0)


    def update_book_state_sequence(self):
        ask_list = []
        bid_list = []

        for i, (price, quantity) in enumerate(self.asks):
            if i == 0:
                self.last_best_ask_price = price
                self.last_best_ask_volume = quantity

            ask_list.append([self.time, price, quantity, 'ask'])

        self.book_state_sequence.append(ask_list)

        for i, (price, quantity) in enumerate(self.bids):
            if i == 0:
                self.last_best_bid_price = price
                self.last_best_bid_volume = quantity

            bid_list.append([self.time, price, quantity, 'bid'])

        self.book_state_sequence.append(bid_list)


    def update_mid_price_sequence(self):
        self.mid_price_sequence.append(self.return_mid_price())


    def update_bid_ask_spread_sequence(self):
        self.bid_ask_spread_sequence.append(self.return_bid_ask_spread())


    def return_volume_imbalance(self):
        try:
            volume_ask = self.asks[0][1]

            volume_bid = self.bids[0][1]

            return (volume_bid - volume_ask) / (volume_bid + volume_ask)
        
        except Exception:
            return np.nan
        

    def update_volume_imbalance_sequence(self):
        self.volume_imbalance_sequence.append(self.return_volume_imbalance())


    def return_order_flow_imbalance(self):
        try:
            if self.time == 1:
                return 0
            
            else:
                price_ask = self.asks[0][0]
                volume_ask = self.asks[0][1]

                price_bid = self.bids[0][0]
                volume_bid = self.bids[0][1]

                if price_bid > self.last_best_bid_price:
                    delta_volume_bid = volume_bid
                elif price_bid < self.last_best_bid_price:
                    delta_volume_bid =  - self.last_best_bid_volume
                else:
                    delta_volume_bid = volume_bid - self.last_best_bid_volume

                if price_ask > self.last_best_ask_price:
                    delta_volume_ask = - self.last_best_ask_volume
                elif price_ask < self.last_best_ask_price:
                    delta_volume_ask = volume_ask
                else:
                    delta_volume_ask = volume_ask - self.last_best_ask_volume


                return delta_volume_bid - delta_volume_ask
        
        
        except Exception:
            return 0
        

    def update_order_flow_imbalance_sequence(self):
        self.order_flow_imbalance_sequence.append(self.return_order_flow_imbalance())

    def return_order_book_depth_size(self):
        return (len(self.asks), len(self.bids))
    
    def return_order_book_depth_volumes(self):
        sum_volumes_ask = 0
        for a in self.asks:
            sum_volumes_ask += a[1]

        sum_volumes_bid = 0
        for b in self.bids:
            sum_volumes_bid += b[1]

        return (sum_volumes_ask, sum_volumes_bid)

    def update_depth_sequence(self):
        self.depth_sequence_size.append(self.return_order_book_depth_size())
        self.depth_sequence_volumes.append(self.return_order_book_depth_volumes())


