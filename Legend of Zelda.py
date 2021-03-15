'''TO DO: death screen, pause button, display controls, organize code better (put more things in player class)'''
'''BUG FIXES NEEDED: link can spam sword when holding a direction and overall sword buffer is not good, link can take knockback and go offscreen (not really a bug)'''
'''THINGS TO DRAW: maybe title screen and pause menu stuff'''
import pygame
import random
import sys

WIDTH = 1800 #1800
HEIGHT = 1400 #1400
FPS = 60

#defining colors
GROUND_COLOR = (255, 222, 179)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
PURPLE = (255,0,255)

#link and animation constants
TILESIZE = 100
player_speed = 10
animation_count = 0
item_used = False
sword_out = False #is true during the sword animation and a bit after the animation for a cooldown and set to false after this time limit
changed_rooms = False #is false as soon as the game starts

#sprite lists
octorok_list = []
wall_list = []
background_list = []
item_list = []
locked_door_list = []

#initialize pygame and create window
pygame.mixer.pre_init(44100, -16, 1, 512) #makes sounds have no delay
pygame.init()
#pygame.mixer.init() #for sounds (do i need this?)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Legend of Zelda")
clock = pygame.time.Clock()

#loading link forward sprites
link_standing = pygame.transform.scale(pygame.image.load('Player_Sprites/link_standing_forward.png'), (TILESIZE, TILESIZE)).convert_alpha()
link_1 = pygame.transform.scale(pygame.image.load('Player_Sprites/link_forward_walking_A.png'), (TILESIZE, TILESIZE)).convert_alpha()
link_2 = pygame.transform.scale(pygame.image.load('Player_Sprites/link_forward_walking_B.png'), (TILESIZE, TILESIZE)).convert_alpha()
player_forward = [link_1, link_2]

#loading link backward sprites
link_3 = pygame.transform.scale(pygame.image.load('Player_Sprites/link_back_A.png'), (TILESIZE, TILESIZE)).convert_alpha()
link_4 = pygame.transform.scale(pygame.image.load('Player_Sprites/link_back_B.png'), (TILESIZE, TILESIZE)).convert_alpha()
player_backward = [link_3, link_4]

#loading link horizontal sprites
link_5 = pygame.transform.scale(pygame.image.load('Player_Sprites/link_right_A.png'), (TILESIZE, TILESIZE)).convert_alpha()
link_6 = pygame.transform.scale(pygame.image.load('Player_Sprites/link_right_B.png'), (TILESIZE, TILESIZE)).convert_alpha()
player_right = [link_5, link_6]
player_left = [pygame.transform.flip(link_5, True, False), pygame.transform.flip(link_6, True, False)]

#loading link using sword sprites
link_item_front = pygame.transform.scale(pygame.image.load('Player_Sprites/link_forward_item.png'), (TILESIZE, TILESIZE)).convert_alpha()
link_item_back = pygame.transform.scale(pygame.image.load('Player_Sprites/link_back_item.png'), (TILESIZE, TILESIZE)).convert_alpha()
link_item_right = pygame.transform.scale(pygame.image.load('Player_Sprites/link_right_item.png'), (TILESIZE, TILESIZE)).convert_alpha()
link_item_left = pygame.transform.flip(link_item_right, True, False).convert_alpha()

#loading sword sprites
sword_right = pygame.transform.scale(pygame.image.load('Player_Sprites/sword_horizontal.png'), (TILESIZE, TILESIZE)).convert_alpha()
sword_left = pygame.transform.flip(pygame.transform.scale(pygame.image.load('Player_Sprites/sword_horizontal.png'), (TILESIZE, TILESIZE)), True, False).convert_alpha()
sword_up = pygame.transform.scale(pygame.image.load('Player_Sprites/sword_vertical.png'), (TILESIZE, TILESIZE)).convert_alpha()
sword_down = pygame.transform.flip(pygame.transform.scale(pygame.image.load('Player_Sprites/sword_vertical.png'), (TILESIZE, TILESIZE)), False, True).convert_alpha()
sword_sprites = [sword_up, sword_down, sword_left, sword_right]

#loading red octorok sprites
octorok_ball = pygame.transform.scale(pygame.image.load('Octorok_Sprites/octorok_ball.png'), (int(TILESIZE/2), int(TILESIZE/2))).convert_alpha()
red_down_1 = pygame.transform.scale(pygame.image.load('Octorok_Sprites/red_down_A.png'), (TILESIZE, TILESIZE)).convert_alpha()
red_down_2 = pygame.transform.scale(pygame.image.load('Octorok_Sprites/red_down_B.png'), (TILESIZE, TILESIZE)).convert_alpha()
red_right_1 = pygame.transform.scale(pygame.image.load('Octorok_Sprites/red_right_A.png'), (TILESIZE, TILESIZE)).convert_alpha()
red_right_2 = pygame.transform.scale(pygame.image.load('Octorok_Sprites/red_right_B.png'), (TILESIZE, TILESIZE)).convert_alpha()
red_up_1 = pygame.transform.flip(pygame.transform.scale(pygame.image.load('Octorok_Sprites/red_down_A.png'), (TILESIZE, TILESIZE)), False, True).convert_alpha()
red_up_2 = pygame.transform.flip(pygame.transform.scale(pygame.image.load('Octorok_Sprites/red_down_B.png'), (TILESIZE, TILESIZE)), False, True).convert_alpha()
red_left_1 = pygame.transform.flip(pygame.transform.scale(pygame.image.load('Octorok_Sprites/red_right_A.png'), (TILESIZE, TILESIZE)), True, False).convert_alpha()
red_left_2 = pygame.transform.flip(pygame.transform.scale(pygame.image.load('Octorok_Sprites/red_right_B.png'), (TILESIZE, TILESIZE)), True, False).convert_alpha()
red_down = [red_down_1, red_down_2]
red_right = [red_right_1, red_right_2]
red_up = [red_up_1, red_up_2]
red_left = [red_left_1, red_left_2]

