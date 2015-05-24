from hw.entities import Hero, Skill

from hw.tools import chance, chancef
from hw.tools import tell
from hw.tools import get_nearby_players

from effects import temp_entities

from filters.recipients import RecipientFilter
from mathlib import Vector


class undeadScourge(Hero):
    name = 'Undead Scourge'
    description = 'Vampiric Aura|Unholy Aura|Levitation|Suicide Bomber'
    authors = ('Kryptonite [WCS team]')
    
@undeadScourge.skill
class VampiricAura(Skill):
    name = 'Vampiric Aura'
    description = 'Gives you a 60% chance to gain 16-30% of the damage you do in attack, back as health'
    max_level = 8
    
    @chance(60)
    def player_attack(self, **eargs):
        player = eargs['attacker']
        enemy = eargs['defender']
        leechPercent = 0.14 + self.level * 0.02
        leeched = int(eargs['damage']*(leechPercent))
        player.health += leeched
        tell('Leeched {} health'.format(leeched), player)
        tell('Lost {} health by Vampiric Aura'.format(leeched), enemy)
        
        
@undeadScourge.skill
class UnholyAura(Skill):
    name = 'Unholy Aura'
    description = 'Gives you a speed boost, 8-36% faster'
    max_level = 8
    
    def player_spawn(self, player, **eargs):
        speed = 0.08 + self.level * 0.04
        player.speed += speed
        tell('Unholy Aura activated', player)
        
        
@undeadScourge.skill
class Levitation(Skill):
    name = 'Levitation'
    description = 'Allows you to jump higher by reducing your gravity for 8-64%'
    max_level = 8
    
    def player_spawn(self, player, **eargs):
        gravityReduce = 0.08 * self.level
        player.gravity = 1 - gravityReduce
        tell('Levitation has been set.', player)

@undeadScourge.skill
class SuicideBomber(Skill):
    name = 'Suicide Bomber'
    description = 'On death, you have a 20-70% chance to explode and make 70-160 damage on each player in 12-18 feet range'
    max_level = 8
    
    @chancef(lambda self, **kwargs:(20, 30, 40, 45, 50, 55, 60, 70)[self.level-1])
    def player_death(self, **eargs):
        radius = (0, 120, 120, 140, 160, 170, 170, 180, 180)[self.level]
        magnitude = (0, 80, 80, 90, 100, 110, 120, 120, 130)[self.level]
        damage = radius*magnitude/150
        player = eargs['defender']
        team = player.get_team()
        temp_entities.explosion(RecipientFilter(), 0, player.get_abs_origin(), 0, 1, 255, 0, radius, magnitude, Vector(), ord('C'), )
        if (team >= 2):
            damaged = 0
            for enemy in get_nearby_players(player.get_abs_origin(), radius, not_filters=['ct', 't'][3-team]):
                enemy.take_damage(damage, attacker_index = player.index)
                damaged += 1
            if damaged > 0: 
                tell('You damaged {} enemies for {} damage each'.format(damaged, damage), player)

