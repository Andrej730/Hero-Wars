# ======================================================================
# >> IMPORTS
# ======================================================================

# Python
from random import randint

from functools import wraps, WRAPPER_ASSIGNMENTS

# Source.Python
from listeners.tick.repeat import TickRepeat

from messages import SayText2

from filters.players import PlayerIter

# ======================================================================
# >> CLASSES
# ======================================================================

class classproperty(object):
    """
    Decorator to create a class property.

    http://stackoverflow.com/a/3203659/2505645
    """

    def __init__(self, getter):
        self.getter = getter

    def __get__(self, instance, owner):
        return self.getter(owner)


# ======================================================================
# >> FUNCTIONS
# ======================================================================

def find_element(iterable, attr_name, attr_value):
    """Finds an element from an iterable by comparing an attribute.

    Args:
        iterable: Where to seek for the element
        attr_name: Name of the comparable attribute
        attr_value: Value to compare to

    Returns:
        The first element with matching attribute
    """

    for x in iterable:
        if getattr(x, attr_name) == attr_value:
            return x


def find_elements(iterable, attr_name, attr_value):
    """Finds all elements from an iterable by comparing an attribute.

    Args:
        iterable: Where to seek for the element
        attr_name: Name of the comparable attribute
        attr_value: Value to compare to

    Returns:
        A generator of elements with matching attribute
    """

    return (x for x in iterable if getattr(x, attr_name) == attr_value)


def get_subclasses(cls):
    """Returns a set of class's subclasses.

    Returns:
        A set of class's subclasses.
    """

    subclasses = set()
    for subcls in cls.__subclasses__():
        subclasses.add(subcls)
        subclasses.update(get_subclasses(subcls))
    return subclasses


def get_messages(lang_strings):
    """Gets a dict of SayText2 messages from a LangStrings object.

    Args:
        lang_strings: LangStrings object used to fetch the messages

    Returns:
        A dict of SayText2 messages
    """

    return {key: SayText2(message=lang_strings[key]) for key in lang_strings}


def shiftattr(obj, attr_name, shift):
    """Shifts an attribute's value.

    Similar to getattr() and setattr(), shiftattr() shifts
    (increments or decrements) attributes value by the given shift.

    Args:
        obj: Object whose attribute to shift
        attr_name: Name of the attribute to shift
        shift: Shift to make, can be negative
    """

    setattr(obj, attr_name, getattr(obj, attr_name) + shift)


def chance(percentage):
    """Decorates a function to be executed at a static chance.

    Takes a percentage as a parameter, returns an other decorator
    that wraps the original function so that it only gets executed
    at a chance of the given percentage.

    Args:
        percentage: Chance of execution in percentage (0-100)

    Returns:
        New function that doesn't always get executed when called
    """

    return chancef(lambda self, **eargs: percentage)


def chancef(fn):
    """Decorates a function to be executed at a dynamic chance.

    Takes a percentage as a parameter, returns an other decorator
    that wraps the original function so that it only gets executed
    at a chance of the percentage calculated by given function.

    Args:
        fn: Function to determine the chance of the method's execution

    Returns:
        New function that doesn't always get executed when called
    """

    # Create a decorator using the function provided
    def method_decorator(method):

        # Create a wrapper method
        @wraps(method, assigned=WRAPPER_ASSIGNMENTS+('__dict__',), updated=())
        def method_wrapper(self, **eargs):

            # If the randomization passes
            if randint(0, 100) <= fn(self, **eargs):

                # Call the method
                return method(self, **eargs)

            # Else exit with code 2
            return 2

        # Return the wrapper
        return method_wrapper

    # Return the decorator
    return method_decorator


def cooldown(time, message=None):
    """Decorates a function to have a static cooldown.

    Decorator function for easily adding cooldown as
    a static time (integer) into skill's methods.

    Args:
        time: Cooldown of the method
        message: Optional message sent if there's still cooldown left

    Returns:
        Decorated method with a static cooldown
    """

    return cooldownf(lambda self, **eargs: time, message)


def cooldownf(fn, message=None):
    """Decorates a method to have a dynamic cooldown.

    Decorator function for easily adding cooldown as a dynamic time
    (function) into skill's methods. The function gets called when the
    cooldown is needed, and the skill is passed to the function.

    Args:
        fn: Function to determine the cooldown of the method
        message: Optional message sent if there's still cooldown left

    Returns:
        Decorated method with a dynamic cooldown
    """

    # Create a decorator using the function and message provided
    def method_decorator(method):

        # Create a wrapper method
        @wraps(method, assigned=WRAPPER_ASSIGNMENTS+('__dict__',), updated=())
        def method_wrapper(self, **eargs):

            # If the method's cooldown is over
            if method_wrapper.cooldown.remaining <= 0:

                # Restart the cooldown
                method_wrapper.cooldown.start(1, fn(self, **eargs))

                # And call the function
                return method(self, **eargs)

            # If there was cooldown remaining and a message is provided
            if message:

                # Format the provided message
                formatted_message = message.format(
                    name=self.name,
                    cd=method_wrapper.cooldown.remaining,
                    max_cd=method_wrapper.cooldown.limit
                )

                # And send it to the player
                SayText2(message=formatted_message).send(eargs['player'].index)

                # And exit with code 3
                return 3

        # Create the cooldown object for the wrapper
        method_wrapper.cooldown = TickRepeat(lambda: None)

        # And return the wrapper
        return method_wrapper

    # Return the decorator
    return method_decorator


def split_string(string, n):
    """Splits a string every n:th character.

    Args:
        string: String to split
        n: Amount of characters per splitted part
    """

    return [string[i:i + n] for i in range(0, len(string), n)]
 
def get_nearby_players(point, radius, is_filters='alive', not_filters=''):
    """Gets players near a point sorted by their distance to the point.		
	
    Args:		
        point: (x, y, z) coordinates of a 3D point		
        radius: Radius to look for the players		
        is_filters: PlayerIter's is_filters		
        not_filters: PlayerIter's not_filters

    Returns:		
        A list of players within the given radius from the given point,		
        sorted by their distance of the point.		
    """
    
    players = set()
    for player in PlayerIter(is_filters, not_filters, 'player'):
        if (point.get_distance(player.get_abs_origin()) <= radius):
            players.add(player)
    return sorted(players, key = lambda player: point.get_distance(player.get_abs_origin()))
 
def tell(message, *players):
    """Send message to a player or to everyone on server

    Args:
        message: Message to send
        player: Player objects that will get the message, 
        empty if message was sent to anyone on server
    """
    if players:
        SayText2(message=message).send([player.index for player in players])
    else:
        SayText2(message=message).send()
