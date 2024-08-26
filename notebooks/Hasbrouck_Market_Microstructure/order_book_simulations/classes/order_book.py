"""
This class is the core of the order book simulator. This class allows a Trader object to place some
Order objects as orders in the book. If the demand and the offer match, a Trade object is generated.

This class allows to:
- place limit orders
- execute market orders
- modify orders
- print the state of the order book
- return various quantities (mid price, micro price, bid ask spread, traded price, traded volumes)

Additional features that can be implemented in this simulator are the following:
- stop loss / take profit

"""

from classes.order import Order
from prettytable import PrettyTable
import numpy as np
from classes.trade import Trade


class OrderBook():

    def __init__(self):
        self.bids = []  # list of (price, quantity, order_id, trader_id)
        self.asks = []  # list of (price, quantity, order_id, trader_id)

        self.trades = {} # dictionary where the key is the time (you can see this as a snapshot number) and the value is the Trade object
        self.time = 0 # time of the simulation, you can see this as an order book snapshot number

        self.price_sequence = [] # contains the sequence of executed prices
        self.mid_price_sequence = [] # sequence of mid prices
        self.micro_price_sequence = [] # sequence of micro prices
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


    def execute_market_order(self, quantity, order_type, order_id, trader_id):
        # execute a market order, getting the first available ask if buying
        # and the first available bid if selling
        # if the first available book level is not sufficient to execute the
        # whole trade, the next level is used 

        if order_type == 'market_buy':
            # market buy
            try:
                # pop the best ask
                best_available_ask_price, best_available_ask_quantity, bb_order_id, bb_trader_id = self.asks.pop(0)
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
                            direction='buy',
                            trader_id_already_in_book=bb_trader_id,
                            trader_id_coming_in_book=trader_id,
                            order_id_already_in_book=bb_order_id,
                            order_id_coming_in_book=order_id
                            )
                            ) 
                
                # add another market order for the remaining quantity.
                # this will call the function again and execute it on the new best ask
                # since we called the Trade class, we don't have to take care of margin and units
                self.execute_market_order(round(quantity - best_available_ask_quantity, 5), 'market_buy', order_id, trader_id)
            else:
                # if the quantity is less than the available quantity...
                if quantity != 0:  # <- this is useful to stop the recursion if the market order executes exactly the ask volumes
                    # ... then trade 
                    self.trades[self.time].append(
                        Trade(
                            price=best_available_ask_price, 
                            volume=quantity,
                            direction='buy',
                            trader_id_already_in_book=bb_trader_id,
                            trader_id_coming_in_book=trader_id,
                            order_id_already_in_book=bb_order_id,
                            order_id_coming_in_book=order_id)
                            )
                # since we popped the best ask, now we want to put it again in the asks sequence,
                # with the updated volume 
                # since we called the Trade class, we don't have to take care of margin and units
                self.asks.append((best_available_ask_price, round(best_available_ask_quantity - quantity, 5), bb_order_id, bb_trader_id))
                self.asks = sorted(self.asks, key=lambda x: (x[0], x[2]))

        elif order_type == 'market_sell':
            # market sell
            # the code is similar to market buy, but with the bids
            try:
                best_available_bid_price, best_available_bid_quantity, bb_order_id, bb_trader_id = self.bids.pop(0)
            except Exception:
                # bid is empty
                return
            if quantity >= best_available_bid_quantity:
                self.trades[self.time].append(
                    Trade(
                        price=best_available_bid_price, 
                        volume=best_available_bid_quantity,
                        direction='sell',
                        trader_id_already_in_book=bb_trader_id,
                        trader_id_coming_in_book=trader_id,
                        order_id_already_in_book=bb_order_id,
                        order_id_coming_in_book=order_id)
                        )
                # since we called the Trade class, we don't have to take care of margin and units

                self.execute_market_order(round(quantity - best_available_bid_quantity, 5), 'market_sell', order_id, trader_id)
            else:
                if quantity != 0:
                    self.trades[self.time].append(
                        Trade(
                            price=best_available_bid_price, 
                            volume=quantity,
                            direction='sell',
                            trader_id_already_in_book=bb_trader_id,
                            trader_id_coming_in_book=trader_id,
                            order_id_already_in_book=bb_order_id,
                            order_id_coming_in_book=order_id)
                            ) 
                # since we called the Trade class, we don't have to take care of margin and units

                self.bids.append((best_available_bid_price, round(best_available_bid_quantity - quantity, 5), bb_order_id, bb_trader_id))
                self.bids = sorted(self.bids, key=lambda x: (-x[0], x[2]))
    

    @staticmethod
    def find_order_with_certain_price(order_book, price, order_id=None):
        # this method finds the orders with a certain price
        # this is useful to update the volumes of the orders when dealing with a limit order
        orders = []
        for index, (p, q, o_id, t_id) in enumerate(order_book):
            if p == price:
                orders.append((index, (p, q, o_id, t_id)))

        if not orders:
            return None
        else:
            return orders

    def modify_order_of_the_order_book(self, trader, price, quantity, order_type, trader_id):
        if order_type == 'modify_limit_buy':
            where_to_look = self.bids
            rev = True

            # I already checked that this is feasible
            trader.margin += (price * quantity)

        elif order_type == 'modify_limit_sell':
            where_to_look = self.asks
            rev = False

            # I already checked that this is feasible
            trader.number_units_stock += quantity

        else:
            raise ValueError('Order type not supported')
        

        orders = OrderBook.find_order_with_certain_price(where_to_look, price)

        if orders is not None:
            while True:
                # a trader could have many orders with that price
                (index, q_in_order, id) = [(t[0], t[1][1], t[1][2]) for t in orders if t[1][3] == trader_id][0]

                where_to_look.pop(index)
                quantity = round(q_in_order - quantity, 5)

                if quantity > 0:
                    # if something remains, then add it again to the book
                    where_to_look.append((price, quantity, id, trader_id))
                    break
                elif quantity == 0:
                    break
                else:
                    quantity = abs(quantity)
                    orders = OrderBook.find_order_with_certain_price(where_to_look, price)


        if rev:
            self.bids = sorted(self.bids, key=lambda x: (-x[0], x[2]))
        else:
            self.asks = sorted(self.asks, key=lambda x: (x[0], x[2]))
        


    def add_limit_order(self, trader, price, quantity, order_type, order_id, trader_id):
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
                best_available_ask_price, best_available_ask_quantity, bb_order_id, bb_trader_id = self.asks[0]
            except Exception:
                # if there is no ask add a fake one, in reality probably a dealer would execute your trade
                best_available_ask_price = price + 1
                best_available_ask_quantity = 0
                
            # if your limit buy has a price greater than the best ask, you are executed at the best ask
            if price >= best_available_ask_price:
                # you are executed at the best ask for the volumes in the best ask
                if quantity > best_available_ask_quantity:
                    if best_available_ask_quantity != 0:
                        self.execute_market_order(best_available_ask_quantity, 'market_buy', order_id, trader_id)

                    # then you are either executed at the next best ask or a limit buy is added
                    # this does this logic recursively
                    self.add_limit_order(trader, price, round(quantity - best_available_ask_quantity, 5), 'limit_buy', order_id, trader_id)
                    trader.margin = round(trader.margin - (quantity - best_available_ask_quantity), 5) * price

                # if the quantity is less than the available quantity, you are executed on the best ask
                elif quantity <= best_available_ask_quantity:
                    self.execute_market_order(quantity, 'market_buy', order_id, trader_id) 

            # if your price is less than the best ask, then your order goes in the book
            elif price < best_available_ask_price:
                # now check for the best bid
                try:
                    best_available_bid_price, _, _, _ = self.bids[0]
                except Exception:
                    best_available_bid_price = -1


                self.bids.append((price, quantity, order_id, trader_id))
                self.bids = sorted(self.bids, key=lambda x: (-x[0], x[2]))  

                trader.margin = round(trader.margin - (quantity * price), 5)

        elif order_type == 'limit_sell':
            # this is similar to the limit buy situation
            try:
                best_available_bid_price, best_available_bid_quantity, bb_order_id, bb_trader_id = self.bids[0]
            except Exception:
                best_available_bid_price = -1
                best_available_bid_quantity = 0

            if price <= best_available_bid_price:
                if quantity > best_available_bid_quantity:
                    if best_available_bid_quantity != 0:
                        self.execute_market_order(best_available_bid_quantity, 'market_sell', order_id, trader_id)
                    self.add_limit_order(trader, price, round(quantity - best_available_bid_quantity, 5), 'limit_sell', order_id, trader_id)
                    
                    trader.number_units_stock = round(trader.number_units_stock - (quantity - best_available_bid_quantity), 5)

                elif quantity <= best_available_bid_quantity:
                    self.execute_market_order(quantity, 'market_sell', order_id, trader_id)    


            elif price > best_available_bid_price:
                try:
                    best_available_ask_price, _, _, _ = self.asks[0]
                except Exception:
                    best_available_ask_price = price + 1

                self.asks.append((price, quantity, order_id, trader_id))
                self.asks = sorted(self.asks, key=lambda x: (x[0], x[2]))

                trader.number_units_stock = round(trader.number_units_stock - quantity, 5)


    def order_manager(self, order: Order, trader, time=None):
        # method used to add, execute or modify an order of the order book 
        if time is None:
            self.time += 1
        else:
            self.time = time
            
        self.trades[self.time] = []

        if order.order_type in ('market_buy', 'market_sell'):
            self.execute_market_order(order.quantity, order.order_type, self.time, order.trader_id)
        elif order.order_type in ('limit_buy', 'limit_sell'):
            self.add_limit_order(trader, order.price, order.quantity, order.order_type, self.time, order.trader_id)
        elif order.order_type in ('modify_limit_buy', 'modify_limit_sell'):
            self.modify_order_of_the_order_book(trader, order.price, order.quantity, order.order_type, order.trader_id)

        # if no orders we want to update the book anyway

        # update the lists useful to track various quantities

        self.update_mid_price_sequence()
        self.update_micro_price_sequence()

        self.update_bid_ask_spread_sequence()
        self.update_price_volume_sequences()
        self.update_volume_imbalance_sequence()
        self.update_order_flow_imbalance_sequence()

        self.update_book_state_sequence()
        self.update_depth_sequence()



    def print_order_book_state(self):
        # print the bid and the asks, with prices and volumess
        print(f"\nOrder book at time {self.time}")

        table = PrettyTable()
        table.field_names = ['price', 'quantity', 'side']

        asks = self.asks[::-1]

        sums = {}
        for p, v, _, _ in asks:
            if p in sums:
                sums[p] += v
            else:
                sums[p] = v

        for p, v in list(sums.items()):
            table.add_row((p, v, 'ask'))

        sums = {}
        for p, v, _, _ in self.bids:
            if p in sums:
                sums[p] += v
            else:
                sums[p] = v

        for p, v in list(sums.items()):
            table.add_row((p, v, 'bid'))

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
            asks_orders = self.find_order_with_certain_price(self.asks, price_ask)
            volume_ask = sum([v[1][1] for v in asks_orders])

            price_bid = self.bids[0][0]
            bids_orders = self.find_order_with_certain_price(self.bids, price_bid)
            volume_bid = sum([v[1][1] for v in bids_orders])

            return ((volume_bid * price_ask) + (volume_ask * price_bid)) / (volume_ask + volume_bid)
        except Exception:
            return np.nan

    def return_bid_ask_spread(self):
        # return the bid ask spread
        try:
            price_ask = self.asks[0][0]
            price_bid = self.bids[0][0]

            return round(price_ask - price_bid, 5)
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

        if self.asks:
            sums = {}
            first_ask = True
            for p, v, _, _ in self.asks:
                if first_ask:
                    self.last_best_ask_price = p # quantity useful to compute the order flow imbalance
                    first_ask = False
                if p in sums:
                    sums[p] += v
                else:
                    sums[p] = v

            
            ask_list = [[self.time, p, v, 'ask'] for p, v in sums.items()]

            # quantity useful to compute the order flow imbalance
            self.last_best_ask_volume = sums[self.last_best_ask_price]

        self.book_state_sequence.append(ask_list)

        if self.bids:
            sums = {}
            first_bid = True
            for p, v, _, _ in self.bids:
                if first_bid:
                    self.last_best_bid_price = p # quantity useful to compute the order flow imbalance
                    first_bid = False
                if p in sums:
                    sums[p] += v
                else:
                    sums[p] = v

            
            bid_list = [[self.time, p, v, 'bid'] for p, v in sums.items()]

            # quantity useful to compute the order flow imbalance
            self.last_best_bid_volume = sums[self.last_best_bid_price]

        self.book_state_sequence.append(bid_list)


    def update_mid_price_sequence(self):
        self.mid_price_sequence.append(self.return_mid_price())

    def update_micro_price_sequence(self):
        self.micro_price_sequence.append(self.return_micro_price())

    def update_bid_ask_spread_sequence(self):
        self.bid_ask_spread_sequence.append(self.return_bid_ask_spread())


    def return_volume_imbalance(self):
        try:
            asks_orders = self.find_order_with_certain_price(self.asks, self.asks[0][0])
            volume_ask = sum([v[1][1] for v in asks_orders])

            bids_orders = self.find_order_with_certain_price(self.bids, self.bids[0][0])
            volume_bid = sum([v[1][1] for v in bids_orders])

            return round(volume_bid - volume_ask, 5) / (volume_bid + volume_ask)
        
        except Exception:
            return np.nan
        

    def update_volume_imbalance_sequence(self):
        self.volume_imbalance_sequence.append(self.return_volume_imbalance())


    def return_order_flow_imbalance(self):
        try:
            if self.time == 1:
                return 0
            
            else:
                # sum volumes of orders with the same price
                price_ask = self.asks[0][0]
                asks_orders = self.find_order_with_certain_price(self.asks, price_ask)
                volume_ask = sum([v[1][1] for v in asks_orders])

                price_bid = self.bids[0][0]
                bids_orders = self.find_order_with_certain_price(self.bids, price_bid)
                volume_bid = sum([v[1][1] for v in bids_orders])

                if price_bid > self.last_best_bid_price:
                    delta_volume_bid = volume_bid
                elif price_bid < self.last_best_bid_price:
                    delta_volume_bid =  - self.last_best_bid_volume
                else:
                    delta_volume_bid = round(volume_bid - self.last_best_bid_volume, 5)

                if price_ask > self.last_best_ask_price:
                    delta_volume_ask = - self.last_best_ask_volume
                elif price_ask < self.last_best_ask_price:
                    delta_volume_ask = volume_ask
                else:
                    delta_volume_ask = round(volume_ask - self.last_best_ask_volume, 5)


                return round(delta_volume_bid - delta_volume_ask, 5)
        
        
        except Exception:
            return 0
        

    def update_order_flow_imbalance_sequence(self):
        self.order_flow_imbalance_sequence.append(self.return_order_flow_imbalance())

    def return_order_book_depth_size(self):
        return (len(self.book_state_sequence[(self.time * 2) - 2]), 
                len(self.book_state_sequence[(self.time * 2) - 1]))
    
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


