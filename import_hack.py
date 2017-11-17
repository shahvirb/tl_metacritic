GAME_TITLES = """
Portal 2
Borderlands 2
Dying Light
Torchlight II
Left 4 Dead 2
Dead Rising
Dragon Quest Heroes 2
Double Dragon Neon
How to Survive
Alien Swarm
Cry of Fear
Hammerwatch
Streets of Rogue
Awesomenauts
Divinity: Original Sin
Survivalist
Iron Brigade
Battleblock Theater
Castle Crashers
Magicka
The Red Solstice
Lost Castle
Rampage Knights
Shadowrun Chronicles - Boston Lockdown
Monaco
Abyss Odyssey
Binary Domain
Payday
Saints Row
Sanctum
Killing Floor
System Shock 2
F.E.A.R. 3
Dead Space 3
Resident Evil series
Terraria, Starbound, Creativerse, Minecraft
Moon Hunters
20XX
Baldur's Gate, Icewind Dale, and Planescape: Torment
Gauntlet
Forced
Titan Quest
Risk of Rain
ibb & obb
The Forest
Don't Starve Together
Dungeon Defenders
E.Y.E. Divine Cybermancy
Serious Sam
TowerFall Ascension
Orcs Must Die 2
Warhammer: Vermintinde
Lord of the Rings: War in the North
Trine
Factorio
BroForce
Duck Game
"""

def get_titles():
    titles = []
    for gt in GAME_TITLES.split('\n'):
        if gt:
            titles.append({'title':gt, 'url':''})
    return titles

def main():
    for i, gt in enumerate(get_titles()):
        print('{0} {1}'.format(i, gt['title']))

if __name__ == '__main__':
    main()