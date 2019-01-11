"""
This file contains the Monster class.

The Monster class encapsules the data for a monster character.
"""

class Monster:
    def __init__(self, monster):
        self.health = monster['health']
        self.strength = monster['strength']
        self.dexterity = monster['dexterity']
        self.monster_type = monster['monster_type']
        self.description = monster['description']

    def display_stats(self):
        """Return the monster's health, strenght, and dexterity."""
        output = ('Monster: {} - Health: {} - Strength: {} - Dexterity: {}'
                 .format(self.monster_type, self.health, self. strength, 
                      self.dexterity))

        return output
 