#!/usr/bin/env python3

"""
This script runs a simple text based choose your own adventure style game.
It is an assignment for Udacity's Intro to Programming Nanodegree.

Written by: Christopher Crookes
"""

import time
import random
from game_state import GameState as gs
from monster import Monster as mn


def print_sleep(text_to_print, seconds):
    """Print text to the console and wait a specified number of seconds.

    print_sleep will print to the console text that has been passed in.
    It will then wait the number of seconds passed in by the user.

    Args:
    text_to_print - (string) text that will be printed to the console.

    seconds - (int) the number of seconds to wait before exiting the funciton.

    Returns:
    none
    """
    print(text_to_print)
    time.sleep(seconds)


def present_choice(choices):
    """Present the user a list of choices.

    present_choice prints a list of choices to the screen and waits for user
    input. The prompt is repeated until the user inputs one of the choices in
    the list. Once a valid choice has been made, the choice is returned.

    Args:
    choices - (list of strings) a list of items that will be printed to the
              screen. Each item in the list must be a string.

    Returns
    A string containing the user's choice.
    """
    while True:    
        prompt = '(Please enter ' + choices[0]
        for choice in choices[1:]:
            prompt += ' or ' + choice
        prompt += ')'

        print(prompt)
        answer = input()
        if answer in choices:
            break

    return answer


def open_field(game):
    """The starting location of the game."""

    print_sleep('You are in an open field.', 1)
    print_sleep('There is a large, ominous castle up ahead. There is a quaint '
          'town to your right', 1)
    print('*' * 25)
    print('Press 1 to go to the castle.')
    print('Press 2 to go to the town.')
    print('*' * 25)
    answer = present_choice(['1', '2'])
    if answer == '1':
        location = 'castle'
    elif answer == '2':
        location = 'town'

    game.location = location
    game.game_over = False


def castle(game):
    """Handle the castle area of the game.

    The castle is where the user will face Timmy the terrible and his
    henchmen."""
    print_sleep('You are at the gate of a large castle.', 1)
    if 'Stake' not in game.inventory:
        print_sleep('You notice a wooden stake laying in the grass to your '
                    'side. That may come it handy for killing vampires!', 1)
        print('*' * 25)
        print('Press 1 to go pick up the stake.')
        print('Press 2 to leave the stake. Who knows where its been!')
        print('*' * 25)
        answer = present_choice(['1', '2'])
        if answer == '1':
            game.inventory.append('Stake')

    print_sleep('You enter through the gate into the main hall.', 1)
    random_monster = random.randint(1, 3)
    switcher = {
        1: {'monster_type': 'Werewolf',
            'description': ('Strong and fast, the Werewolf is one of the '
                            'deadliest monsters in the realm. Only the most '
                            'experienced warriors dare fight one.'),
            'health': 100,
            'strength': 35,
            'dexterity': 30
           },
        2: {'monster_type': 'Ogre',
            'description': ('Strong and resilient, the Ogre can crush a man '
                            'in a single blow and can withstand a beating. '
                            'However if you dodge this lumbering beast\'s '
                            'clumsy strikes, you may have a chance.'),
            'health': 200,
            'strength': 100,
            'dexterity': 15
           },
        3: {'monster_type': 'Bunny',
            'description': ('These cute little balls of pure evil don\'t '
                            'look like much of a threat. One solid whack '
                            'will take them out. That is if you can keep up '
                            'with the speedy little critters.'),
            'health': 5,
            'strength': 1,
            'dexterity': 70
           }
    }
    monster = mn(switcher[random_monster])

    print_sleep('Your blood curdles as you sense the presence of evil '
                'lurking in the shadows.', 1)
    print_sleep('Rushing out to greet you is one of Timmy\'s henchmen. '
                'It\'s a {}!'.format(monster.monster_type), 1)
    print_sleep(monster.description, 1)
    
    battle_system(game, monster)

    game.location = 'field'


