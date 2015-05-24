# ======================================================================
# >> IMPORTS
# ======================================================================

# Hero-Wars
from hw.entities import Hero, Skill

#Source.Python
from filters.players import PlayerIter

from colors import Color

class humanAlliance(Hero):
    name = "Human Alliance"
    description = "Invisibility|Devotion Aura|Bash|Teleport"
    authors = ('Kryptonite [WCS team]')

@humanAlliance.skill
class Invisibility(Skill):
    name = 'Invisibility'
    description = 'Makes you partially invisible, 62-37%'
    max_lvl = 8
    
    def player_spawn(self, player):
        player.get_color()

@humanAlliance.skill
class DevotionAura(Skill):
    name = 'Devotion Aura'
    description = 'Gives your team additional 15-50 health each round'
    max_lvl = 8
    
    def player_spawn(self, player):
        extraHealth = (15, 20, 25, 30, 35, 40, 45, 50)[self.lvl-1]
        team = player.team
        for player in PlayerIter(['ct', 't'][3-team], return_types='player'):
            player.health += extraHealth
        tell('#green: Devotion Aura #lightgreenactivated.', player)


@humanAlliance.skill
class Bash(Skill):
    name = 'Bash'
    description = 'Have a 15-32% chance to render an enemy immobile for 1 second'
    max_lvl = 8
    
    def player_attack(self, **eargs):
        player = eargs['attacker']
        enemy = eargs['defender']
        
@humanAlliance.skill
class Teleport(Skill):
    name = 'Teleport'
    description = 'Allows you to teleport to where you aim, \nrange is 60-108 feet'
    max_lvl = 8
    
    def player_ultimate(self, player):
        pass