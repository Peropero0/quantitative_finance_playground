"""
This class contains the logic of the simulation. You can run the simulations using the method run_market_manager.
Write custom logic in the method simulate_market.
"""
from classes.trader import Trader
from classes.order_book import OrderBook
from abc import abstractmethod

class MarketManager():

    def __init__(self, simulation_length, traders_dict, book: OrderBook):
        self.simulation_length = simulation_length
        self.traders = self.generate_traders(traders_dict)
        self.book = book


    def generate_traders(self, traders_dict):
        """ Method useful to generate traders. The traders dict is a dictionary that has:
        - key -> is an int representing the trader_id, you should have a key for each trader
        - values:
            - value[0] -> initial_wealth : initial wealth of the trader, can be a float
            - value[1] -> number_units_stock : inital number of units of stock of the trader, can be a float
            - value[2] -> check_order_feasibility : do I have to check if a trader has enough cash/units to trade?
        """

        traders_list = []
        for key, value in traders_dict.items():
            traders_list.append(
                Trader(
                    initial_wealth=value[0], 
                    number_units_stock=value[1], 
                    check_order_feasibility=value[2], 
                    trader_id=key
                    )
                    )
        
        return traders_list

    def run_market_manager(self, *args):
        """This is the main engine that you should run. This takes care of running the simulation
        that is defined under self.simulate_market() .
        At each timestep of the simulation, run the actual logic of the market and then 
        update the trader's quantities, like the wealth and the number of units.
        """

        # update the traders' sequences with initial values
        self.update_traders_wealth(simulation_step=0)
        self.update_traders_number_of_units_of_stock(simulation_step=0)

        for simulation_step in range(1, self.simulation_length + 1):
            self.simulate_market(simulation_step, *args)

            self.update_current_wealth_margin_and_units(simulation_step)

            self.update_traders_wealth(simulation_step)
            self.update_traders_number_of_units_of_stock(simulation_step)

            self.update_traders_active_orders()

    @abstractmethod
    def simulate_market(self, simulation_step, *args):
        """
        Here you can add a custom logic of how the traders should behave
        """
        pass


    def update_traders_wealth(self, simulation_step):
        for trader in self.traders:
            trader.wealth_sequence.append((simulation_step, trader.wealth))
        

    def update_traders_number_of_units_of_stock(self, simulation_step):
        for trader in self.traders:
            trader.number_units_stock_sequence.append((simulation_step, trader.number_units_stock))

    
    def update_current_wealth_margin_and_units(self, simulation_step):
        """
        This function is useful to update the current wealth, margin and units of each trader.

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
                trader_coming_in_book.wealth = round(
                    trader_coming_in_book.wealth - (trade.price * trade.volume), 5)
                trader_coming_in_book.margin = round(
                    trader_coming_in_book.margin - (trade.price * trade.volume), 5)
                trader_coming_in_book.number_units_stock = round(
                    trader_coming_in_book.number_units_stock + trade.volume, 5)

                trader_already_in_book.wealth = round(
                    trader_already_in_book.wealth + (trade.price * trade.volume), 5)
                trader_already_in_book.margin = round(
                    trader_already_in_book.margin + (trade.price * trade.volume), 5)
                
                # I already subtracted the number of shares when issuing the limit order!

            elif trade.direction == 'sell':
                trader_coming_in_book.wealth = round(
                    trader_coming_in_book.wealth + (trade.price * trade.volume), 5)
                trader_coming_in_book.margin = round(
                    trader_coming_in_book.margin + (trade.price * trade.volume), 5)
                trader_coming_in_book.number_units_stock = round(
                    trader_coming_in_book.number_units_stock - trade.volume, 5)

                trader_already_in_book.wealth = round(
                    trader_already_in_book.wealth - (trade.price * trade.volume), 5)
                # I already subtracted the margin when issuing the limit order!
                trader_already_in_book.number_units_stock = round(
                    trader_already_in_book.number_units_stock + trade.volume, 5)





    def update_traders_active_orders(self):
        """
        Keep track of active orders issued by each trader
        """
        for trader in self.traders:
            active_limit_buys = [(bid[0], bid[1], bid[2], 'limit_buy') for bid in self.book.bids if bid[3] == trader.trader_id]
            active_limit_sells = [(ask[0], ask[1], ask[2], 'limit_sell') for ask in self.book.asks if ask[3] == trader.trader_id]

            trader.active_orders = active_limit_buys + active_limit_sells

