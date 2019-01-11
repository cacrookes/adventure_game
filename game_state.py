"""
This file contains the GameState class.

The GameState class contains persistent player and game attributes.
"""

class GameState:
    def __init__(self):
        self.health = 100
        self.experience = 1
        self.inventory = ['Sword', 'Shield']
        self.location = 'field'
        self.game_over = False
        self.been_to_town = False

    def display_stats(self):
        """Print out the user's health, experience, and inventory."""
        print('You are equiped with: ' + 
              ', '.join([x for x in self.inventory]))
        print('Your health is: {}'.format(self.health))
        print('You have {} experience points'.format(self.experience))

    def increase_experience(self):
        """Increment the player's experience by 1."""
        self.experience += 1
