"""
Cookie Clicker Simulator
"""

import simpleplot
import math
import random

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._current_resources = 0.0
        self._total_resources = 0.0
        self._time = 0.0
        self._cookiespersecond = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]
        
        
    def __str__(self):
        """
        Return human readable state
        """
        return str(['Time: ' + str(self._time),
                    'Current cookies: ' + str(self._current_resources),
                    'Total cookies: ' + str(self._total_resources),
                    'CPS: ' + str(self._cookiespersecond)])
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_resources
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cookiespersecond
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: (0.0, None, 0.0, 0.0)
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if self._current_resources >= cookies:
            return 0.0
        else:
            how_long = (cookies - self._current_resources) / self._cookiespersecond
            return math.ceil(how_long)
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0
        """
        if time <= 0:
            return
        else:
            self._time += time
            self._total_resources += time * self._cookiespersecond
            self._current_resources += time * self._cookiespersecond
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if cost > self._current_resources:
            return
        else:
            self._current_resources -= cost
            self._cookiespersecond += additional_cps
            self._history.append((self._time, item_name, cost, self._total_resources))
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to game.
    """
    upgrades =  build_info.clone() 
    game = ClickerState() 
    
    while True:
        if game.get_time() >= duration:
            if game.get_cookies() > 0:
                item_name = strategy(game.get_cookies(), game.get_cps(), (duration - game.get_time()), upgrades)
                if item_name != None:
                    game.buy_item(item_name, upgrades.get_cost(item_name), upgrades.get_cps(item_name))
                    upgrades.update_item(item_name)
            else:
                break
                
        item_name = strategy(game.get_cookies(), game.get_cps(), (duration - game.get_time()), upgrades)
        if item_name == None:
            remainder = duration - game.get_time()
            game.wait(remainder)
            break
        nextitem = game.time_until(upgrades.get_cost(item_name))
        if (game.get_time() + nextitem) > duration:
            remainder = duration - game.get_time()
            game.wait(remainder)
            break
        game.wait(nextitem)
        game.buy_item(item_name, upgrades.get_cost(item_name), upgrades.get_cps(item_name))
        upgrades.update_item(item_name)
        

    # Replace with your code
    return game


def strategy_cursor(cookies, cps, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic strategy does not properly check whether
    it can actually buy a Cursor in the time left.  Your strategy
    functions must do this and return None rather than an item you
    can't buy in the time left.
    """
    return "Cursor"

def strategy_none(cookies, cps, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that you can use to help debug
    your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, time_left, build_info):
    """ 
    Strategy that always buys the most cheapest item
    """
    options = build_info.build_items()
    cheapest_item = float('inf')
    handycursor = ''
    for item in options:
        if build_info.get_cost(item) < cheapest_item:
            cheapest_item = build_info.get_cost(item)
            handycursor = item
            
    if cheapest_item <= (time_left * cps + cookies):
        return handycursor  
    else:
        return None

def strategy_expensive(cookies, cps, time_left, build_info):
    """ 
    Strategy that always buys the most expensive item
    """
    options = build_info.build_items()
    expensive_item = 0
    handycursor = ''
    for item in options:
        if (build_info.get_cost(item) > expensive_item) and (build_info.get_cost(item) <= time_left * cps + cookies):
            expensive_item = build_info.get_cost(item)
            handycursor = item
    if handycursor == "":
        return None
    else:
        return handycursor

def strategy_best(cookies, cps, time_left, build_info):
    """ 
    Strategy that implements my personal 'best' strategy
    """
    options = build_info.build_items()
    best_cps = -9999999999999999999999999999999999999999999999
    handycursor = ''
    for item in options:
        ratio = build_info.get_cps(item) / build_info.get_cost(item)
        if (ratio > best_cps):
            best_cps = ratio
            handycursor = item
    if handycursor == "":
        return None
    else:
        return handycursor
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation with one strategy
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    #history = state.get_history()
    #history = [(item[0], item[3]) for item in history]
    #simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
run()