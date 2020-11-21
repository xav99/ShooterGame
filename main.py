import os
import pygame
import random
from colours import *
from CustomExceptions import *
from upgrades import *
import playsound


class Setup:
    # SCREEN
    pygame.init()
    pygame.font.init()
    WIDTH, HEIGHT = (750, 750)
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100, 30)  # window position
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # Screen size
    pygame.display.set_caption('RPG')  # Form title
    sound = True
    try:
        bullet_sfx = pygame.mixer.Sound("Sounds/Bullet.wav")
        missile_sfx = pygame.mixer.Sound("Sounds/Missile.wav")
        ray_of_light_sfx = pygame.mixer.Sound("Sounds/RayOfLightsfx.wav")
        nuke_sfx = pygame.mixer.Sound("Sounds/Nuke.wav")
    except:
        print("sound not available")
        sound = False

    # EXTRAS
    PLAYER_GRAVE = (1000, -1000)
    ENEMY_GRAVE = (-1000, 1000)
    gold = 0
    diamonds = 0
    time_bonus = [0]
    time_index = 0

'''
Notes:
- Gamemodes
- Saves
'''

class NewSprite:
    '''
    Create a new sprite
    '''
    def __init__(self, x, y, width=50, height=50, speed=2, hp=100, colour=red):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.hp = hp
        self.orig_colour = colour
        self.colour = colour
        self.invinsible = False
        self.status = None
        self.sprite_type = None
        self.bonus_type = None # type of bonus to recieve (time or gold/diamonds)
        self.bonus = None # bonus recieved when killed (gold/ diamonds or time)
        self.initAssign()

    def draw(self, window, shape="rect"):
        '''
        Draws the sprite to the chosen window
        :param window: the window to add the sprite to
        :param shape: shape of the sprite
        '''
        if shape == "rect":
            pygame.draw.rect(window, self.colour, (self.x, self.y, self.width, self.height))
        elif shape == "circle":
            pygame.draw.circle(window, self.colour, (self.x, self.y), self.width)
        else:
            print("INVALID SHAPE")
            exit()

    def initAssign(self):
        '''
        Assigns values to status and sprite_type in order to keep init clean and free of statements
        '''
        self.checkStatus(False) # assign status
        if self.colour == blue or self.colour == green: # assign sprite_type
            self.sprite_type = "player"
        else:
            self.sprite_type = "enemy"

    def assignBonus(self, bonustype): # FIX
        '''
        Bonus to give when an enemy is killed
        :param bonustype: type of bonus to recieve (gold/ diamonds or time)
        
        '''
        self.bonus_type = bonustype
        if self.bonus_type != "gold" and self.bonus_type != "diamond" and self.bonus_type != "time":
            raise StandardExceptions.InvalidOperationException("Bonus_type is invalid")
        
    def giveBonus(self, bonus): # FIX
        '''
        Gives the bonus when an enemy is killed
        :param bonus: bonus to give every time an enemy is killed
        '''
        self.bonus = bonus
        if self.bonus_type == "gold":
            pass
        elif self.bonus_type == "diamond":
            pass
        elif self.bonus_type == "time":
            Setup.time_bonus.append(bonus)
            Setup.time_index +=1
            Setup.time_bonus[Setup.time_index]+= Setup.time_bonus[Setup.time_index-1]
        else:
            raise StandardExceptions.InvalidOperationException("Bonus_type is invalid")

    def move(self, x, y, replace=True):
        '''
        Teleports the sprite to the specified position
        :param x: x-position to move sprite
        :param y: y-position to move sprite
        :param replace: True- Changes the position to the specified position |
                        False- Changes the position by the specified amount
        '''
        if replace:
            self.x = x
            self.y = y
        else:
            self.x += x
            self.y += y

    def travel(self, x, y):
        '''
        Travels to the enemy instead of teleporting (like move does)
        :param x: x-position to move sprite
        :param y: y-position to move sprite
        '''
        if self.x != x:
            if self.x < x:
                self.x += self.speed
            elif self.x > x:
                self.x -= self.speed
        if self.y != y:
            if self.y < y:
                self.y += self.speed
            elif self.y > y:
                self.y -= self.speed
        
    def getCoords(self):
        '''
        Returns the sprites' coordinates 
        '''
        return self.x, self.y

    def changeSpeed(self, speed, replace=True):
        '''
        Changes the movement speed of the sprite
        :param speed: amount of speed to change to
        :param replace: True- Changes the speed to the specified amount |
                        False- Changes the speed by the specified amount
        '''
        if replace:
            self.speed = speed
        else:
            self.speed += speed

    def changeHp(self, hp, replace=True ,cleanup=True, retrieval=False):
        '''
        Changes the hp of the sprite
        :param hp: amount of hp to change to
        :param replace: True- Changes the hp to the specified amount |
                        False- Changes the hp by the specified amount
        :param cleanup: passes the arg to checkStatus
        :param retrieval: passes the arg to checkStatus
        '''
        if not self.invinsible:
            if replace:
                self.hp = hp
            else:
                self.hp += hp
            self.checkStatus(cleanup, retrieval)

    def setInvinsibility(self, status: bool):
        '''
        :param status: (bool) changes the invinsibility status to the one specified (True or False)
        '''
        self.invinsible = status

    def changeColour(self, colour):
        '''
        Changes the colour of the sprite
        :param colour: colour to change to
        '''
        self.colour = colour

    def checkStatus(self, cleanup=True, retrieval=False):
        '''
        Checks the status of the sprite on whether it is 'alive' or 'dead'
        :param cleanup: whether or not to send the player/enemy to the graveyard and change the colout to white if it has a status of dead
        :param retrieval: whether or not to change the colour back to the original colour and move the sprite back to the screen
                         (should be True if used to revive)
        '''
        if self.hp >= 1:
            self.status = "alive"
            if retrieval:
                self.colour = self.orig_colour
                self.move(random.randint(0, Setup.WIDTH-self.width), random.randint(0, Setup.HEIGHT-self.height))
        else:
            self.status = "dead"
            if cleanup:
                self.changeColour(white)
                if self.sprite_type == "player":
                    self.move(Setup.PLAYER_GRAVE[0], Setup.PLAYER_GRAVE[1])
                else:
                    self.move(Setup.ENEMY_GRAVE[0], Setup.ENEMY_GRAVE[1])
                if self.bonus_type is not None: # FIX
                    self.giveBonus(10) #bonus given upon kill (move to Gamemode class upon gamemoden being chosen)

        return self.status

    def createCollision(self, *target, **extras):
        '''
        :param target: the target(s) to set the collision with
        :param extras: extra options if a collision occurs
            valid extras:
                func: calls a func if a collision occurs (func must be called with its corresponding number order (example: first func must be called 'func1'))
                    example:
                        extras={"func1": gg} # it will call function gg
                args: passes the args to the corresponding function based on its number (example: 'args1' will be passed as args to 'function1'
                warning: the 'args(number)' arguments must be put in a tuple and always have a comma after the last arg. The 'args(number)' argument must also
                         be put after its corresponding func number
                            example:
                                  'func1': gg, 'arg1: ('h',), 'func2': hh, 'arg2': ('jj', 'bb',)
        '''
        count = 0
        func = None # which function will be called each time 'func' is mentioned as an extra
        eval1 = False
        #eval2 = False
        for i in target:
            if self.x + self.width > i.x and self.x < i.x + i.width and self.y + self.width > i.y and self.y < i.y \
                + i.height and current_loadout["weapon_loadout"]["current_weapon"] != weapon_list[3]: # if a collision occurs
                    eval1 = True # normal collision
            elif self.x + self.width > i.x and self.x < i.x + i.width and self.y + self.width > i.y and self.y - self.width < i.y \
                    + i.height and current_loadout["weapon_loadout"]["current_weapon"] == weapon_list[1]:
                eval1 = True # expand bullet collision ( first/second collision had logic error when used with expand bullet)
            elif self.x + self.width > i.x and self.x < i.x + i.width and self.y + self.height > i.y and self.y < i.y \
                    + i.height and current_loadout["weapon_loadout"]["current_weapon"] == weapon_list[3]:
                eval1 = True # ray of light collision ( first collision had logic error when used with ray of light)

            if eval1:
                for k, v in extras.items():
                    for kk, vv in v.items():
                        if "func" in kk: # calculating amount of funcs being passed as a parameter
                            count += 1

                        if kk == "func" + str(count): # func number must be in correspondance with arg number (example: 'func1': gg, 'arg1: ('h',), 'func2': hh, 'arg2': ('jj', 'bb', )
                            if "args" + str(count) in v.keys():
                                func = vv  # if args are found it will wait until we get to args with the corresponding number before we call the func (the args corresponding number MUST be right after the func)
                            else:
                                vv() # if no args are passed, func will be called without args
                        elif kk == "args" + str(count):
                            func(*vv)  # calls func with all parameters (parameters must be put in a tuple and always have a comma after the last arg)

    def kill(self):
        '''
        Kill the sprite
        '''
        self.changeHp(0)

    def revive(self, hp=100):
        '''
        Revive the sprite
        '''
        self.changeHp(hp, retrieval=True)


