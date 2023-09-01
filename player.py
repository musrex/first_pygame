import random

class Player():
    def __init__(self) -> None:
        '''Initializes the player
        Here we set player attributes,
        like health, inventory, and current weapon'''
        self.health = 100
        self.inventory = []
        self.current_weapon = None

    def equip(self, weapon) -> None:
        '''Equips a weapon to the player
        This will set the current_weapon attribute to the weapon passed in'''
        self.current_weapon = weapon

    def use_weapon(self, target) -> None:
        '''Uses the current weapon
        This will call the use method on the current weapon
        Parameters: target, can be player or enemy'''
        if self.current_weapon:
            self.current_weapon.use(target)

    def heal(self) -> None:
        '''Heals the player
        This will increase the health of the player, or enemy subclass.'''
        if self.health < 100:
            self.health += 10
        if self.health > 90:
            self.health = 100

    def move_closer(self, target) -> None:
        '''Moves the player closer to the target
        This will reduce the distance between the player and the target
        Parameters: target, can be player or enemy'''
        target.distance -= 10

    def move_away(self, target) -> None:
        '''Moves the player away from the target
        This will increase the distance between the player and the target
        Parameters: target, can be player or enemy'''
        target.distance += 10

class Enemy(Player):
    def __init__(self) -> None:
        '''Initializes the enemy
        Here we set enemy attributes,
        like health, distance from player, and current weapon'''
        super().__init__()
        self.health = 100
        self.current_weapon = Blaster()
        self.distance = 100

    def use_weapon(self, target) -> None:
        '''Uses the current weapon
        Parameters: target, can be player or enemy'''
        if self.current_weapon:
            self.current_weapon.use(target)

class Weapon():
    def __init__(self) -> None:
        '''Initializes the weapon.
        Fine tune specific weapon attributes in their subclasses'''
        self.ammo = 0
        self.damage = 0
        self.accuracy = 0
        self.range = 0

    def use(self, target) -> None:
        '''Uses the weapon on the target
        This will reduce the ammo of the weapon
        and reduce the health of the target.
        It will also calculate if the weapon hit the target
        based on range, accuracy, and a random number.
        Parameters: target, can be player or enemy'''
        if self.ammo <= 0:
            return False # Weapon out of ammo
        
        effective_accuracy = self.accuracy

        if isinstance(target, Enemy):
            if target.distance > self.range:
                effective_accuracy *= 0.1

        self.ammo -= 1
            
        if random.random() < effective_accuracy:
            target.health -= self.damage
            return True # Weapon hit

        return False # Weapon missed
        
'''Weapon subclasses
Fine tune specific weapon attributes here'''
class Blaster(Weapon):
    def __init__(self) -> None:
        super().__init__()
        self.ammo = 100
        self.damage = 10
        self.accuracy = 0.8
        self.range = 100

class Shotgun(Weapon):
    def __init__(self) -> None:
        super().__init__()
        self.ammo = 12
        self.damage = 50
        self.accuracy = 0.3
        self.range = 50

class Wrench(Weapon):
    def __init__(self) -> None:
        super().__init__()
        self.ammo = float('inf')
        self.damage = 75
        self.accuracy = 0.9
        self.range = 10

def range_check(weapon, target) -> bool:
    if weapon.range < target.distance:
        return False
    return True

def enemy_turn(player, enemy) -> bool:
    '''This function will run the enemy's turn
    This will check the enemy's health and distance from the player
    and decide what to do based on that.
    Parameters: player, the player object and enemy, the enemy object.'''
    if enemy.health <= 50:
        return random.choice([player.move_away(enemy), enemy.use_weapon(player)])
    
    if enemy.health <= 25:
        return random.choice([enemy.heal(), player.move_away(enemy), enemy.use_weapon(player)])
    
    if range_check(enemy.current_weapon, enemy):
        return enemy.use_weapon(player)
    
    return player.move_closer(enemy)

def equip_weapon(player) -> None:
    '''This function will equip a weapon to the player
    This will print out the inventory and ask the player to choose a weapon to equip.
    Parameters: player, the player object.'''
    print(f'''-----------------------
Inventory:
1. Blaster
2. Shotgun
3. Wrench
-----------------------
What do you want to equip? 
(Enter a number)''')
    choice = input('> ')
    match choice:
        case '1':
            player.equip(Blaster())
        case '2':
            player.equip(Shotgun())
        case '3':
            player.equip(Wrench())
    

def main() -> None:
    player = Player()
    enemy = Enemy()

    print(f'''You are approached by a dangerous enemy!''')
    running = True
    while running:
        print(f'''-----------------------
Player health: {player.health}
Enemy health: {enemy.health}
Enemy distance: {enemy.distance}
-----------------------
What do you want to do?
(Enter a number)
1. Move closer
2. Move away
3. Use weapon
4. Equip weapon
5. Heal''')
        choice = input('> ')
        match choice:
            case '1':
                player.move_closer(enemy)
            case '2':
                player.move_away(enemy)
            case '3':
                player.use_weapon(enemy)
            case '4':
                equip_weapon(player)
            case '5':
                player.heal()
        if player.health <= 0:
            print('You died!')
            running = False
            break
        if enemy.health <= 0:
            print('You won!')
            running = False
            break

        enemy_turn(player, enemy)

if __name__ == '__main__':
    main()