#loading blue octorok sprites
blue_down_1 = pygame.transform.scale(pygame.image.load('Octorok_Sprites/blue_down_A.png'), (TILESIZE, TILESIZE)).convert_alpha()
blue_down_2 = pygame.transform.scale(pygame.image.load('Octorok_Sprites/blue_down_B.png'), (TILESIZE, TILESIZE)).convert_alpha()
blue_right_1 = pygame.transform.scale(pygame.image.load('Octorok_Sprites/blue_right_A.png'), (TILESIZE, TILESIZE)).convert_alpha()
blue_right_2 = pygame.transform.scale(pygame.image.load('Octorok_Sprites/blue_right_B.png'), (TILESIZE, TILESIZE)).convert_alpha()
blue_up_1 = pygame.transform.flip(pygame.transform.scale(pygame.image.load('Octorok_Sprites/blue_down_A.png'), (TILESIZE, TILESIZE)), False, True).convert_alpha()
blue_up_2 = pygame.transform.flip(pygame.transform.scale(pygame.image.load('Octorok_Sprites/blue_down_B.png'), (TILESIZE, TILESIZE)), False, True).convert_alpha()
blue_left_1 = pygame.transform.flip(pygame.transform.scale(pygame.image.load('Octorok_Sprites/blue_right_A.png'), (TILESIZE, TILESIZE)), True, False).convert_alpha()
blue_left_2 = pygame.transform.flip(pygame.transform.scale(pygame.image.load('Octorok_Sprites/blue_right_B.png'), (TILESIZE, TILESIZE)), True, False).convert_alpha()
blue_down = [blue_down_1, blue_down_2]
blue_right = [blue_right_1, blue_right_2]
blue_up = [blue_up_1, blue_up_2]
blue_left = [blue_left_1, blue_left_2]

#loading tiles
transparent = pygame.transform.scale(pygame.image.load('Tile_Sprites/transparent.png'), (TILESIZE, TILESIZE)).convert_alpha()
snail_rock = pygame.transform.scale(pygame.image.load('Tile_Sprites/snail_rock.png'), (TILESIZE, TILESIZE)).convert_alpha()
tree = pygame.transform.scale(pygame.image.load('Tile_Sprites/tree.png'), (TILESIZE, TILESIZE)).convert_alpha()
gravestone = pygame.transform.scale(pygame.image.load('Tile_Sprites/gravestone.png'), (TILESIZE, TILESIZE)).convert_alpha()
brown_rock = pygame.transform.scale(pygame.image.load('Tile_Sprites/brown_rock.png'), (TILESIZE, TILESIZE)).convert()
green_rock = pygame.transform.scale(pygame.image.load('Tile_Sprites/green_rock.png'), (TILESIZE, TILESIZE)).convert()
black_square = pygame.transform.scale(pygame.image.load('Tile_Sprites/black_square.png'), (TILESIZE, TILESIZE)).convert()
brown_bridge = pygame.transform.scale(pygame.image.load('Tile_Sprites/brown_bridge.png'), (TILESIZE, TILESIZE)).convert()
green_bridge = pygame.transform.scale(pygame.image.load('Tile_Sprites/green_bridge.png'), (TILESIZE, TILESIZE)).convert()
water_middle = pygame.transform.scale(pygame.image.load('Tile_Sprites/water_middle.png'), (TILESIZE, TILESIZE)).convert_alpha()
water_top_right = pygame.transform.flip(pygame.transform.scale(pygame.image.load('Tile_Sprites/water_bottom_right.png'), (TILESIZE, TILESIZE)),False,True).convert_alpha()
water_bottom_right = pygame.transform.scale(pygame.image.load('Tile_Sprites/water_bottom_right.png'), (TILESIZE, TILESIZE)).convert_alpha()
water_middle_bottom = pygame.transform.scale(pygame.image.load('Tile_Sprites/water_middle_bottom.png'), (TILESIZE, TILESIZE)).convert_alpha()
water_middle_top = pygame.transform.flip(pygame.transform.scale(pygame.image.load('Tile_Sprites/water_middle_bottom.png'), (TILESIZE, TILESIZE)),False,True).convert_alpha()
water_bottom_left = pygame.transform.flip(pygame.transform.scale(pygame.image.load('Tile_Sprites/water_bottom_right.png'), (TILESIZE, TILESIZE)),True, False).convert_alpha()
water_top_left = pygame.transform.flip(pygame.transform.scale(pygame.image.load('Tile_Sprites/water_bottom_right.png'), (TILESIZE, TILESIZE)),True, True).convert_alpha()
water_middle_right = pygame.transform.scale(pygame.image.load('Tile_Sprites/water_middle_right.png'), (TILESIZE, TILESIZE)).convert_alpha()
water_middle_left = pygame.transform.flip(pygame.transform.scale(pygame.image.load('Tile_Sprites/water_middle_right.png'), (TILESIZE, TILESIZE)),True, False).convert_alpha()
key_image = pygame.transform.scale(pygame.image.load('Tile_Sprites/key.png'), (TILESIZE,TILESIZE)).convert_alpha()
brown_bridge_vertical = pygame.transform.rotate(brown_bridge, 90)
locked_door = pygame.transform.scale(pygame.image.load('Tile_Sprites/locked_door.png'), (TILESIZE*2,TILESIZE*2)).convert_alpha()
smoke = pygame.transform.scale(pygame.image.load('Tile_Sprites/smoke.png'), (TILESIZE, TILESIZE)).convert_alpha()

#menu/misc images
full_heart = pygame.transform.scale(pygame.image.load('Menu_Images/full_heart.png'), (int(TILESIZE*.8), int(TILESIZE*.8))).convert_alpha()
half_heart = pygame.transform.scale(pygame.image.load('Menu_Images/half_heart.png'), (int(TILESIZE*.8), int(TILESIZE*.8))).convert_alpha()
no_heart = pygame.transform.scale(pygame.image.load('Menu_Images/no_heart.png'), (int(TILESIZE*.8), int(TILESIZE*.8))).convert_alpha()
title_screen_image = pygame.transform.scale(pygame.image.load('Menu_Images/title_screen_image.jpg'), (1800,1400)).convert()
triforce_image = pygame.transform.scale(pygame.image.load('Menu_Images/triforce_image.png'), (300,300)).convert_alpha()

#additional things that need to be placed in classes for better organization
player_invincible = [gravestone, transparent] ###############temporary invincible animation
music_count = 0 #kinda jank way of playing the music once
disp_winning_text = False