class ItemSprite(NewSprite):
    '''
    Create a new item
    '''
    def __init__(self, x, y, width=50, height=50, speed=7, hp=0, colour=green, damage=25):
        super().__init__(x, y, width=width, height=height, speed=speed, hp=hp, colour=colour)
        self.damage = damage
        self.projectileAttached = True

    def levelConfig(self):
        '''
        Assign the speed and damage based on the item level
        '''
        if current_loadout["weapon_loadout"]["current_weapon"] == weapon_list[0]:
            self.width += current_loadout["weapon_loadout"]["weapon_level"]["bigger_bullets"] # addiitonal width of + level
            self.damage += current_loadout["weapon_loadout"]["weapon_level"]["bigger_bullets"] * 5  # additional damage of + level * 5
            self.speed += current_loadout["weapon_loadout"]["weapon_level"]["faster_bullets"] # addiitonal speed of + level
        elif current_loadout["weapon_loadout"]["current_weapon"] == weapon_list[1]:
            self.damage += current_loadout["weapon_loadout"]["weapon_level"]["bigger_bullets"] * 5  # additional damage of + level * 5
            self.speed += current_loadout["weapon_loadout"]["weapon_level"]["faster_bullets"]  # addiitonal speed of + level
        elif current_loadout["weapon_loadout"]["current_weapon"] == weapon_list[2]:
            self.damage += current_loadout["weapon_loadout"]["weapon_level"]["bigger_bullets"] # additional damage of + level
            self.speed += int(round(current_loadout["weapon_loadout"]["weapon_level"]["faster_bullets"] / 2, 0))  # additional speed of + level /2 (rounded)
            if current_loadout["weapon_loadout"]["weapon_level"]["bigger_bullets"] % 5 == 0 and current_loadout["weapon_loadout"]["weapon_level"]["bigger_bullets"] > 0:
                self.width += 1
            elif current_loadout["weapon_loadout"]["weapon_level"]["bigger_bullets"] % 10 == 0 and current_loadout["weapon_loadout"]["weapon_level"]["bigger_bullets"] > 0:
                self.width += 3
        elif current_loadout["weapon_loadout"]["current_weapon"] == weapon_list[3]:
            self.damage += current_loadout["weapon_loadout"]["weapon_level"]["bigger_bullets"] * 50 # additional damage of + level * 50
            self.speed += current_loadout["weapon_loadout"]["weapon_level"]["faster_bullets"] * 2 # additional speed of + level * 2
            if current_loadout["weapon_loadout"]["weapon_level"]["bigger_bullets"] % 10 != 0:
                self.height += current_loadout["weapon_loadout"]["weapon_level"]["bigger_bullets"] # additional height of + level * 5
            elif current_loadout["weapon_loadout"]["weapon_level"]["bigger_bullets"] % 10 == 0 and current_loadout["weapon_loadout"]["weapon_level"]["bigger_bullets"] > 0:
                self.height *= 2

    def changeDamage(self, damage, replace=True):
        '''
        :param damage: amount to change the damage by
        :param replace: True- Changes the damage to the specified amount |
                        False- Changes the damage by the specified amount
        '''
        if replace:
            self.damage = damage
        else:
            self.damage == damage