def battle_system(game, monster):
    """Handle battles between the player and monsters."""
    print_sleep('*** BATTLE!!!! ***', 1)
    while True:
        print_sleep('Your Health: {}'.format(game.health), 1)
        print_sleep(monster.display_stats(), 1)
        print('*' * 25)
        print('Press 1 to attack the {}.'.format(monster.monster_type))
        print('Press 2 to cowardly run away.')
        print('*' * 25)
        answer = present_choice(['1', '2'])
        if answer == '1':
            hit_chance = random.randint(1, 100)
            if hit_chance < (100 - monster.dexterity + 2 * game.experience):
                damage = random.randint(30, 70) + 2*game.experience
                print_sleep('You landed a hit with {} damage!'
                            .format(damage), 1)
                print_sleep('Your experience has increased.', 1)
                game.increase_experience()
                monster.take_damage(damage)
                if not monster.still_alive():
                    print_sleep('You\'ve slain the {}!'
                                .format(monster.monster_type), 1)
                    break
            else:
                print_sleep('You missed!', 1)

        elif answer == '2':
            dash_chance = random.randint(1, 100)
            if dash_chance < (100 - monster.dexterity + 2 * game.experience):
                print_sleep('Phew, that was close! You successfully escaped',
                             1)
                print_sleep('Your experience has increased.', 1)
                game.increase_experience()
                game.location = 'field'
                break
            else:
                print_sleep('Oh no! The {} blocked your escape!'
                            .format(monster.monster_type), 1)

        print_sleep('The {} attacks you!'.format(monster.monster_type), 1)
        defend_chance = random.randint(1, 100)
        if defend_chance < (100 - monster.dexterity + 2 * game.experience):
            print_sleep('The {} missed!'.format(monster.monster_type), 1)
            print_sleep('Your experience has increased.', 1)
            game.increase_experience()
        else:
            print_sleep('You\'ve been hit!', 1)
            print_sleep('The {} did {} damage'
                        .format(monster.monster_type, monster.strength), 1)
            game.take_damage(monster.strength)
            if not game.still_alive():
                print_sleep('You\'ve died!', 1)
            break


def town(game):
    """Handle the town area game play.

    In the town, the user can rest at the inn to recuperate their health,
    or aquire items at the market.
    """
    location = 'town'
    print_sleep('You enter a quiet, subdued town', 1)

    if not game.been_to_town:
        print_sleep('You are greeted by an official looking individual.', 1)
        print_sleep('"Thank the gods you came. I am the mayor of this town. '
                    'If you can rid of Timmy the Terrible, we will pay you '
                    '100 gold."', 1)
        print_sleep('"Feel free to rest in the inn if you need to recuperate."', 1)
        print_sleep('"You may help yourself to anything useful to your quest '
                    'in the market."', 1)
        game.been_to_town = True

    print('*' * 25)
    print('Press 1 to go to the inn.')
    print('Press 2 to go to the market.')
    print('Press 3 to leave the town.')
    print('*' * 25)
    answer = present_choice(['1', '2', '3'])
    if answer == '1':
        print_sleep('What a great sleep! Your health is back to 100.', 1)
        game.health = 100
    elif answer == '2':
        market(game)
    elif answer == '3':
        location = 'field'

    game.location = location


def market(game):
    """Handle the market area game play.

    The market is where the user can acquire items that may help them on 
    their quest.
    """
    if {'turnip', 'garlic'}.intersection(game.inventory):
        print_sleep('"We are all sold out now. Sorry! '
                    'Please save our town!"', 1)
    else:
        print_sleep('"Brave warrior, '
                    'help yourself to whatever you fancy."', 1)
        print_sleep('"We have the juiciest turnips, and the '
                    'strongest garlic.', 1)
        print('*' * 25)
        print('Press 1 to go to take a turnip.')
        print('Press 2 to go to take some garlic.')
        print('Press 3 to leave the market.')
        print('*' * 25)
        answer = present_choice(['1', '2', '3'])
        if answer == '1':
            print_sleep('You have added a turnip to your inventory!', 1)
            game.inventory.append('turnip')
        if answer == '2':
            print_sleep('You have added garlic to your inventory!', 1)
            game.inventory.append('garlic')
        if answer != '3':
            print_sleep('Your experience has increased.', 1)
            game.increase_experience()


def opening_scene():
    """Present the text for the opening scene."""
    print('\n\n\n')
    print(' ' * 20 + '*' * 60)
    print(' ' * 20 + '**{:^56}**'.format('Adventure Game: Timmy the Terrible'))
    print(' ' * 20 + '**{:^56}**'.format('Developed by: Christopher Crookes'))
    print(' ' * 20 + '**{:^56}**'.format('For: Udacity IPND'))
    print(' ' * 20 + '*' * 60)
    print_sleep('\n\n\n', 2)

    print_sleep('Welcome young warrior! The local town needs your help. '
                'They are being terrorized by Timmy the Terrible!', 1)
    print_sleep('Although you are an experience monster hunter, this will be '
                'your biggest challenge yet. Timmy the Terrible is an '
                'ancient, powerful vampire.', 1)
    

def main():
    game = gs()

    opening_scene()
    game.display_stats()
    while not game.game_over:
        switcher = {
            'field': open_field,
            'castle': castle,
            'town': town
        }
        switcher[game.location](game)


if __name__ == '__main__':
    main()
