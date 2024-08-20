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
            
            self.update_traders_wealth(simulation_step)
            self.update_traders_number_of_units_of_stock(simulation_step)

    @abstractmethod
    def simulate_market(self, simulation_step, *args):
        pass


    def update_traders_wealth(self, simulation_step):
        for trader in self.traders:
            trader.wealth_sequence.append((simulation_step, trader.wealth))
        

    def update_traders_number_of_units_of_stock(self, simulation_step):
        for trader in self.traders:
            trader.number_units_stock_sequence.append((simulation_step, trader.number_units_stock))