class Player(pygame.sprite.Sprite):
    def __init__(self, layer):
        pygame.sprite.Sprite.__init__(self)
        self.image = link_standing
        self.rect = self.image.get_rect() #figures out rectangle hitbox based on image
        self._layer = layer #the sprite's layer is defined here
        self.rect.center = (900, 500)
        self.x_change = 0
        self.y_change = 0
        self.down = True #link faces down by default
        self.up = False
        self.left = False
        self.right = False
        self.health = 6 #start with 3 hearts
        self.invincible = False #only true for a period of time after getting hit by something
        self.collision_with_link_time = 0 #is used for timing the invincibility frames
        self.invincible_animation_count = 0 #count used for animation for being invincible
        self.shield_up = True
        self.key_get = False #starts off as false
        self.unlocked_door = False
        self.alive = True #link is alive by default
        self.sword_get = False #starts out false until you get the sword
        self.stunned = False #prevents player from moving when true
    
    def update(self):
        global animation_count, item_used, original_frame
        #MOVEMENT
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN] and not keys[pygame.K_UP] and not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT] and not item_used and not self.stunned:
            self.rect.y += player_speed
            self.rect.x += 0
            self.down = True
            self.up = False
            self.left = False
            self.right = False
        
            animation_count += 1
            if animation_count + 1 >= 20:
                animation_count = 0
            self.image = player_forward[animation_count//10] #this number times the number of sprites in the list is the number two lines above
        
        if keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT] and not item_used and not self.stunned:
            self.rect.y -= player_speed
            self.x_change += 0
            self.down = False
            self.up = True
            self.left = False
            self.right = False
        
            animation_count += 1
            if animation_count + 1 >= 20:
                animation_count = 0
            self.image = player_backward[animation_count//10]
        
        if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT] and not keys[pygame.K_DOWN] and not keys[pygame.K_UP] and not item_used and not self.stunned:
            self.rect.x += player_speed
            self.rect.y += 0
            self.down = False
            self.up = False
            self.left = False
            self.right = True
        
            animation_count += 1
            if animation_count + 1 >= 20:
                animation_count = 0
            self.image = player_right[animation_count//10]
        
        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not item_used and not self.stunned:
            self.rect.x -= player_speed
            self.rect.y += 0
            self.down = False
            self.up = False
            self.left = True
            self.right = False
        
            animation_count += 1
            if animation_count + 1 >= 20:
                animation_count = 0
            self.image = player_left[animation_count//10]
        
        
        #ITEM USED ANIMATION: if item used is true, then the action of attacking plays out and link cannot move. if he does, the animation is interrupted
        if item_used:
            self.shield_up = False
            if animation_count > 5: #makes link still swing his sword if a direction is held and the space bar is pressed
                if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]: #animation ends if link is moved by the player
                    item_used = False
                    self.shield_up = True
                
            if self.image != link_item_front and self.image != link_item_back and self.image != link_item_right and self.image != link_item_left: #happens if the frame is not an item use frame
                original_frame = self.image #saves the image of what link was before attacking if he is not currently animated
                
            animation_count += 1
            if animation_count + 1 > 9: #stops animation after a certain amount of time
                animation_count = 0
                item_used = False
                self.shield_up = True
                self.image = original_frame #link image is set to whatever it was before the sword has swung
                
            #if the animation is still going on, then the animation will continue here
            elif original_frame == player_forward[0] or original_frame == player_forward[1] or original_frame == link_standing: #happens if link is facing forward
                self.image = link_item_front
            elif original_frame == player_backward[0] or original_frame == player_backward[1]: #if link is facing backward
                self.image = link_item_back
            elif original_frame == player_right[0] or original_frame == player_right[1]:
                self.image = link_item_right
            elif original_frame == player_left[0] or original_frame == player_left[1]:
                self.image = link_item_left
            
        #COLLISIONS WITH WALLS FOR PLAYER
        for wall in wall_list:
            if pygame.sprite.collide_rect(self, wall):
                if self.left:
                    self.rect.x = wall.rect.x + TILESIZE
                elif self.right:
                    self.rect.x = wall.rect.x - TILESIZE
                elif self.down:
                    self.rect.y = wall.rect.y - TILESIZE
                elif self.up:
                    self.rect.y = wall.rect.y + TILESIZE
        
        #PLAYER GETS ITEM
        for item in item_list:
            if pygame.sprite.collide_mask(self, item):
                item.rect.x = -200
                pygame.mixer.Channel(4).play(pygame.mixer.Sound('Sounds/get_item.wav'))
                if item.image == key_image and not self.key_get:
                    self.key_get = True
                if item.image == sword_up and not self.sword_get:
                    self.sword_get = True
        
        #PLAYER COLLISION WITH LOCKED DOOR
        for door in locked_door_list:
            if pygame.sprite.collide_rect(self, door) and not self.key_get: #only checks for going up with this kind of door
                self.rect.y = door.rect.y + TILESIZE*2
            if pygame.sprite.collide_rect(self, door) and self.key_get:
                door.rect.x = -300
                player.unlocked_door = True
                pygame.mixer.Channel(4).play(pygame.mixer.Sound('Sounds/open_door.wav'))
        
        #VISUAL FOR WHEN LINK IS INVINCIBLE###############################need to make this image better and maybe flicker
        if not self.invincible:
            self.invincible_animation_count = 0
        if self.invincible:
            self.invincible_animation_count += 1
            if self.invincible_animation_count + 1 >= 20:
                self.invincible_animation_count = 0
            self.image = player_invincible[self.invincible_animation_count//10]
        if len(octorok_list) == 0: #prevents bug where link stays invincible after he gets hit by an octorok ball and all enemies are dead
            self.invincible = False
        
        #WHEN PLAYER DIES (locks controls)
        if self.health <= 0:
            if not self.stunned:
                pygame.mixer.Channel(4).play(pygame.mixer.Sound('Sounds/game_over.wav')) #sound effect when player dies (plays once)
            self.stunned = True
            self.invincible = True
            self.image = gravestone
            
        ##############################################temporary below for area that changes the current screen (MAP MAKING)
        if self.rect.x >= WIDTH: #right off screen
            if self.rect.y > TILESIZE*9:
                change_room('right', 'room_2')
            elif self.rect.y < TILESIZE*5:
                change_room('right', 'room_3')
            else:
                change_room('right', 'room_4')
        if self.rect.x <= -TILESIZE: #left off screen
            if self.rect.y > TILESIZE*9:
                change_room('left', 'room_1')
            elif self.rect.y < TILESIZE*5:
                change_room('left', 'room_2')
            else:
                change_room('left', 'room_5')
            
        if self.rect.y >= HEIGHT: #down off screen
            if self.rect.x < TILESIZE*7:
                change_room('down', 'room_3')
            elif self.rect.x > TILESIZE*10:
                change_room('down', 'room_2')
            else:
                change_room('down', 'room_5')
        if self.rect.y <= TILESIZE: #up off screen
            if self.rect.x < TILESIZE*7:
                change_room('up', 'room_4')
            elif self.rect.x > TILESIZE*10:
                change_room('up', 'room_5')
            else:
                change_room('up', 'room_6')
    
    def player_reset_inventory(self): #for restarting the game
        self.health = 6
        self.key_get = False #starts off as false
        self.unlocked_door = False
        self.alive = True #link is alive by default
        self.sword_get = False
        self.stunned = False

class Sword(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sword_sprites[1]
        self.rect = self.image.get_rect() #figures out rectangle hitbox based on image
        self.rect.x = -1000 #sword is stored off screen a frame before it is used (prevents visual bug)
        self.rect.y = -1000
        self.collision_time = 0
        self.time_sword_out = 0
        self.sword_buffer = 70 #sets the cooldown between sword slashes(has to be a low number because it only gets updated when the sword is spawned in)
    
    def update(self):
        global item_used, octorok_list, animation_count, sword_out
        #spawns sword in the player's hand
        if item_used:
            if not sword_out: #starts timer if sword is not out
                self.time_sword_out = pygame.time.get_ticks()
            sword_out = True
            if player.right:
                self.image = sword_sprites[3]
                self.rect.x = player.rect.x + TILESIZE/1.4
                self.rect.y = player.rect.y + TILESIZE/10
            elif player.left:
                self.image = sword_sprites[2]
                self.rect.x = player.rect.x - TILESIZE/1.4
                self.rect.y = player.rect.y + TILESIZE/10
            elif player.up:
                self.image = sword_sprites[0]
                self.rect.x = player.rect.x - TILESIZE/10
                self.rect.y = player.rect.y - TILESIZE/1.4
            elif player.down:
                self.image = sword_sprites[1]
                self.rect.x = player.rect.x + TILESIZE/10
                self.rect.y = player.rect.y + TILESIZE/1.4
        else:
            all_sprites.remove(self) #gets rid of sword if the player is not in an item animation state
            if pygame.time.get_ticks() - self.time_sword_out > self.sword_buffer: #sword is no longer 'out' if the time passed passes the buffer time
                sword_out = False
        
        #CHECKS COLLISION WITH ITEMS IN OCTOROK LIST (each octorok has a cooldown called octorok.invincible)
        for octorok in octorok_list: #checks for collision for any item in the octorok list, octorok gets knocked back based on the direction link is facing
            if pygame.sprite.collide_mask(octorok, self) and not octorok.invincible: #octorok health goes down if it is attacked and not invincible
                octorok.health -= 1
                if octorok.health > 0: #plays hit sound only if the enemy is not dead
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('Sounds/sword_hit.wav'))
                
                #for octorok knockback, octorok only takes knockback when it is alive
                original_octorok_x = octorok.rect.x
                original_octorok_y = octorok.rect.y
                if player.up and octorok.health > 0:
                    octorok.rect.y -= TILESIZE*1.5
                if player.down and octorok.health > 0:
                    octorok.rect.y += TILESIZE*1.5
                if player.right and octorok.health > 0:
                    octorok.rect.x += TILESIZE*1.5
                if player.left and octorok.health > 0:
                    octorok.rect.x -= TILESIZE*1.5
                for wall in wall_list: #prevents octorok from going off screen or into walls during knockback
                    if pygame.sprite.collide_rect(octorok, wall) or octorok.rect.x > WIDTH or octorok.rect.x < 0 or octorok.rect.y > HEIGHT or octorok.rect.y < TILESIZE*2:
                        octorok.rect.x = original_octorok_x
                        octorok.rect.y = original_octorok_y
                    
                octorok.invincible = True
                self.collision_time = pygame.time.get_ticks()
            if pygame.time.get_ticks() - self.collision_time > 700: #after 700 ms, the octorok is no longer invincible
                octorok.invincible = False
            if octorok.health < 1: #the octorok dies if it's health goes below 1
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('Sounds/enemy_dies.wav'))
                
                #death animation (kinda jank but it's the last thing i did with this program, the '6' only updates when colliding with the sword so jank but it works)
                if octorok.count < 6:
                    octorok.count+=1
                    octorok.image = smoke
                else:
                    all_sprites.remove(octorok)
                    octorok_list.remove(octorok)#############octorok death animation goes after this
        
        
class Octorok(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, color, health): #a red octorok is placed in a location specified with an x and y value
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILESIZE,TILESIZE))
        self.image.fill(GROUND_COLOR) #image is the color of the background by default
        self.rect = self.image.get_rect() #figures out rectangle hitbox based on image
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.color = color
        self.health = health
        self.invincible = False #not invincible by default
        self.direction = ['up', 'down', 'left', 'right', 'stop', 'stop', 'stop'] #octorok can either stop or move in any of four directions
        self.octorok_direction = self.direction[random.randrange(0,4)] #default direction is random when spawned in (not stopped)
        self.octorok_move_count = 0 #for moving
        self.octorok_animation_count = 0 #for moving animation
        self.down = True #enemy faces down by default
        self.up = False
        self.left = False
        self.right = False
        self.able_to_shoot = True #for cooldown once a projectile is shot
        self.able_to_shoot_timer = 0
        self.collision_with_link_start = 0
        self.count = 0
    
    def update(self):
        global changed_rooms, octorok_list, locked_door_list
        #MOVEMENT
        self.octorok_move_count += 1
        if self.octorok_move_count + 1 > 30: #stops animation after a certain amount of time
            self.octorok_move_count = 0
            self.octorok_direction = self.direction[random.randrange(0,6)] #picks a new direction to travel after the specified time
            
        if self.octorok_direction == 'up' and self.rect.y > TILESIZE*2:
            self.rect.y -= self.speed
            self.down = False
            self.up = True
            self.left = False
            self.right = False
            self.octorok_animation_count += 1
            if self.octorok_animation_count + 1 >= 20:
                self.octorok_animation_count = 0
            if self.color == 'blue': #image changes color based on what color was specified(red by default)
                self.image = blue_up[self.octorok_animation_count//10]
            else:
                self.image = red_up[self.octorok_animation_count//10]
            
        if self.octorok_direction == 'down' and self.rect.y < HEIGHT-TILESIZE:
            self.rect.y += self.speed
            self.down = True
            self.up = False
            self.left = False
            self.right = False
            self.octorok_animation_count += 1
            if self.octorok_animation_count + 1 >= 20:
                self.octorok_animation_count = 0
            if self.color == 'blue':
                self.image = blue_down[self.octorok_animation_count//10]
            else:
                self.image = red_down[self.octorok_animation_count//10]
            
        if self.octorok_direction == 'left' and self.rect.x > 0:
            self.rect.x -= self.speed
            self.down = False
            self.up = False
            self.left = True
            self.right = False
            self.octorok_animation_count += 1
            if self.octorok_animation_count + 1 >= 20:
                self.octorok_animation_count = 0
            if self.color == 'blue':
                self.image = blue_left[self.octorok_animation_count//10]
            else:
                self.image = red_left[self.octorok_animation_count//10]
            
        if self.octorok_direction == 'right' and self.rect.x < WIDTH-TILESIZE:
            self.rect.x += self.speed
            self.down = False
            self.up = False
            self.left = False
            self.right = True
            self.octorok_animation_count += 1
            if self.octorok_animation_count + 1 >= 20:
                self.octorok_animation_count = 0
            if self.color == 'blue':
                self.image = blue_right[self.octorok_animation_count//10]
            else:
                self.image = red_right[self.octorok_animation_count//10]
        
        #CHECK COLLISION WITH WALLS
        for wall in wall_list:
            if pygame.sprite.collide_rect(self, wall):
                if self.left:
                    self.rect.x = wall.rect.x + TILESIZE
                    self.octorok_direction = self.direction[random.randrange(3,6)]
                elif self.right:
                    self.rect.x = wall.rect.x - TILESIZE
                    self.octorok_direction = self.direction[random.randrange(0,2)]
                elif self.down:
                    self.rect.y = wall.rect.y - TILESIZE
                    self.octorok_direction = self.direction[random.randrange(2,6)]
                elif self.up:
                    self.rect.y = wall.rect.y + TILESIZE
                    self.octorok_direction = self.direction[random.randrange(1,6)]
        
        #CHECK COLLISION WITH LOCKED DOOR
        for octorok in octorok_list:
            for locked_door in locked_door_list:
                if pygame.sprite.collide_rect(octorok, locked_door): #only checks for going up with this kind of door
                    octorok.rect.y = locked_door.rect.y + TILESIZE*2        
        
        #CHECKS IF THE OCTOROK SHOULD SHOOT AN OCTOROK BALL  (octorok has a chance to shoot a ball if it is stopped and facing a direction and link is in that direction and the cooldown is done)
        if self.right and self.octorok_direction == 'stop' and player.rect.x > self.rect.x and self.able_to_shoot and random.random() < 0.1:
            changed_rooms = False #the flag preventing them to shoot is gone as soon as they are about to shoot
            all_sprites.add(Octorok_Ball(self.rect.x + TILESIZE, self.rect.y + TILESIZE/4, 'right', 12))
            self.able_to_shoot = False
        if self.left and self.octorok_direction == 'stop' and player.rect.x < self.rect.x and self.able_to_shoot and random.random() < 0.1:
            changed_rooms = False
            all_sprites.add(Octorok_Ball(self.rect.x - TILESIZE/2, self.rect.y + TILESIZE/4, 'left', 12))
            self.able_to_shoot = False
        if self.up and self.octorok_direction == 'stop' and player.rect.y < self.rect.y and self.able_to_shoot and random.random() < 0.1:
            changed_rooms = False
            all_sprites.add(Octorok_Ball(self.rect.x + TILESIZE/4, self.rect.y - TILESIZE/2, 'up', 12))
            self.able_to_shoot = False
        if self.down and self.octorok_direction == 'stop' and player.rect.y > self.rect.y and self.able_to_shoot and random.random() < 0.1:
            changed_rooms = False
            all_sprites.add(Octorok_Ball(self.rect.x + TILESIZE/4, self.rect.y + TILESIZE/0.9, 'down', 12))
            self.able_to_shoot = False
            
        if not self.able_to_shoot: #if the octorok has just shot, it will be able to shoot 2 seconds later
            self.able_to_shoot_timer += 1
            if self.able_to_shoot_timer > 120:
                self.able_to_shoot_timer = 0
                self.able_to_shoot = True
        
        #COLLISION WITH LINK
        if pygame.sprite.collide_mask(self, player) and not player.invincible:
            original_x = player.rect.x #saves these in case the player collides with a wall. if so, the player is moved back to their position to prevent clipping into walls
            original_y = player.rect.y
            player.health -= 1
            pygame.mixer.Channel(2).play(pygame.mixer.Sound('Sounds/link_hurt.wav'))
            player.collision_with_link_time = pygame.time.get_ticks()
            player.invincible = True
            
            #knockback
            if player.rect.x < self.rect.x and player.rect.y < self.rect.y:
                player.rect.x -= TILESIZE
                player.rect.y -= TILESIZE
            if player.rect.x < self.rect.x and player.rect.y > self.rect.y:
                player.rect.x -= TILESIZE
                player.rect.y += TILESIZE
            if player.rect.x > self.rect.x and player.rect.y < self.rect.y:
                player.rect.x += TILESIZE
                player.rect.y -= TILESIZE
            if player.rect.x > self.rect.x and player.rect.y > self.rect.y:
                player.rect.x += TILESIZE
                player.rect.y += TILESIZE
                
            for wall in wall_list: #prevents link from going in walls during knockback
                if pygame.sprite.collide_rect(player, wall):
                    player.rect.x = original_x
                    player.rect.y = original_y
                    
        if pygame.time.get_ticks() - player.collision_with_link_time > 800: #player is invincible for a time after getting hit
            player.invincible = False
            

class Octorok_Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed): #when called, an octorok ball spawns on an octorok
        pygame.sprite.Sprite.__init__(self)
        self.image = octorok_ball
        self.rect = self.image.get_rect() #figures out rectangle hitbox based on image
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
        self.speed = speed
    
    def update(self):
        global player
        if self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction ==  'down':
            self.rect.y += self.speed
        elif self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction ==  'right':
            self.rect.x += self.speed
        
        #Balls despawn when they hit the edge of the screen
        if self.rect.x > WIDTH or self.rect.x < 0 or self.rect.y < 0 or self.rect.y > HEIGHT:
            all_sprites.remove(self)
        if changed_rooms: #if link changes the room, all the projectiles will disappear
            all_sprites.remove(self)
        
        #COLLISION WITH LINK AND KNOCKBACK AND SHIELDING
        if pygame.sprite.collide_mask(self, player) and not player.invincible:
            player_hit = True #for shielding
            #shielding
            if player.shield_up:
                if player.up and self.direction == 'down' or player.down and self.direction == 'up' or player.left and self.direction == 'right' or player.right and self.direction == 'left':
                    player.health += 1 #counters the minus health below
                    player_hit = False
                    pygame.mixer.Channel(3).play(pygame.mixer.Sound('Sounds/shield.wav'))
            
            original_x = player.rect.x #saves these in case the player collides with a wall. if so, the player is moved back to their position to prevent clipping into walls
            original_y = player.rect.y
            player.collision_with_link_time = pygame.time.get_ticks()
            if self.direction == 'up' and player_hit:
                player.rect.y -= TILESIZE
            if self.direction == 'down' and player_hit:
                player.rect.y += TILESIZE
            if self.direction == 'left' and player_hit:
                player.rect.x -= TILESIZE
            if self.direction == 'right' and player_hit:
                player.rect.x += TILESIZE
            
            
            player.health -= 1
            
            if player_hit:
                pygame.mixer.Channel(2).play(pygame.mixer.Sound('Sounds/link_hurt.wav'))
                player.invincible = True
            
            all_sprites.remove(self)
            for wall in wall_list:
                if pygame.sprite.collide_rect(player, wall):
                    player.rect.x = original_x
                    player.rect.y = original_y
            
        if pygame.time.get_ticks() - player.collision_with_link_time > 800:
            player.invincible = False
                    
            


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, image): #takes in the xy location of where the wall needs to be and the image of the wall
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect() #figures out rectangle hitbox based on image
        self.rect.x = x
        self.rect.y = y

class BackgroundTile(pygame.sprite.Sprite): #blits to the screen
    def __init__(self, x, y, image): #takes in the xy location of where the wall needs to be and the image of the wall
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Item(pygame.sprite.Sprite): #blits to the screen
    def __init__(self, x, y, image): #takes in the xy location of where the wall needs to be and the image of the wall
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class LockedDoor(pygame.sprite.Sprite):
    def __init__(self, x, y, image): #takes in the xy location of where the wall needs to be and the image of the wall
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect() #figures out rectangle hitbox based on image
        self.rect.x = x
        self.rect.y = y

#adds player to the sprite group and applies layering so that link is above other sprites
def add_player_sprite():
    global player, all_sprites
    all_sprites = pygame.sprite.Group()
    all_sprites = pygame.sprite.LayeredUpdates() #makes the all_sprites sprite group have layers
    player = Player(1) #sets player layer to 1 (in front of sword layer)
    all_sprites.add(player)


def draw_menu():
    display_font = pygame.font.SysFont("ebrima", 60, bold=True)
    screen.blit(display_font.render('— L I F E — ', 1, RED), (80, 10))
    if player.key_get:
        screen.blit(key_image,(1650,50))
    if player.sword_get:
        screen.blit(sword_up, (1550,50))
    
    #Health (for 3 hearts)
    if player.health >= 2: #drawing full hearts
        screen.blit(full_heart, (100,85))
        if player.health >= 4:
            screen.blit(full_heart, (200,85))
            if player.health >= 6:
                screen.blit(full_heart, (300,85))
    if player.health <= 4: #drawing no hearts
        screen.blit(no_heart, (300,85))
        if player.health <= 2:
            screen.blit(no_heart, (200,85))
            if player.health <= 0:
                screen.blit(no_heart, (100,85))
    if player.health == 5: #drawing half hearts
        screen.blit(half_heart, (300,85))
    if player.health == 3:
        screen.blit(half_heart, (200,85))
    if player.health == 1:
        screen.blit(half_heart, (100,85))

def draw_winning_text():
    global disp_winning_text
    if disp_winning_text:
        display_font = pygame.font.SysFont("javanesetext", 60, bold=True)
        screen.blit(display_font.render('CONGRATULATIONS! YOU HAVE FOUND', 1, BLACK), (250, 650))
        screen.blit(display_font.render('THE TRIFORCE AND SAVED HYRULE!', 1, BLACK), (300, 730))
        
def play_overworld_music():
    #play music for pygame:
    song = pygame.mixer.music.load('Sounds/zelda_overworld.mp3')
    pygame.mixer.music.play(-1)

def play_intro_music():
    #play music for pygame:
    song = pygame.mixer.music.load('Sounds/title_theme.mp3')
    pygame.mixer.music.play(-1)
    

#MAP MAKING FROM THIS POINT DOWN UNTIL YOU GET TO MAIN
#resets the room, or if parameters are not specified, restarts game
def change_room(direction=0, room=0):
    global octorok_list, wall_list, changed_rooms, background_list, item_list, locked_door_list
    changed_rooms = True #the room is changed, so this flag is set until it is false when an enemy shoots
    #resets all sprites and lists
    for wall in wall_list:
        all_sprites.remove(wall)
    for octorok in octorok_list:
        all_sprites.remove(octorok)
    for background in background_list:
        all_sprites.remove(background)
    for item in item_list:
        all_sprites.remove(item)
    for door in locked_door_list:
        all_sprites.remove(door)
    octorok_list = []
    wall_list = []
    background_list = []
    item_list = []
    locked_door_list = []
    
    if direction == 'right':
        player.rect.x = 0
        if room == 'room_2':
            draw_room_2()
        if room == 'room_3':
            draw_room_3()
        if room == 'room_4':
            draw_room_4()
    elif direction == 'left':
        player.rect.x = WIDTH-TILESIZE
        if room == 'room_1':
            draw_room_1()
        if room == 'room_2':
            draw_room_2()
        if room == 'room_5':
            draw_room_5()
    elif direction == 'up':
        player.rect.y = HEIGHT-TILESIZE
        if room == 'room_4':
            draw_room_4()
        if room == 'room_5':
            draw_room_5()
        if room == 'room_6':
            draw_room_6()
    elif direction == 'down':
        player.rect.y = 2*TILESIZE
        if room == 'room_3':
            draw_room_3()
        if room == 'room_2':
            draw_room_2()
        if room == 'room_5':
            draw_room_5()
    else: #for if the player is reset into a room (clears inventory and reset position)
        player.rect.x = 750
        player.rect.y = 550
        player.image = link_standing
        player.player_reset_inventory()
        

#this function draws the room and adds all the sprites to the all_sprites sprite group
def draw_room_1():
    global wall_list, octorok_list, background_list, item_list
    
    if not player.sword_get: #sword only appears if the player does not already have it
        item_list.append(Item(150,850,sword_up))
        
    for i in range(0,int(WIDTH/TILESIZE)): #main horizontal
        wall_list.append(Wall(i*TILESIZE,200,green_rock))
        wall_list.append(Wall(i*TILESIZE,300,green_rock))
        wall_list.append(Wall(i*TILESIZE,400,green_rock))
        wall_list.append(Wall(i*TILESIZE,HEIGHT-TILESIZE,water_middle))
    for i in range(6,int(WIDTH/TILESIZE)): #shoreline
        wall_list.append(Wall(i*TILESIZE,HEIGHT-TILESIZE*2,water_middle_top))
    for i in range(0,6): #left mountain
        wall_list.append(Wall(i*TILESIZE,500,green_rock))
        wall_list.append(Wall(i*TILESIZE,600,green_rock))
    for i in range(0,5): #left water
        wall_list.append(Wall(i*TILESIZE,700,water_middle))
        wall_list.append(Wall(i*TILESIZE,1000,water_middle))
        wall_list.append(Wall(i*TILESIZE,1100,water_middle))
        wall_list.append(Wall(i*TILESIZE,1200,water_middle))
    #island shenanigans
    wall_list.append(Wall(0,800,water_middle))
    wall_list.append(Wall(0,900,water_middle))
    wall_list.append(Wall(500,700,water_middle_right))
    wall_list.append(Wall(500,1000,water_middle_right))
    wall_list.append(Wall(500,1100,water_middle_right))
    wall_list.append(Wall(500,1200,water_middle))
    
    #right mts and snail rocks
    for i in range(5,10):
        wall_list.append(Wall(WIDTH-TILESIZE,i*100,green_rock))
        wall_list.append(Wall(WIDTH-TILESIZE*2,i*100,green_rock))
    for i in range(10,14):
        wall_list.append(Wall(i*100,700,snail_rock))
    wall_list.append(Wall(800,900,snail_rock))
    wall_list.append(Wall(900,900,snail_rock))
    
    
    wall_list.append(Wall(800, 400,black_square))
    
    #bridge
    for i in range(1,4):
        background_list.append(BackgroundTile(i*TILESIZE+200,800,brown_bridge))
    for i in range(1,4):
        background_list.append(BackgroundTile(i*TILESIZE+200,900,brown_bridge))
    
    #adding list elements to all_sprites
    for background in background_list:
        all_sprites.add(background)
    for wall in wall_list:
        all_sprites.add(wall)
    for item in item_list:
        all_sprites.add(item)

def draw_room_2():
    global wall_list, octorok_list, item_list        
    
    octorok_list.append(Octorok(1400, 800, 4, 'red', 1))
    octorok_list.append(Octorok(1100, 700, 4, 'red', 1))
    
    for i in range(0,int(WIDTH/TILESIZE)):
        wall_list.append(Wall(i*TILESIZE-700,1300,water_middle))
        wall_list.append(Wall(i*TILESIZE-600,1200,water_middle_top))
        
        wall_list.append(Wall(i*TILESIZE+700,1300,brown_rock))
        wall_list.append(Wall(i*TILESIZE+800,1200,brown_rock))
        wall_list.append(Wall(i*TILESIZE+1200,1100,brown_rock))
        wall_list.append(Wall(i*TILESIZE+1300,1000,brown_rock))
        wall_list.append(Wall(i*TILESIZE+1300,900,brown_rock))
        
        wall_list.append(Wall(i*TILESIZE-500,200,green_rock))
        wall_list.append(Wall(i*TILESIZE+1500,200,green_rock))
        
    for i in range(0,int(HEIGHT/TILESIZE)):
        wall_list.append(Wall(0,i*TILESIZE-400,green_rock))
        wall_list.append(Wall(100,i*TILESIZE-400,green_rock))
    
    for i in range(5,int(HEIGHT/TILESIZE)-5):
        wall_list.append(Wall(WIDTH-TILESIZE,i*TILESIZE,tree))
    for i in range(6,int(HEIGHT/TILESIZE)-5):
        wall_list.append(Wall(WIDTH-TILESIZE*2,i*TILESIZE,tree))
    for i in range(6,11):
        wall_list.append(Wall(i*TILESIZE,500,snail_rock))
    wall_list.append(Wall(400,800,snail_rock))
    wall_list.append(Wall(500,800,snail_rock))
    
    for wall in wall_list:
        all_sprites.add(wall)
    for enemy in octorok_list:
        all_sprites.add(enemy)

def draw_room_3():
    global wall_list, octorok_list
    
    if not player.key_get: #key only appears if the player does not already have it
        item_list.append(Item(450,1150,key_image))
    
    octorok_list.append(Octorok(800, 700, 4, 'red', 1))
    octorok_list.append(Octorok(700, 1200, 4, 'blue', 2))
    octorok_list.append(Octorok(1400, 800, 4, 'red', 1))
    
    for i in range(0,int(WIDTH/TILESIZE)): #horizontal
        wall_list.append(Wall(i*TILESIZE+300,1300,water_middle))
        wall_list.append(Wall(i*TILESIZE+1400,1200,water_middle))
        wall_list.append(Wall(i*TILESIZE+1400,1100,water_middle))
        wall_list.append(Wall(i*TILESIZE+1400,1000,water_middle))
        wall_list.append(Wall(i*TILESIZE+1400,900,water_middle_top))
        wall_list.append(Wall(i*TILESIZE-1400,200,green_rock))
        wall_list.append(Wall(i*TILESIZE+700,200,green_rock))
    
    for i in range(0,int(HEIGHT/TILESIZE)): #vertical
        wall_list.append(Wall(0,i*TILESIZE+800,brown_rock))
        wall_list.append(Wall(100,i*TILESIZE+800,brown_rock))
    
    for i in range(5,8): #vertical 3
        wall_list.append(Wall(0,i*TILESIZE,tree))
        wall_list.append(Wall(300,i*TILESIZE+500,water_middle))
    for i in range(3,10): #vertical 8
        wall_list.append(Wall(1700,i*TILESIZE,water_middle))
        wall_list.append(Wall(1600,i*TILESIZE,water_middle))
        wall_list.append(Wall(1500,i*TILESIZE,water_middle_left))
    for i in range(1,3): #horizontal 2
        wall_list.append(Wall(i*TILESIZE+500,500,snail_rock))
        wall_list.append(Wall(i*TILESIZE+900,600,snail_rock))
    for i in range(2,12): #horizontal 10
        wall_list.append(Wall(i*TILESIZE,900,water_middle_top))
        wall_list.append(Wall(i*TILESIZE,1000,water_middle))
    
    wall_list.append(Wall(200,1200,brown_rock))
    wall_list.append(Wall(200,1300,brown_rock))
    wall_list.append(Wall(1500,900,water_middle))
    wall_list.append(Wall(200,1100,water_middle))
    
    #bridge
    for i in range(1,3):
        background_list.append(BackgroundTile(i*TILESIZE+1100,900,brown_bridge_vertical))
        background_list.append(BackgroundTile(i*TILESIZE+1100,1000,brown_bridge_vertical))
    for i in range(1,7):
        background_list.append(BackgroundTile(i*TILESIZE+500,1100,brown_bridge))
        background_list.append(BackgroundTile(i*TILESIZE+500,1200,brown_bridge))
    
    for wall in wall_list:
        all_sprites.add(wall)
    for background in background_list:
        all_sprites.add(background)
    for item in item_list:
        all_sprites.add(item)
    for enemy in octorok_list:
        all_sprites.add(enemy)

def draw_room_4():
    global wall_list, octorok_list
    
    octorok_list.append(Octorok(1100, 500, 5, 'blue', 2))
    octorok_list.append(Octorok(700, 800, 4, 'red', 1))
    octorok_list.append(Octorok(1200, 1100, 5, 'red', 1))
    
    for i in range(0,int(WIDTH/TILESIZE)): #horizontal
        wall_list.append(Wall(i*TILESIZE,200,green_rock))
        wall_list.append(Wall(i*TILESIZE,300,green_rock))
        wall_list.append(Wall(i*TILESIZE-1400,1300,green_rock))
        wall_list.append(Wall(i*TILESIZE+700,1300,green_rock))
    
    for i in range(0,int(HEIGHT/TILESIZE)): #vertical
        wall_list.append(Wall(1700,i*TILESIZE+300,green_rock))
        wall_list.append(Wall(1600,i*TILESIZE+300,green_rock))
        wall_list.append(Wall(0,i*TILESIZE+900,green_rock))
        wall_list.append(Wall(0,i*TILESIZE-800,green_rock))
    
    for i in range(4,9): #horizontal 5
        wall_list.append(Wall(i*TILESIZE,600,snail_rock))
        wall_list.append(Wall(i*TILESIZE+500,1000,snail_rock))
    
    for wall in wall_list:
        all_sprites.add(wall)
    for enemy in octorok_list:
        all_sprites.add(enemy)

def draw_room_5():
    global wall_list, octorok_list, locked_door_list, disp_winning_text
    disp_winning_text = False
    
    octorok_list.append(Octorok(800, 700, 3, 'blue', 2))
    octorok_list.append(Octorok(700, 700, 3, 'blue', 2))
    octorok_list.append(Octorok(900, 700, 3, 'blue', 2))
    octorok_list.append(Octorok(700, 800, 3, 'blue', 2))
    
    if not player.unlocked_door: #only draws door if it has not been unlocked
        locked_door_list.append(LockedDoor(800,400,locked_door))
        
    for i in range(0,int(WIDTH/TILESIZE)): #horizontal
        wall_list.append(Wall(i*TILESIZE-1100,200,green_rock))
        wall_list.append(Wall(i*TILESIZE+1100,200,green_rock))
        wall_list.append(Wall(i*TILESIZE-500,1300,green_rock))
        wall_list.append(Wall(i*TILESIZE+1500,1300,green_rock))
    
    for i in range(0,int(HEIGHT/TILESIZE)): #vertical
        wall_list.append(Wall(0,i*TILESIZE+1000,green_rock))
        wall_list.append(Wall(100,i*TILESIZE+1000,green_rock))
        wall_list.append(Wall(1700,i*TILESIZE+900,green_rock))
        wall_list.append(Wall(1700,i*TILESIZE-800,green_rock))
    
    for i in range(3,5): #horizontal 2
        wall_list.append(Wall(i*TILESIZE,700,snail_rock))
    for i in range(1,3): #vertical 2
        background_list.append(BackgroundTile(800,i*TILESIZE+200,brown_bridge_vertical))
        background_list.append(BackgroundTile(900,i*TILESIZE+200,brown_bridge_vertical))
        
    for i in range(1,8): #horizontal 7
        wall_list.append(Wall(i*TILESIZE,400,water_middle_bottom))
        wall_list.append(Wall(i*TILESIZE,300,water_middle))
        wall_list.append(Wall(i*TILESIZE+900,400,water_middle_bottom))
        wall_list.append(Wall(i*TILESIZE+900,300,water_middle))
    for i in range(1,8): #vertical 7
        wall_list.append(Wall(0,i*TILESIZE+200,water_middle))
        wall_list.append(Wall(100,i*TILESIZE+200,water_middle_right))
    
    wall_list.append(Wall(700, 500,gravestone))
    wall_list.append(Wall(1000, 500,gravestone))
    wall_list.append(Wall(100, 300,water_middle))
    wall_list.append(Wall(100, 400,water_middle))
    
    for wall in wall_list:
        all_sprites.add(wall)
    for background in background_list:
        all_sprites.add(background)
    for door in locked_door_list:
        all_sprites.add(door)
    for enemy in octorok_list:
        all_sprites.add(enemy)

def draw_room_6():
    global wall_list, octorok_list, disp_winning_text
    disp_winning_text = True
    pygame.mixer.Channel(3).play(pygame.mixer.Sound('Sounds/secret.wav'))
    
    for i in range(0,int(WIDTH/TILESIZE)): #horizontal
        wall_list.append(Wall(i*TILESIZE,200,green_rock))
        wall_list.append(Wall(i*TILESIZE+1100,1300,green_rock))
        wall_list.append(Wall(i*TILESIZE-1100,1300,green_rock))
    
    for i in range(0,int(HEIGHT/TILESIZE)): #vertical
        wall_list.append(Wall(1700,i*TILESIZE+300,green_rock))
        wall_list.append(Wall(0,i*TILESIZE+300,green_rock))
    
    background_list.append(BackgroundTile(750,300,triforce_image))
    wall_list.append(Wall(100, 300,gravestone))
    wall_list.append(Wall(1600, 300,gravestone))
    
    for wall in wall_list:
        all_sprites.add(wall)
    for background in background_list:
        all_sprites.add(background)

def title_screen():
    global music_count, disp_winning_text
    screen.blit(title_screen_image, (0,0))
    disp_winning_text = False
    if music_count == 0: #makes music start once
        play_intro_music()
        music_count += 1

#Game Loop
def main():
    global item_used, animation_count, sword_out, music_count
    add_player_sprite() #adds player to sprite group
    running = True
    disp_title_screen = True
    while running:
        #keeps loop running at the right speed
        clock.tick(FPS)
        #process input (events)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN: #happens if key is pressed down
                if event.key == pygame.K_SPACE and player.sword_get and not sword_out and not player.stunned: #space bar is for using an item, item animation happens when the sword_out is false
                    animation_count = 0 #resets animation count when swinging sword
                    item_used = True #plays out item use animation
                    all_sprites.add(Sword()) #sword is added as a sprite
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound('Sounds/sword_slash.wav'))
                
                if event.key == pygame.K_c: #space bar is for using an item, item animation happens when the sword_out is false
                    animation_count = 0 #resets animation count when swinging sword
                    item_used = True #plays out item use animation
                
                if event.key == pygame.K_r: #resets game to title screen
                    disp_title_screen = True
                    change_room()
                    title_screen()
                if disp_title_screen and event.key == pygame.K_RETURN: #starts game when pressing enter
                    disp_title_screen = False
                    music_count = 0
                    play_overworld_music() #plays overworld music
                    change_room()
                    draw_room_1() #draws the room at the start of the game

        # Update
        all_sprites.update()
            
    
        # Draw / render
        if disp_title_screen:
            title_screen()
        else: #only draws level if not in title screen
            screen.fill(GROUND_COLOR)
            all_sprites.draw(screen)
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, TILESIZE*2)) #draws menu background
            draw_winning_text()
            draw_menu()
        pygame.display.update()

    pygame.quit()

main()