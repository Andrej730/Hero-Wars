# ======================================================================
# >> CUSTOM EVENTS
# ======================================================================

# Source.Python
from events.custom import CustomEvent

from events.resource import ResourceFile
from events.variable import StringVariable
from events.variable import ShortVariable


# ======================================================================
# >> ALL DECLARATION
# ======================================================================

__all__ = (
    'Hero_Pre_Level_Up',
    'Hero_Level_Up',
    'Player_Ultimate'
)


# ======================================================================
# >> EVENT CLASSES
# ======================================================================

class Hero_Pre_Level_Up(CustomEvent):
    cid = StringVariable("Hero's class' id")
    id = StringVariable("Hero's unique Python id")


class Hero_Level_Up(CustomEvent):
    cid = StringVariable("Hero's class' id")
    id = StringVariable("Hero's unique Python id")
    player_index = ShortVariable("Player's index")
    player_userid = ShortVariable("Player's userid")


class Player_Ultimate(CustomEvent):
    index = ShortVariable("Player's index")
    userid = ShortVariable("Player's userid")


# ======================================================================
# >> CREATE RESOURCE FILE
# ======================================================================

def load():
    """Create a resource file upon plugin loading."""
    resource_file = ResourceFile(
        'hw', Hero_Pre_Level_Up, Hero_Level_Up, Player_Ultimate
    )
    resource_file.write()
    resource_file.load_events()
