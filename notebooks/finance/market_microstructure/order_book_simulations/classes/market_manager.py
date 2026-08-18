"""
This class contains the logic of the simulation. You can run the simulations using the method run_market_manager.
Write custom logic in the method simulate_market.
"""
from classes.trader import Trader
from classes.order_book import OrderBook
from abc import abstractmethod
import numpy as np

class MarketManager():

    def __init__(self, simulation_length, traders_dict, book: OrderBook):
        self.simulation_length = simulation_length
        self.traders = self.generate_traders(traders_dict)
        self.book = book


    def generate_traders(self, traders_dict):
        """ Method useful to generate traders. The traders dict is a dictionary that has:
        - key -> is an int representing the trader_id, you should have a key for each trader
        - values:
            - value[0] -> initial_cash : initial cash of the trader, can be a float
            - value[1] -> number_units_stock_in_inventory : inital number of units of stock of the trader, can be a float
            - value[2] -> check_order_feasibility : do I have to check if a trader has enough cash/units to trade?
        """

        traders_list = []
        for key, value in traders_dict.items():
            traders_list.append(
                Trader(
                    initial_cash=value[0], 
                    number_units_stock_in_inventory=value[1], 
                    check_order_feasibility=value[2], 
                    trader_id=key
                    )
                    )
        
        return traders_list

    def run_market_manager(self, *args):
        """This is the main engine that you should run. This takes care of running the simulation
        that is defined under self.simulate_market() .
        At each timestep of the simulation, run the actual logic of the market and then 
        update the trader's quantities, like the cash and the number of units.
        """

        # update the traders' sequences with initial values
        self.update_traders_cash(simulation_step=0)
        self.update_traders_number_of_units_of_stock(simulation_step=0)

        for simulation_step in range(1, self.simulation_length + 1):
            self.simulate_market(simulation_step, *args)

            self.update_current_cash_margin_and_units(simulation_step)

            self.update_traders_cash(simulation_step)
            self.update_traders_number_of_units_of_stock(simulation_step)
            self.update_traders_total_wealth(simulation_step)
            self.update_traders_active_orders()

    @abstractmethod
    def simulate_market(self, simulation_step, *args):
        """
        Here you can add a custom logic of how the traders should behave
        """
        pass


    def update_traders_cash(self, simulation_step):
        for trader in self.traders:
            trader.cash_sequence.append((simulation_step, trader.cash))
        

    def update_traders_number_of_units_of_stock(self, simulation_step):
        for trader in self.traders:
            trader.number_units_stock_in_inventory_sequence.append((simulation_step, trader.number_units_stock_in_inventory))
            trader.number_units_stock_in_market_sequence.append((simulation_step, trader.number_units_stock_in_market))

    def update_traders_total_wealth(self, simulation_step):
        for trader in self.traders:
            if np.isnan(self.book.price_sequence[-1]) or (self.book.price_sequence[-1] == False):
                price = self.book.mid_price_sequence[-1]
            else:
                price = self.book.price_sequence[-1]

            # total wealth = 
            # cash + (stocks in my inventory + stocks in limit sells) * last price)
            total_wealth = trader.cash + ((trader.number_units_stock_in_inventory + trader.number_units_stock_in_market) * price)

            trader.total_wealth_sequence.append((simulation_step, total_wealth))

    def update_current_cash_margin_and_units(self, simulation_step):
        """
        This function is useful to update the current cash, margin and units of each trader.

        It uses the trades list of the book to update the quantities.
        We don't update some quantities because we already did that in the order book class
        """   
        for trade in self.book.trades[simulation_step]:
            trader_already_in_book = [
                trader for trader in self.traders if trader.trader_id == trade.trader_id_already_in_book
                ][0]
            
            trader_coming_in_book = [
                trader for trader in self.traders if trader.trader_id == trade.trader_id_coming_in_book
                ][0]
            

            if trade.direction == 'buy':
                trader_coming_in_book.cash = round(
                    trader_coming_in_book.cash - (trade.price * trade.volume), 5)
                
                trader_coming_in_book.margin = round(
                    trader_coming_in_book.margin - (trade.price * trade.volume), 5)
                
                trader_coming_in_book.number_units_stock_in_inventory = round(
                    trader_coming_in_book.number_units_stock_in_inventory + trade.volume, 5)
                
                trader_already_in_book.cash = round(
                    trader_already_in_book.cash + (trade.price * trade.volume), 5)
                trader_already_in_book.margin = round(
                    trader_already_in_book.margin + (trade.price * trade.volume), 5)
                
                trader_already_in_book.number_units_stock_in_market = round(
                    trader_already_in_book.number_units_stock_in_market - trade.volume,5)

            elif trade.direction == 'sell':
                trader_coming_in_book.cash = round(
                    trader_coming_in_book.cash + (trade.price * trade.volume), 5)
                trader_coming_in_book.margin = round(
                    trader_coming_in_book.margin + (trade.price * trade.volume), 5)
                
                trader_coming_in_book.number_units_stock_in_inventory = round(
                    trader_coming_in_book.number_units_stock_in_inventory - trade.volume, 5)
                

                trader_already_in_book.cash = round(
                    trader_already_in_book.cash - (trade.price * trade.volume), 5)

                trader_already_in_book.number_units_stock_in_inventory = round(
                    trader_already_in_book.number_units_stock_in_inventory + trade.volume, 5)





    def update_traders_active_orders(self):
        """
        Keep track of active orders issued by each trader
        """
        for trader in self.traders:
            active_limit_buys = [(bid[0], bid[1], bid[2], 'limit_buy') for bid in self.book.bids if bid[3] == trader.trader_id]
            active_limit_sells = [(ask[0], ask[1], ask[2], 'limit_sell') for ask in self.book.asks if ask[3] == trader.trader_id]

            trader.active_orders = active_limit_buys + active_limit_sells