def main():
    # operations
    run = True
    fps = 60
    cutEvent = 0  # use to cut event in pygame as the event repeats more than once when a key is pressed
    game_modes = ["level_mode", "time_mode", "survival_mode"]
    gamemode = game_modes[0]
    level = 1
    clock = pygame.time.Clock()
    main_font = pygame.font.SysFont("ariel", 20)
    player = NewSprite(10, 10, 30, 30, colour=blue)
    recently_hit = [False, 0]

    # weapons
    single_shot = ItemSprite(int(player.x+player.width/2), int(player.y+player.height/2), 3)
    expand_shot = ItemSprite(int(player.x+player.width/2), int(player.y+player.height/2), 5)
    stalker_missile = ItemSprite(int(player.x+player.width/2), int(player.y+player.height/2), 5, speed=5, damage=50)
    ray_of_light = ItemSprite(int(player.x+player.width/2), int(player.y+player.height/2), 5, 15, damage=500, speed=30)

    # powerups
    nuke = ItemSprite(int(Setup.WIDTH/2), int(Setup.HEIGHT/2), 3, colour=white)

    # weapon assignment
    playerProjectile = None
    if current_loadout["weapon_loadout"]["current_weapon"] == weapon_list[0]:
        playerProjectile = single_shot
    elif current_loadout["weapon_loadout"]["current_weapon"] == weapon_list[1]:
        playerProjectile = expand_shot
    elif current_loadout["weapon_loadout"]["current_weapon"] == weapon_list[2]:
        playerProjectile = stalker_missile
    elif current_loadout["weapon_loadout"]["current_weapon"] == weapon_list[3]:
        playerProjectile = ray_of_light
        playerProjectile.changeColour(yellow)

    #config
    playerProjectile.levelConfig()
    player.changeSpeed(int(round(current_loadout["attribute_loadout"]["attribute_level"]["player_speed_increase"]/2.5,0)), replace=False)
    player.changeHp(current_loadout["attribute_loadout"]["attribute_level"]["player_hp_increase"]*100, replace=False)
    print(player.speed)
    def refresh():
        '''
        Updates the display and displays all the objects
        '''
        global current_time
        Setup.WIN.fill(white)
        current_time = round(pygame.time.get_ticks()/1000, 2) # FIX BONUS (+ Setup.time_bonus[Setup.time_index])
        hp_label = main_font.render(f"HP: {str(player.hp)}", 1, green)
        level_label = main_font.render(f"Level: {str(level)}", 1, blue)
        clock_label = main_font.render(str(current_time), 1, black)


        Setup.WIN.blit(hp_label, (10, 10))
        Setup.WIN.blit(level_label, (Setup.WIDTH/2, 10))
        Setup.WIN.blit(clock_label, (Setup.WIDTH-80, 10))

        if current_loadout["weapon_loadout"]["current_weapon"] != weapon_list[3]:
            playerProjectile.draw(Setup.WIN, "circle")
        else:
            playerProjectile.draw(Setup.WIN, "rect")
        player.draw(Setup.WIN)
        nuke.draw(Setup.WIN, "circle")
        for i in enemies:
            i.draw(Setup.WIN)
            i.assignBonus("time") # FIX

        pygame.display.update()

    def resetProjectile():
        '''
        Resets projectile location to inside the player
        '''
        playerProjectile.x = int(player.x+player.width/2)
        playerProjectile.y = int(player.y+player.height/2)
        playerProjectile.projectileAttached = True
        if current_loadout["weapon_loadout"]["current_weapon"] == weapon_list[1]:
            playerProjectile.width = 3
        elif current_loadout["weapon_loadout"]["current_weapon"] == weapon_list[3]: # if its ray of light equipped, resets its width
            playerProjectile.width = 15
            playerProjectile.y = int(player.y+player.height/2-playerProjectile.height/2)

    def uponBulletCollision(target):
        '''
        What should be done upon a bullet collision occuring
        '''
        target.move(10, 0, False)
        target.changeHp(target.hp - playerProjectile.damage)

    def uponPlayerCollision():
        '''
        Player loses 50 hp and gains invinsibility for 3 seconds upon being hit recently
        '''
        if not recently_hit[0]: # if you werent hit recently
            player.changeHp(player.hp - 50)
            player.setInvinsibility(True)
            recently_hit[0] = True
            recently_hit[1] = round(current_time, 1)

    def playerCollisionEffect():
        '''
        Player flashes colour upon being hit recently
        '''
        player.changeColour(grey)

    def resetColour():
        '''
        Changes player colour back to blue
        '''
        player.changeColour(blue)

    def resetPlayer():
        player.move(10, Setup.WIDTH/2)
        resetProjectile()

    def nukeExplosion():
        nuke.changeColour(orange)
        nuke.projectileAttached = False

    def resetNuke():
        '''
        Resets nuke
        '''
        nuke.projectileAttached = True
        nuke.width = 3
        nuke.changeColour(white)
        nuke.move(int(Setup.WIDTH / 2), int(Setup.HEIGHT / 2))

    def createEnemies():
        for i in range(1, (level * 5) + 2 - level -len(enemies)):
            globals().update({"enemy" + str(i): NewSprite(-100, -100, 25, 25)})
            enemies.append(globals()["enemy" + str(i)])
        for i in enemies:
            i.move(random.randint(70, Setup.WIDTH - i.width), random.randint(0, Setup.HEIGHT - i.height))

    enemies = []
    createEnemies()
    resetProjectile() # to centre ray of light

    while run:
        clock.tick(fps)
        refresh()

        for event in pygame.event.get():  # Gets any event that happens
            if event.type == pygame.QUIT:
                run = False
        # movement and boundaries
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and player.x + player.width < Setup.WIDTH:
            player.x += player.speed
            if playerProjectile.projectileAttached: # projectile will move with player if its attached
                playerProjectile.x += player.speed
        if keys[pygame.K_LEFT] and player.x > 0:
            player.x -= player.speed
            if playerProjectile.projectileAttached:
                playerProjectile.x -= player.speed
        if keys[pygame.K_UP] and player.y > 0:
            player.y -= player.speed
            if playerProjectile.projectileAttached:
                playerProjectile.y -= player.speed
        if keys[pygame.K_DOWN] and player.y + player.height < Setup.HEIGHT:
            player.y += player.speed
            if playerProjectile.projectileAttached:
                playerProjectile.y += player.speed
        if keys[pygame.K_SPACE]:
            playerProjectile.projectileAttached = False
            if Setup.sound:
                if current_loadout["weapon_loadout"]["current_weapon"] == weapon_list[0] or current_loadout["weapon_loadout"]["current_weapon"] == weapon_list[1]:
                    pygame.mixer.Sound.play(Setup.bullet_sfx)
                elif current_loadout["weapon_loadout"]["current_weapon"] == weapon_list[2]:
                    pygame.mixer.Sound.play(Setup.missile_sfx)
                elif current_loadout["weapon_loadout"]["current_weapon"] == weapon_list[3]:
                    pygame.mixer.Sound.play(Setup.ray_of_light_sfx)
        if keys[pygame.K_a]:
            for i in enemies:
                i.move(random.randint(0, Setup.WIDTH-i.width), random.randint(0, Setup.HEIGHT-i.height))
        if keys[pygame.K_n]: # nuke (create animation)
            if Setup.sound:
                pygame.mixer.Sound.play(Setup.nuke_sfx)
            nukeExplosion()
            cutEvent+=1
            for i in enemies:
                i.kill()
            if cutEvent >= 1:
                cutEvent = 0
                continue
        if keys[pygame.K_r]: # reload projectile (incase of bullet stuck)
            resetProjectile()
        for v in range(len(enemies)):
            player.createCollision(enemies[v], extras={'func1': uponPlayerCollision})
            playerProjectile.createCollision(enemies[v], extras={ "func1": resetProjectile, "func2": uponBulletCollision, 'args2': (enemies[v],)}) # must leave empty comma (,) in tuple (after the first arg) if theres only 1 arg

        if not playerProjectile.projectileAttached:
            if current_loadout["weapon_loadout"]["current_weapon"] == weapon_list[1]:
                if playerProjectile.width < 20 + current_loadout["weapon_loadout"]["weapon_level"]["bigger_bullets"]:
                    playerProjectile.width += 1
                playerProjectile.x += playerProjectile.speed
            elif current_loadout["weapon_loadout"]["current_weapon"] == weapon_list[2]:
                totalrange = {}
                for i in enemies:
                    if i.status == "alive":  # loops through all alive enemies
                        enemyrangex = abs(
                            playerProjectile.x - i.x)  # difference between the enemeies x range and the players bullet
                        enemyrangey = abs(
                            playerProjectile.y - i.y)  # difference between the enemeies y range and the players bullet
                        totalrange.update({enemyrangex + enemyrangey: i})
                chosenenemy = totalrange[min(totalrange)]  # the missile will go after the closest enemy
                playerProjectile.travel(chosenenemy.x, chosenenemy.y+chosenenemy.height/2)  # bullet travels to the closest enemy
            elif current_loadout["weapon_loadout"]["current_weapon"] == weapon_list[3]:
                if playerProjectile.x + playerProjectile.width  < Setup.WIDTH:
                    playerProjectile.width += playerProjectile.speed
            else:
                playerProjectile.x += playerProjectile.speed

        if not nuke.projectileAttached: # nuke explosion
            if nuke.width < Setup.WIDTH:
                nuke.width += 80
            else:
                resetNuke()

        if playerProjectile.x > Setup.WIDTH or current_loadout["weapon_loadout"]["current_weapon"] == weapon_list[3] and playerProjectile.x + playerProjectile.width >= Setup.WIDTH: # if bullet goes off screen
            playerProjectile.projectileAttached = True
            resetProjectile()

        if recently_hit[0]: # turns off invinsibility as a result of being hit recently
            playerCollisionEffect()
            if round(current_time,1) == recently_hit[1] + 3:  # if its been 3 seconds since player collided with enemy
                recently_hit[0] = False
                player.setInvinsibility(False)
                resetColour()

        # MODES
        if gamemode == game_modes[0]:
            deadcount = 0
            for i in enemies:
                if i.status == "dead":
                    deadcount += 1
            if deadcount == len(enemies):
                for i in enemies:
                    if i.status == "dead":
                        i.revive()
                level += 1
                resetPlayer()
                pygame.time.wait(500)
                createEnemies()

        elif gamemode == game_modes[1]:
            pass
            # if all enemies arent killed within the allowed time period you lose
            #if round(current_time,1) %10.0 == 0: # TIME MODE
                #for i in enemies:
                    #i.move(random.randint(0, Setup.WIDTH-i.width), random.randint(0, Setup.HEIGHT-i.height))
        elif gamemode == game_modes[2]:
            pass
        # enemies keep getting stronger the more theyre killed (keep spawning endlessly)

main()
