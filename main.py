#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Modules
from operator import itemgetter
import pygame, random, math, pickle, datetime, os

pygame.init()

########################################################################################################################
########################################################################################################################
'                                             **** GLOBAL VARIABLES ****                                               '
########################################################################################################################
########################################################################################################################

# PHYSICS
drag = 0.999
gravity_angle, gravity_distance = math.pi, 0.002

# DISPLAY/COLOURS
# set screen position
x, y = 1920 // 4, 1080 // 4
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)
WIDTH, HEIGHT = 768, 432
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Master Blaster")
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# FONTS
TITLE_FONT = pygame.font.Font(os.path.normpath("font/Title font.otf"), 30)
NEW_BODY_FONT = pygame.font.Font(os.path.normpath("font/New Body Font.otf"), 20)
HEADER_FONT = pygame.font.Font(os.path.normpath("font/Header font.ttf"), 20)
BODY_FONT = pygame.font.Font(os.path.normpath("font/Body font.ttf"), 20)
BODY_ITALIC_FONT = pygame.font.Font(os.path.normpath("font/Body italic.ttf"), 20)
TABLE_FONT = pygame.font.Font(os.path.normpath("font/Body font.ttf"), 13)
TABLE_ITALIC_FONT = pygame.font.Font(os.path.normpath("font/Body italic.ttf"), 13)
HUD_FONT = pygame.font.SysFont("monospace", 15)

# SOUND FX
SFX_VOLUME = 1
MUSIC_VOLUME = 1
HIT_SOUND = pygame.mixer.Sound(os.path.normpath("sound/hit.wav"))
HIT_SOUND.set_volume(0.1 *SFX_VOLUME)
GAME_PAUSED_SOUND = pygame.mixer.Sound(os.path.normpath("sound/Game Paused Sound.ogg"))
GAME_PAUSED_SOUND.set_volume(0.8)
MENU_SCROLL_SOUND = pygame.mixer.Sound(os.path.normpath("sound/menu scroll sound.wav"))
MENU_SCROLL_SOUND.set_volume(0.2)
MENU_SELECT_SOUND = pygame.mixer.Sound(os.path.normpath("sound/menu select sound.wav"))
MENU_SELECT_SOUND.set_volume(0.3)

########################################################################################################################
########################################################################################################################
'                                             **** GLOBAL FUNCTIONS ****                                               '
########################################################################################################################
########################################################################################################################
def quit_flag():
    dir.quit_flag = True

def read_high_scores():
    with open(os.path.normpath('data/high scores.txt'), 'rb') as f:
        high_scores = pickle.load(f)
        return high_scores

def write_high_scores(name, high_score, high_scores):
        high_scores.append((name, high_score, datetime.datetime.now().strftime('%d/%b/%Y - %H:%M')))
        high_scores = sorted(high_scores, key=itemgetter(1), reverse=True)[:10]
        with open(os.path.normpath('data/high scores.txt'), 'wb') as f:
            pickle.dump(high_scores, f)

def blit_text(surface, text, position, max_width, font, colour):
        words = text.split()  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        max_width = max_width
        x, y = position
        for word in words:

            word_surface = font.render(word, 0, colour)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = position[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = position[0]  # Reset the x.
        y += word_height  # Start on new row.

def colour():
    red = (random.randint(0,190))
    green = (random.randint(0,50))
    blue = (random.randint(0,255))
    colour = (red, green, blue)
    return colour

def lightning_red_stem_colours():
    red = (random.randint(150, 255))
    green = (random.randint(50, 150))
    blue = (random.randint(80, 200))
    colour = (red, green, blue)
    return colour

def lightning_red_fork_colours():
    red = (random.randint(30, 150))
    green = (random.randint(0, 50))
    blue = (random.randint(20, 80))
    colour = (red, green, blue)
    return colour

def lightning_blue_stem_colours():
    red = (random.randint(80, 200))
    green = (random.randint(50, 150))
    blue = (random.randint(150, 255))
    colour = (red, green, blue)
    return colour

def lightning_blue_fork_colours():
    red = (random.randint(20, 80))
    green = (random.randint(0, 50))
    blue = (random.randint(30, 150))
    colour = (red, green, blue)
    return colour

def afterburner_colours():
    red = (random.randint(220,225))
    green = (random.randint(220,255))
    blue = (random.randint( 150,255))
    colour = (red, green, blue)
    return colour

def explosion_colours():
    red = (random.randint(200, 255))
    green = (random.randint(0, 200))
    blue = (random.randint(0, 255))
    colour = (red, green, blue)
    return colour

def damage_colours():
    red = (random.randint(0,50))
    green = (random.randint(180,210))
    blue = (random.randint(200,255))
    colour = (red, green, blue)
    return colour

def booster_colours():
    red = (random.randint(0,150))
    green = (random.randint(25,200))
    blue = (random.randint(80,255))
    colour = (red, green, blue)
    return colour

def damage(explosion_location, particles):
    for number in range(random.randint(17, 33)):
        particle = Particle(explosion_location.x, explosion_location.y - 10, damage_colours(), 2, random.randint(1,4))
        particles.append(particle)

def explosion(enemy, particles):
    for number in range(random.randint(17, 53)):
        particle = Particle(enemy.x, enemy.y, explosion_colours(), random.randint(1, 5), random.randint(1, 4))
        particles.append(particle)

def glancing_hit(enemy, particles):
    for number in range(random.randint(3, 7)):
        particle = Spark(enemy.x, enemy.y, damage_colours(), random.randint(1, 5), 1)
        particles.append(particle)

def vanish(position, particles):
    for number in range(20):
        particle = Spark( position*30, HEIGHT - 25, WHITE, 5, 1)
        particles.append(particle)

def sumVectors(angle_1, distance_1, angle_2, distance_2):
    x = (math.sin(angle_1) * distance_1) + (math.sin(angle_2) * distance_2)
    y = (math.cos(angle_1) * distance_1) + (math.cos(angle_2) * distance_2)
    angle = 0.5 * math.pi - math.atan2(y, x)
    speed = math.hypot(x, y)
    return (angle, speed)

def main_menu_background_update():
    afterburner = AfterBurner(main_menu_scene.defender, main_menu_scene.movement_x, main_menu_scene.movement_y) 
    main_menu_scene.particles.append(afterburner)
    stars_ = random.randint(0, 13)
    if stars_ == 7:
        star = Star()
        main_menu_scene.particles.append(star)
    booster = Booster(main_menu_scene.defender, main_menu_scene.movement_x, main_menu_scene.movement_y)
    main_menu_scene.particles.append(booster)
    main_menu_scene.defender.bounce()
    for particle in main_menu_scene.particles:
        if particle.delete():
            main_menu_scene.particles.remove(particle)
        particle.update()

def main_menu_background_draw():
    for particle in main_menu_scene.particles:
        particle.display()   
    else: main_menu_scene.defender.display()

def display_game():
    #this will display the game behind some menus
    for pickup in game_play_scene.pickups:
        pickup.display()                 
    for i in range(game_play_scene.lives):
        heart = Heart()
        heart.display(i)
    for particle in game_play_scene.particles:
        particle.display()   
    for projectile in game_play_scene.projectiles:
        projectile.display()
    for enemy in game_play_scene.enemies:
        enemy.display()

    if (game_play_scene.draw_orientation[0] and game_play_scene.draw_orientation[1]) or (game_play_scene.draw_orientation[2] and game_play_scene.draw_orientation[3]): 
        game_play_scene.defender.display()
    elif game_play_scene.draw_orientation[0]: game_play_scene.defender.display_right()
    elif game_play_scene.draw_orientation[1]: game_play_scene.defender.display_left()
    elif game_play_scene.draw_orientation[2]: game_play_scene.defender.display_forward()
    elif game_play_scene.draw_orientation[3]: game_play_scene.defender.display_back()
    else: game_play_scene.defender.display()

    paused_text = HUD_FONT.render("Paused", 1, (WHITE))
    paused_text_width = paused_text.get_rect().width
    SCREEN.blit(game_play_scene.display_score, (WIDTH *0.84, HEIGHT *0.96))
    SCREEN.blit(game_play_scene.selected_weapon_text, (WIDTH *0.01, HEIGHT *0.85))
    SCREEN.blit(game_play_scene.ammo_text, (WIDTH *0.01, HEIGHT *0.9))

########################################################################################################################
########################################################################################################################
'                                             **** DIRECTOR ****                                                       '
########################################################################################################################
########################################################################################################################

class Director:
 
    def __init__(self):

        self.scene = None
        self.quit_flag = False
        self.clock = pygame.time.Clock()
    
    def loop(self):
        # Main game loop
        
        while not self.quit_flag:
            time = self.clock.tick(60)
            mpos1, mpos2 = pygame.mouse.get_pos()
            
            # Exit events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_flag()
                else:
                    self.scene.on_event(event, mpos1, mpos2)
 
            # Update scene
            self.scene.on_update()
 
            # Draw the screen
            self.scene.on_draw(mpos1, mpos2)
            pygame.display.flip()

########################################################################################################################
########################################################################################################################
'                                             **** PARTICLE CLASSES ****                                               '
########################################################################################################################
########################################################################################################################
  
class Particle:

    def __init__(self, x, y, colours, speed, size):   
        self.x = x
        self.origin_x, self.origin_y = x, y
        self.y = y 
        self.distance = 0
        self.size = size
        self.colour = colours
        self.thickness = 1
        self.speed = speed
        self.angle = random.uniform(0, math.pi*2)
        self.shrink_tally = 0
        self.distance_one = random.randint(17, 33)
        self.distance_two = random.randint(33, 66)
        self.distance_three = random.randint(66, 99)
        self.distance_four = random.randint(99, 133)

    def display(self):
        pygame.draw.circle(SCREEN, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)
        
    def update(self):
        (self.angle, self.speed) = sumVectors(self.angle, self.speed, gravity_angle, gravity_distance)
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= drag

        dx = self.x - self.origin_x
        dy = self.y - self.origin_y

        self.distance = math.hypot(dx, dy)

        if self.distance > self.distance_one and self.size > 1 and self.shrink_tally == 0:
            self.size += -1
            self.shrink_tally += 1
        if self.distance > self.distance_two and self.size > 1 and self.shrink_tally < 2:
            self.size += -1
            self.shrink_tally += 1
        if self.distance > self.distance_three and self.size > 1 and self.shrink_tally < 3:
            self.size += -1
            self.shrink_tally += 1

    def delete(self):       
        if self.distance > self.distance_four:
             return True
        else:
            return False


class Spark(Particle):

    def delete(self):
        self.distance_one = 20  
        if self.distance > self.distance_one:
            return True
        else:
            return False


class Star:

    def __init__(self):
        self.x = random.randint(1, WIDTH)
        self.y = 0
        self.size = 1
        self.thickness = 4
        self.speed = random.uniform(2, 20)
        self.angle = math.pi

    def display(self):
        pygame.draw.rect(SCREEN, WHITE, (self.x, self.y, self.size, self.thickness))
        
    def update(self):
        self.y +=  self.speed

    def delete(self):
        if self.y >HEIGHT + 10:
            return True
        else:
            return False


class Booster(Star):

    def __init__(self, defender, movement_x, movement_y):
        self.movement_x = movement_x
        self.movement_y = movement_y
        self.origin_x, self.origin_y = defender.x, defender.y  
        
        def which_booster(i):
            if i[0]: booster, a, b = defender.y, 3, 1
            else: booster, a, b = defender.x, 4, 2

            which_booster = random.randint(1, 2)

            if which_booster == 1:
                coordinate = random.uniform((booster - a *defender.size) + 1, (booster - b *defender.size )- 1)
            else:
                coordinate = random.uniform((booster + b *defender.size) + 1, (booster + a *defender.size) - 1)
            
            if i[0] and i[1]:
                self.x = defender.x + 4*defender.size 
                self.y = coordinate
            elif i[0] and not i[1]:
                self.x = defender.x - 4*defender.size
                self.y = coordinate   
            elif i[1] and not i[0]: 
                self.x = coordinate
                self.y = defender.y - 3*defender.size
            else:
                self.y = defender.y + 3*defender.size
                self.x = coordinate             
            return self.x, self.y

        if self.movement_y[1] and not self.movement_y[0]: 
            which_booster([False, True])
        elif not self.movement_y[0] and not self.movement_y[1]: 
            if self.movement_x[0] and not self.movement_x[1]: 
                which_booster([True,True])
            elif self.movement_x[1] and not self.movement_x[0]:
                which_booster([True, False])
            else:
                which_booster([False, False])
        else: 
            which_booster([False, False])

        dx = self.x - self.origin_x
        dy = self.y - self.origin_y
        
        self.distance = math.hypot(dx, dy) 
        self.size = random.randint(1, 6)
        self.colour = booster_colours()
        self.thickness = 1
        self.speed = 5
        self.shrink_tally = 0
        self.distance_one = random.randint(10, 20)
        self.distance_two = random.randint(20, 30)
        self.distance_three = random.randint(30, 40)
        self.distance_four = random.randint(40, 50)
        
    def display(self):
        pygame.draw.circle(SCREEN, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)
        
    def update(self):
        if self.movement_y[1] and not self.movement_y[0]: self.y +=  -self.speed
        elif not self.movement_y[0] and not self.movement_y[1]:
            if self.movement_x[0] and not self.movement_x[1]: self.x += self.speed 
            elif self.movement_x[1] and not self.movement_x[0]: self.x += -self.speed
            else: 
                self.y += self.speed
        else: self.y += self.speed

        dx = self.x - self.origin_x
        dy = self.y - self.origin_y

        self.distance = math.hypot(dx, dy)

        if self.distance > self.distance_one and self.size > 1 and self.shrink_tally == 0:
            self.size += -1
            self.shrink_tally += 1
        if self.distance > self.distance_two and self.size > 1 and self.shrink_tally < 2:
            self.size += -1
            self.shrink_tally += 1
        if self.distance > self.distance_three and self.size > 1 and self.shrink_tally < 3:
            self.size += -1
            self.shrink_tally += 1

    def delete(self):
        if self.distance > self.distance_four:
            return True
        else:
            return False
        
class AfterBurner(Booster):
    def __init__(self, defender, movement_x, movement_y):
        
        n = random.randint(0, 2)

        self.speed = 7
        self.y = defender.y + 4 * defender.size
        self.x = random.uniform((defender.x - defender.size) + 1, (defender.x + defender.size )- 1)
        self.movement_x = movement_x
        self.movement_y = movement_y
        self.origin_x, self.origin_y = defender.x, defender.y

        dx = self.x - self.origin_x
        dy = self.y - self.origin_y
        
        self.distance = math.hypot(dx, dy) 
        self.size = random.randint(2, 4)
        if n == 2: self.colour = afterburner_colours()
        else: self.colour = booster_colours()
        self.thickness = 1
        self.speed = 5
        self.shrink_tally = 0
        self.distance_one = random.randint(10, 20)
        self.distance_two = random.randint(30, 40)
        self.distance_three = random.randint(40, 60)
        self.distance_four = random.randint(60, 80)
    
    def display(self):
        pygame.draw.circle(SCREEN, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)

class RocketBooster(Star):
    def __init__(self, rocket):
        self.speed = 7
        self.y = rocket.y + 1 * rocket.size
        self.x = random.uniform(rocket.x + 1, rocket.x + rocket.size - 1)
        self.origin_x, self.origin_y = rocket.x, rocket.y
        self.distance = 0
        self.size = random.randint(2, 4)
        self.colour = damage_colours()
        self.thickness = 1
        self.speed = 5
        self.shrink_tally = 0
        self.distance_one = random.randint(10, 20)
        self.distance_two = random.randint(30, 40)
        self.distance_three = random.randint(40, 60)
        self.distance_four = random.randint(60, 80)
    
    def display(self):
        pygame.draw.circle(SCREEN, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)
    
    def update(self):
        self.y +=  self.speed

        dx = self.x - self.origin_x
        dy = self.y - self.origin_y

        self.distance = math.hypot(dx, dy)

        if self.distance > self.distance_one and self.size > 1 and self.shrink_tally == 0:
            self.size += -1
            self.shrink_tally += 1
        if self.distance > self.distance_two and self.size > 1 and self.shrink_tally < 2:
            self.size += -1
            self.shrink_tally += 1
        if self.distance > self.distance_three and self.size > 1 and self.shrink_tally < 3:
            self.size += -1
            self.shrink_tally += 1

    def delete(self):
        if self.distance > self.distance_four:
            return True
        else:
            return False

class ElectricalDischarge():
    def __init__(self, x1, y1, x2, y2, stem_colour, fork_colour, angle):
        self.segments = []
        self.new_segments = []
        self.stem_colour = stem_colour
        self.fork_colour = fork_colour
        self.life_time = random.uniform(0.01, 0.1)
        self.initial_time = pygame.time.get_ticks()
    
        angle = angle
        hit_radius = 3
        origin_radius = 1
        hit_angle = random.uniform(0, math.pi*2)

        x1 = x1 + origin_radius *math.sin(hit_angle)
        y1 = y1 - origin_radius *math.cos(hit_angle)

        x2 = x2 + hit_radius *math.sin(hit_angle)
        y2 = y2 - hit_radius *math.cos(hit_angle)

        size = math.hypot(x1-x2, y1-y2)
        i = 100
    
        segment = [(x1, y1), (x2, y2), (size), (angle), (i), (True)]
        self.segments.append(segment)
        

        for n in range(5):
            for new_segment in self.new_segments:
                self.segments.append(new_segment)
            
            self.new_segments[:] = []

            for segment in self.segments:
                x1, y1 = segment[0]
                x3, y3 = segment[1]
                size = segment[2] *0.5
       
                xi = (x1 + x3) / 2
                yi = (y1 + y3) / 2
                i = segment[4] *0.5
                
                perpendicular_angle = segment[3] -0.1
                offset = random.uniform(-i, i) 
                size1 = math.sqrt(size**2 + offset**2)
                
                x2 = xi + offset *math.sin(perpendicular_angle)
                y2 = yi - offset *math.cos(perpendicular_angle)

                angle1 = segment[3] + math.copysign(math.acos(size /size1), -offset)
                angle2 = segment[3] - math.copysign(math.acos(abs(offset) /size1), -offset)

                if segment[5]:
                    segment1 = [(x1, y1), (x2, y2), (size1), (angle1), (i), (True)]
                    segment2 = [(x2, y2), (x3, y3), (size1), (angle2), (i), (True)]
                else:
                    segment1 = [(x1, y1), (x2, y2), (size1), (angle1), (i), (False)]
                    segment2 = [(x2, y2), (x3, y3), (size1), (angle2), (i), (False)]

                self.new_segments.append(segment1)
                self.new_segments.append(segment2)

                got_fork = random.randint(1, 3)

                if got_fork == 3:
                    size2 = size1 *random.uniform(0.7, 0.8)
                    fork_angle = angle + random.uniform(-0.5, 0.5)

                    x4 = x2 + size2 *math.sin(fork_angle)
                    y4 = y2 - size2 *math.cos(fork_angle)
                    segment3 = [(x2, y2), (x4, y4), (size2), (fork_angle), (i), (False)]
                    self.new_segments.append(segment3)
                
            self.segments[:] = []

        self.segments[:] = []
        for segment in self.new_segments:
            self.segments.append(segment)
         
    def display(self):
        for segment in self.segments:
            if segment[5]:
                pygame.draw.line(SCREEN, self.stem_colour, (segment[0]), (segment[1]))
            else:
                pygame.draw.line(SCREEN, self.fork_colour, (segment[0]), (segment[1]))
    
    def update(self):
        pass
            
    def delete(self):
        if ((self.life_time * 1000) + self.initial_time) < pygame.time.get_ticks():
            return True
        else:
            return False

########################################################################################################################
########################################################################################################################
'                                             **** PICKUP CLASSES ****                                                 '
########################################################################################################################
########################################################################################################################

class WeaponPickup():

    def __init__(self, game_play_scene, x, y):

        self.size = 5
        self.x = x
        self.y = y
        self.thickness = 0
        self.colour = 100, 100, 100
        self.speed = 0.5
        self.type = 1
        self.weapon_type = random.randint(0, len(game_play_scene.collectable_weapons) - 1)

    def display(self):
        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y - self.size, self.size, self.thickness))

    def update(self):
        self.y += self.speed

    def delete(self, owner):
        if self.y + 3* self.size > HEIGHT:
            owner.pickups.remove(self)


    def collected(self, defender):
        dx = (self.x + self.size) - (defender.x + (2*defender.size / 2)) 
        dy = self.y - (defender.y + (3*defender.size / 2))

        proximity = math.hypot(dx, dy)       
        if proximity < self.size + defender.size *4:
            return True

class AmmoPickup():
    def __init__(self, game_play_scene, x, y):

        self.size = 5
        self.x = x
        self.y = y
        self.thickness = 0
        self.colour = WHITE
        self.speed = 0.5
        self.type = 2
        self.weapon_type = random.randint(0, len(game_play_scene.weapon_inventory) - 1)
        self.contents = random.randint(1, 20)

    def display(self):
        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y - self.size, self.size, self.thickness))

    def update(self):
        self.y += self.speed

    def delete(self, owner):
        if self.y + 3* self.size > HEIGHT:
            owner.pickups.remove(self)


    def collected(self, defender):
        dx = (self.x + self.size) - (defender.x + (defender.size / 2)) 
        dy = self.y - (defender.y + (defender.size / 2))

        proximity = math.hypot(dx, dy)       
        if proximity < self.size + defender.size *4:
            return True

class ExtraLife():
    def __init__(self, game_play_scene, x, y):

        self.size = 1
        self.x = x
        self.y = y
        self.thickness = 0
        self.colour = 255, 150, 150
        self.speed = 0.5
        self.contents = random.randint(0, 3)
        self.type = 3

    def display(self):
            
        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x , self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 2*self.size, self.y- 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + 2*self.size, self.y - 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 2*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + 2*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 2*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + 2*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 3*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + 3*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 4*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + 4*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 3*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + 3*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 2*self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + 2*self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 3*self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + 3*self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + 2*self.size, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 2*self.size, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y + 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y + 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y + 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y + 4*self.size, self.size, self.thickness))

    def update(self):
        self.y += self.speed

    def delete(self, owner):
        if self.y + 3* self.size > HEIGHT:
            owner.pickups.remove(self)


    def collected(self, defender):
        dx = (self.x + self.size) - (defender.x + (defender.size / 2)) 
        dy = self.y - (defender.y + (defender.size / 2))

        proximity = math.hypot(dx, dy)       
        if proximity < self.size + defender.size*4:
            return True
########################################################################################################################
########################################################################################################################
'                                             **** WEAPON CLASSES ****                                                 '
########################################################################################################################
########################################################################################################################

class Gun():
    def __init__(self, game_play_scene):

        self.ammo = math.inf
        self.fire_mode = 'semi'
        self.user = game_play_scene
        self.primary_fire_sound = pygame.mixer.Sound(os.path.normpath("sound/Gun Primary Fire Sound.ogg"))
        self.secondary_fire_sound = pygame.mixer.Sound(os.path.normpath("sound/Gun Secondary Fire Sound.ogg"))
        self.text = "Gun"

    def primary_fire(self):
        projectile = Projectile(self.user.defender.x, self.user.defender.y)
        game_play_scene.projectiles.append(projectile)
        self.primary_fire_sound.play(0)
        self.ammo -= 1

    def secondary_fire(self):
        projectile = Projectile(self.user.defender.x, self.user.defender.y)
        game_play_scene.projectiles.append(projectile)
        self.secondary_fire_sound.play(0)
        self.ammo -= 1

class RocketLauncher():
    def __init__(self, game_play_scene):

        self.ammo = 100
        self.fire_mode = 'semi'
        self.user = game_play_scene
        self.primary_fire_sound = pygame.mixer.Sound(os.path.normpath("sound/Rocket Launcher Primary Fire Sound.ogg"))
        self.secondary_fire_sound = pygame.mixer.Sound(os.path.normpath("sound/Rocket Launcher Secondary Fire Sound.ogg"))
        self.text = "Rocket Launcher"

    def primary_fire(self):
        projectile = Rocket(self.user.defender.x, self.user.defender.y)
        game_play_scene.projectiles.append(projectile)
        self.primary_fire_sound.play(0)
        self.ammo -= 1

    def secondary_fire(self):
        projectile = Rocket(self.user.defender.x, self.user.defender.y)
        game_play_scene.projectiles.append(projectile)
        self.secondary_fire_sound.play(0)
        self.ammo -= 1

class BombLauncher():
    def __init__(self, game_play_scene):

        self.ammo = 100
        self.fire_mode = 'semi'
        self.user = game_play_scene
        self.primary_fire_sound = pygame.mixer.Sound(os.path.normpath("sound/Bomb Launcher Primary Fire Sound.ogg"))
        self.secondary_fire_sound = pygame.mixer.Sound(os.path.normpath("sound/Bomb Launcher Secondary Fire Sound.ogg"))
        self.text = "Remote Bombs"

    def primary_fire(self):
        projectile = Bomb(self.user.defender.x, self.user.defender.y)
        game_play_scene.projectiles.append(projectile)
        self.primary_fire_sound.play(0)
        self.ammo -= 1

    def secondary_fire(self):
        projectile = Bomb(self.user.defender.x, self.user.defender.y)
        game_play_scene.projectiles.append(projectile)
        self.secondary_fire_sound.play(0)
        self.ammo -= 1

class LaserGun():
    def __init__(self, game_play_scene):

        self.ammo = 100
        self.fire_mode = 'semi'
        self.user = game_play_scene
        self.primary_fire_sound = pygame.mixer.Sound(os.path.normpath("sound/Laser Gun Primary Fire Sound.ogg"))
        self.secondary_fire_sound = pygame.mixer.Sound(os.path.normpath("sound/Laser Gun Secondary Fire Sound.ogg"))
        self.text = "Laser Gun"

    def primary_fire(self):
        projectile = Laser(self.user.defender.x, self.user.defender.y)
        game_play_scene.projectiles.append(projectile)
        self.primary_fire_sound.play(0)
        self.ammo -= 1

    def secondary_fire(self):
        projectile = Laser(self.user.defender.x, self.user.defender.y)
        game_play_scene.projectiles.append(projectile)
        self.secondary_fire_sound.play(0)
        self.ammo -= 1

class LightningGun():
    def __init__(self, game_play_scene):

        self.ammo = 1000
        self.fire_mode = 'auto'
        self.game_play_scene = game_play_scene
        self.primary_fire_sound = pygame.mixer.Sound(os.path.normpath("sound/Lightning Gun Primary Fire Sound.ogg"))
        self.secondary_fire_sound = pygame.mixer.Sound(os.path.normpath("sound/Lightning Gun Secondary Fire Sound.ogg"))
        self.text = "Lightning Gun"

    def primary_fire(self):
        projectile = Lightning(self.game_play_scene.defender.x, 
                                self.game_play_scene.defender.y - game_play_scene.defender.size * 4, 
                                self.game_play_scene.defender.x, self.game_play_scene.defender.y - 200,
                                lightning_blue_stem_colours(),
                                lightning_blue_fork_colours(),
                                math.pi * 2)
        game_play_scene.projectiles.append(projectile)
        self.primary_fire_sound.play(0)
        self.ammo -= 1

    def secondary_fire(self):
        projectile = Lightning(self.game_play_scene.defender.x, 
                                self.game_play_scene.defender.y - game_play_scene.defender.size * 4, 
                                self.game_play_scene.defender.x, self.game_play_scene.defender.y - 200,
                                lightning_red_stem_colours(),
                                lightning_red_fork_colours(),
                                math.pi * 2)
        game_play_scene.projectiles.append(projectile)
        self.secondary_fire_sound.play(0)
        self.ammo -= 1

########################################################################################################################
########################################################################################################################
'                                             **** PROJECTILE CLASSES ****                                             '
########################################################################################################################
########################################################################################################################
        
class Projectile:
    def __init__(self, x, y):
        
    
        self.size = 4
        self.power = 1
        
        self.angle = 0
        self.x = x - self.size / 2
        self.x2 = x + self.size
        self.y = y -25
        self.colour = WHITE
        self.speed = 4
        

    def display(self):
        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y, self.size, self.size))
    
    def update(self):
        self.y += -self.speed

    def position(self):
        return self.x, self.y, self.size

    def delete(self):
        if self.y + self.size < 0:
            return True
        else:
            return False

class Rocket(Projectile):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 4
        self.thickness = 0
        self.colour = WHITE
        self.power = 40
        self.blast_radius = 100
        self.speed = 4
        self.hit_detection_point = (self.x + self.size / 2), self.y
        self.sound = "".join(["Rocket Fire Sound ", str(random.randint(1, 4)), ".ogg"])

    def display(self):
        pygame.draw.polygon(SCREEN, RED, 
        ((self.x, self.y), (self.x + self.size, self.y), (self.x + self.size / 2, self.y - self.size)),
        self.thickness)
        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y, self.size, self.size))
        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y + self.size, self.size, self.size))


class Bomb(Projectile):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 4
        self.thickness = 0
        self.colour = WHITE
        self.power = 40
        self.blast_radius = 100
        self.speed = 4
        self.hit_detection_point = (self.x + self.size / 2), self.y

    def display(self):
        pygame.draw.polygon(SCREEN, RED, 
        ((self.x, self.y), (self.x + self.size, self.y), (self.x + self.size / 2, self.y - self.size)),
        self.thickness)
        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y, self.size, self.size))
        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y + self.size, self.size, self.size))


class Laser(Projectile):

    def __init__(self, x, y):
        self.x = x
        self.y = y 
        self.size = 2
        self.thickness = 30
        self.colour = WHITE
        self.power = 40
        self.blast_radius = 100
        self.speed = 10
        self.hit_detection_point = (self.x + self.size / 2), self.y
        self.sound = "Laser Fire Sound.ogg"

    def display(self):
        
        pygame.draw.rect(SCREEN, RED, (self.x, self.y, self.size, self.thickness))

class Lightning():
    def __init__(self, x1, y1, x2, y2, stem_colour, fork_colour, angle):
        self.x, self.y = x2, y2
        self.size = 2
        self.segments = []
        self.new_segments = []
        self.stem_colour = stem_colour
        self.fork_colour = fork_colour
        self.life_time = random.uniform(0.01, 0.1)
        self.initial_time = pygame.time.get_ticks()
        self.power = 20

        hit_radius = 3
        origin_radius = 1
        hit_angle = random.uniform(0, math.pi*2)

        x1 = x1 + origin_radius *math.sin(hit_angle)
        y1 = y1 - origin_radius *math.cos(hit_angle)

        x2 = x2 + hit_radius *math.sin(hit_angle)
        y2 = y2 - hit_radius *math.cos(hit_angle)

        size = math.hypot(x1-x2, y1-y2)
        i = 100
    
        segment = [(x1, y1), (x2, y2), (size), (angle), (i), (True)]
        self.segments.append(segment)
        

        for n in range(5):
            for new_segment in self.new_segments:
                self.segments.append(new_segment)
            
            self.new_segments[:] = []

            for segment in self.segments:
                x1, y1 = segment[0]
                x3, y3 = segment[1]
                size = segment[2] *0.5
       
                xi = (x1 + x3) / 2
                yi = (y1 + y3) / 2
                i = segment[4] *0.5
                
                perpendicular_angle = segment[3] -0.1
                offset = random.uniform(-i, i) 
                size1 = math.sqrt(size**2 + offset**2)
        
                x2 = xi + offset *math.sin(perpendicular_angle)
                y2 = yi - offset *math.cos(perpendicular_angle)

                angle1 = segment[3] + math.copysign(math.acos(size /size1), -offset)
                angle2 = segment[3] - math.copysign(math.acos(abs(offset) /size1), -offset)

                if segment[5]:
                    segment1 = [(x1, y1), (x2, y2), (size1), (angle1), (i), (True)]
                    segment2 = [(x2, y2), (x3, y3), (size1), (angle2), (i), (True)]
                else:
                    segment1 = [(x1, y1), (x2, y2), (size1), (angle1), (i), (False)]
                    segment2 = [(x2, y2), (x3, y3), (size1), (angle2), (i), (False)]

                self.new_segments.append(segment1)
                self.new_segments.append(segment2)

                got_fork = random.randint(1, 3)

                if got_fork == 3:
                    size2 = size1 *random.uniform(0.7, 0.8)
                    fork_angle = angle + random.uniform(-0.5, 0.5)

                    x4 = x2 + size2 *math.sin(fork_angle)
                    y4 = y2 - size2 *math.cos(fork_angle)
                    segment3 = [(x2, y2), (x4, y4), (size2), (fork_angle), (i), (False)]
                    self.new_segments.append(segment3)
                
            self.segments[:] = []

        self.segments[:] = []
        for segment in self.new_segments:
            self.segments.append(segment)
         
    def display(self):
        for segment in self.segments:
            if segment[5]:
                pygame.draw.line(SCREEN, self.stem_colour, (segment[0]), (segment[1]))
            else:
                pygame.draw.line(SCREEN, self.fork_colour, (segment[0]), (segment[1]))
    
    def update(self):
        pass
            
    def delete(self):
        if ((self.life_time * 1000) + self.initial_time) < pygame.time.get_ticks():
            return True
        else:
            return False

########################################################################################################################
########################################################################################################################
'                                             **** PLAYER CHARACTER ****                                               '
########################################################################################################################
########################################################################################################################

class Defender():
    def __init__(self, x, y):
        self.x = x
        self.y = y 
        self.colour = 70, 70, 70
        self.thickness = 3
        self.size = 4
        
    def display(self):
        #forwards facedown
        pygame.draw.rect(SCREEN, (20, 20, 80), (self.x, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (20, 20, 80), (self.x - self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 2*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 3*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 4*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 5*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 6*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 2*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 3*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 4* self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 5* self.size, self.y, self.size, self.thickness))

        pygame.draw.rect(SCREEN, (20, 20, 80), (self.x, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (20, 20, 80), (self.x - self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 2*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 3*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 4*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 5*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 6*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 2*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 3*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 4* self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 5* self.size, self.y - self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, (20, 20, 80), (self.x, self.y - 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (20, 20, 80), (self.x - self.size, self.y - 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 2*self.size, self.y - 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 3*self.size, self.y - 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 4*self.size, self.y - 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y - 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 2*self.size, self.y - 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 3*self.size, self.y - 2*self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, (20, 20, 80), (self.x, self.y - 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (20, 20, 80), (self.x - self.size, self.y - 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 2*self.size, self.y - 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 3*self.size, self.y - 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 4*self.size, self.y - 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y - 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 2*self.size, self.y - 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 3*self.size, self.y - 3*self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y - 4*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y - 4*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 2*self.size, self.y - 4*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y - 4*self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y - 5*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y - 5*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 2*self.size, self.y - 5*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + self.size, self.y - 5*self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y - 6*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y - 6*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 2*self.size, self.y - 6*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + self.size, self.y - 6*self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y - 7*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y - 7*self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 2*self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 3*self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 4*self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 2*self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 3*self.size, self.y + self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, (40, 40, 40), (self.x, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (40, 40, 40), (self.x - self.size, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (40, 40, 40), (self.x - 2*self.size, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 3*self.size, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 4*self.size, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (40, 40, 40), (self.x + self.size, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 2*self.size, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 3*self.size, self.y + 2*self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, (40, 40, 40), (self.x, self.y + 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (40, 40, 40), (self.x - self.size, self.y + 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (40, 40, 40), (self.x - 2*self.size, self.y + 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (40, 40, 40), (self.x + self.size, self.y + 3*self.size, self.size, self.thickness))

    def display_right(self):

        #moving left
        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (20, 20, 80), (self.x - self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 2*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 3*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 2*self.size, self.y, self.size, self.thickness))

        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (20, 20, 80), (self.x - self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 2*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 3*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 2*self.size, self.y - self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y - 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (20, 20, 80), (self.x - self.size, self.y - 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 2*self.size, self.y - 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + self.size, self.y - 2*self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y - 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (20, 20, 80), (self.x - self.size, self.y - 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + self.size, self.y - 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 2*self.size, self.y - 3*self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y - 4*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y - 4*self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, (190,190,190), (self.x, self.y - 5*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y - 5*self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, (190,190,190), (self.x, self.y - 6*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y - 6*self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y - 7*self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 2*self.size, self.y + self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, (40, 40, 40), (self.x, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (40, 40, 40), (self.x - self.size, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + self.size, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 2*self.size, self.y + 2*self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, (40, 40, 40), (self.x, self.y + 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (40, 40, 40), (self.x - self.size, self.y + 3*self.size, self.size, self.thickness))

    def display_left(self):
        #moving right
        pygame.draw.rect(SCREEN, (20, 20, 80), (self.x, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 2*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 3*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 2*self.size, self.y, self.size, self.thickness))
        

        pygame.draw.rect(SCREEN, (20, 20, 80), (self.x, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 2*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 3*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 2*self.size, self.y - self.size, self.size, self.thickness))


        pygame.draw.rect(SCREEN, (20, 20, 80), (self.x, self.y - 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y - 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 2*self.size, self.y - 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + self.size, self.y - 2*self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, (20, 20, 80), (self.x, self.y - 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y - 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + self.size, self.y - 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 2*self.size, self.y - 3*self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y - 4*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y - 4*self.size, self.size, self.thickness))
        

        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y - 5*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - self.size, self.y - 5*self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y - 6*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - self.size, self.y - 6*self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y - 7*self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 2*self.size, self.y + self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, (40, 40, 40), (self.x, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (40, 40, 40), (self.x - self.size, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + self.size, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 2*self.size, self.y + 2*self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, (40, 40, 40), (self.x, self.y + 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (40, 40, 40), (self.x - self.size, self.y + 3*self.size, self.size, self.thickness))

    def display_forward(self):

        pygame.draw.rect(SCREEN, (20, 20, 80), (self.x, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (20, 20, 80), (self.x - self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 2*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 3*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 4*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 5*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 6*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 2*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 3*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 4* self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 5* self.size, self.y, self.size, self.thickness))

        pygame.draw.rect(SCREEN, (20, 20, 80), (self.x, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (20, 20, 80), (self.x - self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 2*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 3*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 4*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 5*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 6*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 2*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 3*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 4* self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 5* self.size, self.y - self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, (20, 20, 80), (self.x, self.y - 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (20, 20, 80), (self.x - self.size, self.y - 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 2*self.size, self.y - 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 3*self.size, self.y - 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 4*self.size, self.y - 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y - 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 2*self.size, self.y - 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 3*self.size, self.y - 2*self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, (20, 20, 80), (self.x, self.y - 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (20, 20, 80), (self.x - self.size, self.y - 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 2*self.size, self.y - 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 3*self.size, self.y - 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 4*self.size, self.y - 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y - 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 2*self.size, self.y - 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 3*self.size, self.y - 3*self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y - 4*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y - 4*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 2*self.size, self.y - 4*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y - 4*self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y - 5*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y - 5*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 2*self.size, self.y - 5*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + self.size, self.y - 5*self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y - 6*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y - 6*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 2*self.size, self.y - 6*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + self.size, self.y - 6*self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y - 7*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y - 7*self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 2*self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 3*self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 4*self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 2*self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 3*self.size, self.y + self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, (40, 40, 40), (self.x, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (40, 40, 40), (self.x - self.size, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (40, 40, 40), (self.x - 2*self.size, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 3*self.size, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 4*self.size, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (40, 40, 40), (self.x + self.size, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 2*self.size, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 3*self.size, self.y + 2*self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, (40, 40, 40), (self.x, self.y + 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (40, 40, 40), (self.x - self.size, self.y + 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (40, 40, 40), (self.x - 2*self.size, self.y + 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (40, 40, 40), (self.x + self.size, self.y + 3*self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, (40, 40, 40), (self.x, self.y + 4*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (40, 40, 40), (self.x - self.size, self.y + 4*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (40, 40, 40), (self.x - 2*self.size, self.y + 4*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (40, 40, 40), (self.x + self.size, self.y + 4*self.size, self.size, self.thickness))
    
    def display_back(self):
        pygame.draw.rect(SCREEN, (20, 20, 80), (self.x, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (20, 20, 80), (self.x - self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 2*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 3*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 4*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 5*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 6*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 2*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 3*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 4*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 5*self.size, self.y, self.size, self.thickness))

        pygame.draw.rect(SCREEN, (20, 20, 80), (self.x, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (20, 20, 80), (self.x - self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 2*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 3*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 4*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 5*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 6*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 2*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 3*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 4*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 5*self.size, self.y - self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y - 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y - 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 2*self.size, self.y - 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 3*self.size, self.y - 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 4*self.size, self.y - 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y - 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 2*self.size, self.y - 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 3*self.size, self.y - 2*self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y - 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y - 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 2*self.size, self.y - 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y - 3*self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y - 4*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y - 4*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 2*self.size, self.y - 4*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + self.size, self.y - 4*self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y - 5*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y - 5*self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, (20, 20, 80), (self.x, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (20, 20, 80), (self.x - self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 2*self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 3*self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x - 4*self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 2*self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (190,190,190), (self.x + 3*self.size, self.y + self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 2*self.size, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y + 2*self.size, self.size, self.thickness))

    def bounce(self):
        if self.x + 3*self.size > WIDTH:
            self.x = WIDTH - 3*self.size
        
        if self.x - 3*self.size < 0:
            self.x = 0 + 3*self.size

        if self.y - 7*self.size < 0:
            self.y = 0 + 7*self.size
        
        if self.y + 3*self.size > HEIGHT:
            self.y = HEIGHT - 3*self.size
    
    def position(self):
        return self.x, self.y, self.size

########################################################################################################################
########################################################################################################################
'                                             **** ENEMY CLASSES ****                                                  '
########################################################################################################################
########################################################################################################################

class Enemy():
    def update(self):
        return NotImplementedError("enemy move not implemented")

    def enemy_attack(self):
        if self.y >HEIGHT:
            return True

    def score_(self):
        return self.score
            
    def dead(self):
        if self.health < 0:
            return True

    def bounce(self):
        pass

class BossCube(Enemy):
    def __init__(self, boss_guy, x, y, theta, identity):

        self.theta = theta
        self.boss_guy = boss_guy
        self.size = 6
        self.x = x
        self.y = y 
        self.colour = 120, 120, 120
        self.angle = math.pi/2
        self.health = 2
        self.score = 100
        self.thickness = 0
        self.spin_timer = pygame.time.get_ticks()
        self.identity = identity

    def display(self):
        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y, self.size, self.size))
    
    def update(self):
        if self.identity:
            self.theta += 0.01
            self.x = (self.boss_guy.x + self.boss_guy.inner_shield_radius * math.cos(self.theta)) - (self.size / 2)
            self.y = (self.boss_guy.y + self.boss_guy.inner_shield_radius * math.sin(self.theta)) - (self.size / 2)
        else:
            self.theta -= 0.01
            self.x = (self.boss_guy.x + self.boss_guy.outer_shield_radius * math.cos(self.theta)) - (self.size / 2)
            self.y = (self.boss_guy.y + self.boss_guy.outer_shield_radius * math.sin(self.theta)) - (self.size / 2)
    
    def dead(self):
        if self.health < 0:
            return True

    def hit(self, projectile):
        dx = (self.x + (self.size / 2)) - projectile.x 
        dy = (self.y + (self.size / 2)) - projectile.y

        proximity = math.hypot(dx, dy)       
        if proximity < self.size + projectile.size:
            self.health -= projectile.power
            return True

class BossGuy(Enemy):
    def __init__(self, x, y):

        self.layer_one_cube_number = 12
        self.layer_two_cube_number = 24
        self.inner_shield_radius = 30
        self.outer_shield_radius = 60
        self.x = WIDTH *0.5
        self.y = 0 - self.inner_shield_radius
        self.inner_circumference_division = 2*math.pi / self.layer_one_cube_number
        self.outer_circumference_division = 2*math.pi / self.layer_two_cube_number
        self.size = 3
        self.angle = math.pi
        self.speed = 0.5
        self.colour = WHITE
        self.thickness = 0
        self.health = 10
        self.score = 1000
        self.origin = 0
        self.secondary_movement_mode = True

    def display(self):
        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, BLACK, (self.x - 2*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, BLACK, (self.x - 3*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 4*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 5*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, BLACK, (self.x + self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, BLACK, (self.x + 2*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + 3*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + 4*self.size, self.y, self.size, self.thickness))

        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 2*self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 3*self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 4*self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 5*self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + 2*self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + 3*self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + 4*self.size, self.y + self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, BLACK, (self.x, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, BLACK, (self.x - self.size, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 2*self.size, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (170, 170, 170), (self.x - 3*self.size, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (120,120,120), (self.x - 4*self.size, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (170, 170, 170), (self.x + 2*self.size, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (120,120,120), (self.x + 3*self.size, self.y + 2*self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y + 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y + 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (200, 200, 200), (self.x - 2*self.size, self.y + 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (170, 170, 170), (self.x - 3*self.size, self.y + 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (200, 200, 200), (self.x + self.size, self.y + 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (170, 170, 170), (self.x + 2*self.size, self.y + 3*self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y + 4*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y + 4*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (200, 200, 200), (self.x - 2*self.size, self.y + 4*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, (200, 200, 200), (self.x + self.size, self.y + 4*self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y + 5*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y + 5*self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, BLACK, (self.x - 2*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, BLACK, (self.x - 3*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 4*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, BLACK, (self.x + self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, BLACK, (self.x + 2*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + 3*self.size, self.y - self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y - 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y - 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 2*self.size, self.y - 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 3*self.size, self.y - 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 4*self.size, self.y - 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y - 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + 2*self.size, self.y - 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + 3*self.size, self.y - 2*self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y - 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y - 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 2*self.size, self.y - 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 3*self.size, self.y - 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y - 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + 2*self.size, self.y - 3*self.size, self.size, self.thickness))

        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y - 4*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y - 4*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 2*self.size, self.y - 4*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y - 4*self.size, self.size, self.thickness))


    def update(self):
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        if self.y > HEIGHT * 0.2:
            self.speed = 0.25
            if self.secondary_movement_mode:
                self.secondary_movement_mode = False
                if self.x > WIDTH * 0.5:
                    self.angle = math.pi * 1.5
                else:
                    self.angle = math.pi * 0.5 
            else:
                if self.x > WIDTH * 0.8:
                    self.angle = math.pi * 1.5
                elif self.x < WIDTH * 0.2:
                    self.angle = math.pi * 0.5 
        
    def dead(self):
        if self.health < 0:
            return True

    def hit(self, projectile):
        dx = (self.x + (self.size / 2)) - projectile.x 
        dy = (self.y + (self.size / 2)) - projectile.y

        proximity = math.hypot(dx, dy)       
        if proximity < self.size + projectile.size:
            self.health -= projectile.power
            return True
  

class RedGuy(Enemy):
    def __init__(self, x, y):

        self.size = 3
        self.x = x
        self.y = y + 2*self.size
        self.colour = 255, 0, 150
        self.speed = 2
        self.angle = math.pi/2
        self.health = 5
        self.score = 100
        self.thickness = 0

    def display(self):
        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 2*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + 2*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 2*self.size, self.y - 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + 2*self.size, self.y - 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 2*self.size, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + 2*self.size, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 3*self.size, self.y + 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + 3*self.size, self.y + 3*self.size, self.size, self.thickness))

    def dead(self):
        if self.health < 0:
            return True

    def bounce(self):
        if self.x + 4*self.size > WIDTH:
            self.y += 6*self.size
            self.angle = math.pi*1.5
            
        elif self.x < 0:
            self.angle = math.pi/2
            self.y += 6*self.size
            
    def update(self):
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed

    def hit(self, projectile):
        dx = (self.x + (self.size / 2)) - projectile.x 
        dy = (self.y + (self.size / 2)) - projectile.y

        proximity = math.hypot(dx, dy)       
        if proximity < 4 * self.size + projectile.size:
            self.health -= projectile.power
            return True

class GoldGuy(Enemy):
    def __init__(self, x, y):

        self.size = 3
        self.x = random.randint(0,WIDTH - self.size)
        self.y = y + 2*self.size
        self.colour = 255, 255, 150
        self.speed = 1
        self.score = 200
        self.thickness = 0
        a = random.randint(0, 1)
        if a == 0:
            self.angle = 3*(math.pi)/4
        else:
            self.angle = 5*(math.pi)/4
        self.health = 3

    def display(self):
        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 2*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + 2*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 2*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + 2*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y - 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y - 2*self.size, self.size, self.thickness))
        
    def dead(self):
        if self.health < 0:
            return True

    def bounce(self):
        if self.x + 2*self.size > WIDTH:
            self.x += -4*self.size
            self.angle = -self.angle
        
        elif self.x < 0:
            self.x += 4*self.size
            self.angle = -self.angle

    def update(self):
        x = self.x
        y = (self.x - x)**2
        z = math.sqrt(y)
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        if  z > 400:
            self.angle = -self.angle
                                
    def hit(self, projectile):
        dx = (self.x + (self.size / 2)) - projectile.x 
        dy = (self.y + (self.size / 2)) - projectile.y

        proximity = math.hypot(dx, dy)       
        if proximity < 4 * self.size + projectile.size:
            self.health -= projectile.power
            return True

class BlueGuy(Enemy):
    def __init__(self, x, y):

        self.size = 3
        self.thickness = 0
        self.x = random.randint( 0, WIDTH - self.size)
        self.y = y + 2 * self.size
        self.colour = 150, 150, 255
        self.speed = 1.5
        self.angle = math.pi
        self.health = 0
        self.score = 200

    def display(self):
        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 2*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + 2*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 2*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + 2*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y - 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y - 2*self.size, self.size, self.thickness))

    def bounce(self):
        if self.x + 2 * self.size > WIDTH:
            self.x += - 4 * self.size
        
        elif self.x < 0:
            self.x += 4*self.size

    def update(self):
        self.y += self.speed

    def hit(self, projectile):
        dx = (self.x + (self.size/2)) - projectile.x 
        dy = (self.y + (self.size/2)) - projectile.y
        proximity = math.hypot(dx, dy)       
        if proximity < 4*self.size + projectile.size:
            self.health -= projectile.power
            return True

class Heart():

    def __init__(self):    
        self.size = 3
        self.colour = 255, 150, 150
        self.thickness = 0
    
    def display(self, position):
        self.x = 25 + position*30
        self.y = HEIGHT - 17
            
        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x , self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 2*self.size, self.y- 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + 2*self.size, self.y - 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 2*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + 2*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 2*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + 2*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 3*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + 3*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 4*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + 4*self.size, self.y, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 3*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + 3*self.size, self.y - self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 2*self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + 2*self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 3*self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + 3*self.size, self.y + self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + 2*self.size, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - 2*self.size, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y + 2*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x + self.size, self.y + 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x - self.size, self.y + 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y + 3*self.size, self.size, self.thickness))
        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y + 4*self.size, self.size, self.thickness))

########################################################################################################################
########################################################################################################################
'                                             **** TEXT/MENU CLASSES ****                                               '
########################################################################################################################
########################################################################################################################
    
class MenuItem():
    def __init__(self, text, font, font_size, font_colour, pos_x=0, pos_y=0):
    
        self.text = text
        self.font_size = font_size
        self.font = font
        self.font_colour = font_colour
        self.label = self.font.render(self.text, 1, self.font_colour)
        self.width = self.label.get_rect().width
        self.height = self.label.get_rect().height
        self.dimensions = (self.width, self.height)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.position = pos_x, pos_y
 
    def is_mouse_selection(self, posx, posy):
        if (posx >= self.pos_x and posx <= self.pos_x + self.width) and \
            (posy >= self.pos_y and posy <= self.pos_y + self.height):
                return True
        return False

    def set_position(self, x, y):
        self.position = (x, y)
        self.pos_x = x
        self.pos_y = y
 
    def set_font_colour(self, rgb_tuple):
        self.font_colour = rgb_tuple
        self.label = self.font.render(self.text, 1, self.font_colour)
 
class GameMenu():
    def __init__(self, items, funcs, x, y):

        self.screen_width = SCREEN.get_rect().width
        self.screen_height = SCREEN.get_rect().height
        self.font = BODY_FONT
        self.italic_font = BODY_ITALIC_FONT
        font_size = 30
        font_colour = WHITE
        self.background_colour = BLACK
        self.clock = pygame.time.Clock()
        self.funcs = funcs
        self.items = []
        for index, item in enumerate(items):
            menu_item = MenuItem(item, self.font, font_size, font_colour)
 
            # t_h: totalHEIGHT of text block
            t_h = len(items) * menu_item.height
            pos_x = (self.screen_width / x) - (menu_item.width / 2)
            # This line includes a bug fix by Ariel (Thanks!)
            # Please check the comments section of pt. 2 for an explanation
            a = self.screen_height / y
            b = t_h / 2
            c = index*2
            d = index * menu_item.height
            pos_y = (a + c + d) - b
 
            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)
 
        self.mouse_is_visible = True
        self.cur_item = None
 
    def set_mouse_visibility(self):
        if self.mouse_is_visible:
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)
 
    def set_keyboard_selection(self, key):
        """
        Marks the MenuItem chosen via up and down keys.
        """
        for item in self.items:
            # Return all to neutral
            item.font = self.font
            item.set_font_colour(WHITE)
 
        if self.cur_item is None:
            self.cur_item = 0
        else:
            # Find the chosen item
            if key == pygame.K_UP and \
                    self.cur_item > 0:
                self.cur_item -= 1
            elif key == pygame.K_UP and \
                    self.cur_item == 0:
                self.cur_item = len(self.items) - 1
            elif key == pygame.K_DOWN and \
                    self.cur_item < len(self.items) - 1:
                self.cur_item += 1
            elif key == pygame.K_DOWN and \
                    self.cur_item == len(self.items) - 1:
                self.cur_item = 0
 
        self.items[self.cur_item].font = self.italic_font
        self.items[self.cur_item].set_font_colour(RED)
        MENU_SCROLL_SOUND.play(0)
 
        # Finally check if Enter or Space is pressed
        if key == pygame.K_SPACE or key == pygame.K_RETURN:
            text = self.items[self.cur_item].text
            MENU_SELECT_SOUND.play(0)
            self.funcs[text]()
 
    def set_mouse_selection(self, item, mpos1, mpos2):
        """Marks the MenuItem the mouse cursor hovers on."""
        if item.is_mouse_selection(mpos1, mpos2):
            if item.font_colour == WHITE: MENU_SCROLL_SOUND.play(0)
            item.set_font_colour(RED)
            item.font = self.italic_font
        else:
            item.set_font_colour(WHITE)
            item.font = self.font

class HighScoresTable():
    def __init__(self, items, average_item_width, y):

        self.screen_width = SCREEN.get_rect().width
        self.screen_height = SCREEN.get_rect().height
        self.font = TABLE_FONT
        self.italic_font = TABLE_ITALIC_FONT
        self.background_colour = BLACK
        font_size = 20
        font_colour = WHITE
        
        self.items = []
        for index, item in enumerate(items):
            menu_item = MenuItem(item, self.font, font_size, font_colour)
 
            # t_h: totalHEIGHT of text block
            t_h = len(items) * menu_item.height
            pos_x = (self.screen_width / 2) -  (average_item_width /2)
            a = self.screen_height / y
            b = t_h / 2
            c = index*2
            d = index * menu_item.height
            pos_y = (a + c + d) - b
 
            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)
 
        self.mouse_is_visible = True
        self.cur_item = None
 
    def set_mouse_visibility(self):
        if self.mouse_is_visible:
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)
        
    def set_mouse_selection(self, item, mpos1, mpos2):
        """Marks the MenuItem the mouse cursor hovers on."""
        if item.is_mouse_selection(mpos1, mpos2):
            item.set_font_colour(RED)
            item.font = self.italic_font
        else:
            item.set_font_colour(WHITE)
            item.font = self.font

class PickupNotification():

    def __init__(self, game_play_scene, pickup):
        self.x, self.y = pickup.x, pickup.y
        self.init_time = game_play_scene.time
        if pickup.type == 1:
            self.text = HUD_FONT.render(game_play_scene.collectable_weapons[pickup.weapon_type].text, 1, WHITE)
            self.sound = os.path.normpath('sound/Weapon Collected Sound.ogg')
        elif pickup.type == 2:
            self.text = HUD_FONT.render(game_play_scene.weapon_inventory[pickup.weapon_type].text + ' + ' + str(pickup.contents), 1, WHITE)
            self.sound = os.path.normpath('sound/Ammo Collected Sound.ogg')
        elif pickup.type == 3:
            self.text = HUD_FONT.render('1 UP', 1, WHITE)
            self.sound = os.path.normpath('sound/1 UP Sound.ogg')
        self.text_width = self.text.get_size()[0]
    def delete(self, game_play_scene):
        if game_play_scene.time > self.init_time + 3000:
            game_play_scene.notifications.remove(self)
    
    def display(self):
        SCREEN.blit(self.text, (self.x - self.text_width *0.5, self.y - 20))

    def play_sound(self):
        sound = pygame.mixer.Sound(self.sound)
        sound.play(0)


########################################################################################################################
########################################################################################################################
'                                             **** SCENE CLASSES ****                                                  '
########################################################################################################################
########################################################################################################################

class Scene:
 
    def __init__(self, director):
        self.director = director

    def on_update(self):

        raise NotImplementedError("on_update abstract method must be defined in subclass.")

    def on_event(self, event):

        raise NotImplementedError("on_event abstract method must be defined in subclass.")

    def on_draw(self, SCREEN):

        raise NotImplementedError("on_draw abstract method must be defined in subclass.")

class SplashScene(Scene):
    def __init__(self, director):
        Scene.__init__(self, director)
        self.particles = []
        self.title = TITLE_FONT.render("Master Blaster", 1, WHITE)
        self.title_width, self.title_height = self.title.get_size()
        self.music_flag  = True
        
    def on_event(self, none1, none2, none3):
        pass
    
    def on_update(self):
        if self.music_flag:
            pygame.mixer.music.load(os.path.normpath("sound/splash.wav"))
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(0)
        if pygame.time.get_ticks() > 7000:
            dir.scene = main_menu_scene
        particle = Particle(WIDTH / 2, HEIGHT / 2, explosion_colours(), random.randint(1, 5), random.randint(1, 10))
        self.particles.append(particle)
        for particle in self.particles:
            if particle.delete():
                self.particles.remove(particle)
            particle.update()
        self.music_flag  = False

    def on_draw(self, none1, none2):
        SCREEN.fill(BLACK)
        for particle in self.particles:
            particle.display()
        SCREEN.blit(self.title, (round(WIDTH *0.5 - self.title_width *0.5), round(HEIGHT *0.5 - self.title_height *0.5)))

class MainMenuScene(Scene):
 
    def __init__(self, director):
        Scene.__init__(self, director)

        def play():
            intro_cut_scene.__init__(dir, self)
            dir.scene = intro_cut_scene 
        def high_scores():
            high_scores_scene.__init__(dir)
            high_scores_scene.previous_scene = self
            dir.scene = high_scores_scene
        def about():
            about_scene.previous_scene = self
            dir.scene = about_scene
        def quit_menu():
            quit_menu_scene.previous_scene = self
            quit_menu_scene.destination = None
            dir.scene = quit_menu_scene
        def settings():
            settings_menu_scene.previous_scene = self
            dir.scene = settings_menu_scene
                   
        self.functions = {'Play': play, 'Settings': settings, 'High Scores' : high_scores,
             'About' : about, 'Quit' : quit_menu } 
        self.menu = GameMenu( self.functions.keys(), self.functions, 2, 2)
        self.music_flag = True

        #lists
        self.particles = []
        self.stars = []

        self.defender = Defender(WIDTH / 2, HEIGHT - 50)
        self.movement_x = [False, False]
        self.movement_y = [False, False]
        self.music_flag = True
        
    def on_update(self):
        if self.music_flag:
            pygame.mixer.music.load(os.path.normpath("sound/Title Music.ogg"))
            pygame.mixer.music.set_volume(0.7)
            pygame.mixer.music.play(-1)
            self.music_flag = False

        afterburner = AfterBurner(self.defender, self.movement_x, self.movement_y) 
        self.particles.append(afterburner)
        stars_ = random.randint(0, 13)
        if stars_ == 7:
            star = Star()
            self.stars.append(star)
        booster = Booster(self.defender, self.movement_x, self.movement_y)
        self.particles.append(booster)
        for particle in self.particles:
            if particle.delete():
                self.particles.remove(particle)
            particle.update()
        for star in self.stars:
            if star.delete():
                self.stars.remove(star)
            star.update()

 
    def on_event(self, event, mpos1, mpos2):       
        if event.type == pygame.KEYDOWN:
            self.menu.mouse_is_visible = False
            self.menu.set_keyboard_selection(event.key)
        if event.type == pygame.MOUSEBUTTONDOWN:
            for item in self.menu.items:
                if item.is_mouse_selection(mpos1, mpos2):
                    MENU_SELECT_SOUND.play(0)
                    self.functions[item.text]()

    def on_draw(self, mpos1, mpos2):
        if pygame.mouse.get_rel() != (0, 0):
            self.menu.mouse_is_visible = True
            self.menu.cur_item = None
        self.menu.set_mouse_visibility()
    
        SCREEN.fill(BLACK)

        for particle in self.particles:
            particle.display()   
        for star in self.stars:
            star.display()
        self.defender.display()

        for item in self.menu.items:
            if self.menu.mouse_is_visible:
                self.menu.set_mouse_selection(item, mpos1, mpos2)
            SCREEN.blit(item.label, item.position)

class SettingsMenuScene(Scene):
    def __init__(self, director):
        Scene.__init__(self, director)

        def controls():
            controls_menu_scene.previous_scene = self.previous_scene
            dir.scene = controls_menu_scene
        def sound():
            pass
        def back():
            dir.scene = self.previous_scene
        
        self.functions = {'Controls': controls, 'Sound': sound, 'Back' : back} 
        self.menu = GameMenu( self.functions.keys(), self.functions, 2, 2)
        self.previous_scene = None
        self.menu_scroll_flag = False
        
    def on_update(self):
        if self.previous_scene == main_menu_scene:
            main_menu_background_update()
 
    def on_event(self, event, mpos1, mpos2):       
        if event.type == pygame.KEYDOWN:
            self.menu.mouse_is_visible = False
            self.menu.set_keyboard_selection(event.key)
        if event.type == pygame.MOUSEBUTTONDOWN:
            for item in self.menu.items:
                if item.is_mouse_selection(mpos1, mpos2):
                    MENU_SELECT_SOUND.play(0)
                    self.functions[item.text]()

    def on_draw(self, mpos1, mpos2):
        if pygame.mouse.get_rel() != (0, 0):
            self.menu.mouse_is_visible = True
            self.menu.cur_item = None
        self.menu.set_mouse_visibility()

        SCREEN.fill(BLACK)

        if self.previous_scene == game_paused_scene:
            display_game()
        if self.previous_scene == main_menu_scene:
            main_menu_background_draw()

        for item in self.menu.items:
            if self.menu.mouse_is_visible:
                self.menu.set_mouse_selection(item, mpos1, mpos2)
            SCREEN.blit(item.label,  item.position)

class ControlsMenuScene(Scene):

    def __init__(self, director):
        Scene.__init__(self, director)

        def back():
            dir.scene = self.previous_scene

        def alter_key():
            pass

        #Game controls
        self.up = pygame.K_UP
        self.down = pygame.K_DOWN
        self.left = pygame.K_LEFT
        self.right = pygame.K_RIGHT

        self.fire = pygame.K_SPACE
            
        self.message = HEADER_FONT.render('Select an action to alter the control', 1, WHITE)
        self.message_width = self.message.get_rect().width
        self.previous_scene = None
        
        self.functions = {'up = ' + pygame.key.name(self.up) : alter_key,
                            'down = ' + pygame.key.name(self.down) : alter_key,
                         'left = ' + pygame.key.name(self.left) : alter_key, 
                        'right = ' + pygame.key.name(self.right) : alter_key,
                        'fire weapon = ' + pygame.key.name(self.fire) : alter_key, 'back' : back} 
        self.menu = GameMenu( self.functions.keys(), self.functions, 2, 2)

    def on_update(self):
        if self.previous_scene == main_menu_scene:
            main_menu_background_update()
 
    def on_event(self, event, mpos1, mpos2):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                back()
            self.menu.mouse_is_visible = False
            self.menu.set_keyboard_selection(event.key)

        if event.type == pygame.MOUSEBUTTONDOWN:
            for item in self.menu.items:
                if item.is_mouse_selection(mpos1, mpos2):
                    MENU_SELECT_SOUND.play(0)
                    self.functions[item.text]()

    def on_draw(self, mpos1, mpos2):

        if pygame.mouse.get_rel() != (0, 0):
            self.menu.mouse_is_visible = True
            self.menu.cur_item = None
        self.menu.set_mouse_visibility()

        SCREEN.fill(BLACK)

        if self.previous_scene == game_paused_scene:
            display_game()
        if self.previous_scene == main_menu_scene:
            main_menu_background_draw()

        for item in self.menu.items:
            if self.menu.mouse_is_visible:
                self.menu.set_mouse_selection(item, mpos1, mpos2)
            SCREEN.blit(item.label, item.position)
        SCREEN.blit(self.message, (round(((WIDTH / 2 ) - (self.message_width / 2))), round(HEIGHT / 4)))

class ControlsEntryScene(Scene):

    def __init__(self, director):
        Scene.__init__(self, director)

        def back():
            dir.scene = self.previous_scene

        def alter_key():
            pass

        self.previous_scene = None
        self.selected_key = None
        self.message = TITLE_FONT.render('Press a key for ', 1, WHITE)
        self.message_width = self.message.get_rect().width

        self.functions = {'back' : back} 
        self.menu = GameMenu( self.functions.keys(), self.functions, 2, 2)

    def on_update(self):
        if self.previous_scene == main_menu_scene:
            main_menu_background_update()
 
    def on_event(self, event, mpos1, mpos2):

        if event.type == pygame.KEYDOWN:
            self.menu.mouse_is_visible = False
            self.menu.set_keyboard_selection(event.key)

        if event.type == pygame.MOUSEBUTTONDOWN:
            for item in self.menu.items:
                if item.is_mouse_selection(mpos1, mpos2):
                    self.functions[item.text]()

    def on_draw(self, mpos1, mpos2):

        if pygame.mouse.get_rel() != (0, 0):
            self.menu.mouse_is_visible = True
            self.menu.cur_item = None
        self.menu.set_mouse_visibility()

        SCREEN.fill(BLACK)

        if self.previous_scene == game_paused_scene:
            display_game()
        if self.previous_scene == main_menu_scene:
            main_menu_background_draw()

        for item in self.menu.items:
            if self.menu.mouse_is_visible:
                self.menu.set_mouse_selection(item, mpos1, mpos2)
            SCREEN.blit(item.label, item.position)
        SCREEN.blit(self.message, (round(((WIDTH / 2 ) - (self.message_width / 2)), round(HEIGHT / 3.5))))
    
class QuitMenuScene(Scene):
 
    def __init__(self, director):
        Scene.__init__(self, director)
        
        def back():
            dir.scene = self.previous_scene
        def quit():
            if self.destination == main_menu_scene: 
                main_menu_scene.__init__(dir)
                dir.scene = main_menu_scene
            else:
                quit_flag()
        self.quit_message = HEADER_FONT.render('Are you sure you want to quit?', 1, WHITE)
        self.menu_message = HEADER_FONT.render('Exit to main menu?', 1, WHITE)
        self.previous_scene = None
        self.destination = None
        self.functions = {'Yes': quit, 'No' : back} 
        self.menu = GameMenu( self.functions.keys(), self.functions, 2, 2)

    def on_update(self):
        if self.previous_scene == main_menu_scene:
            main_menu_background_update()
 
    def on_event(self, event, mpos1, mpos2):

        if event.type == pygame.KEYDOWN:
            self.menu.mouse_is_visible = False
            self.menu.set_keyboard_selection(event.key)
            if event.key == pygame.K_ESCAPE:
                MENU_SELECT_SOUND.play(0)
                dir.scene = self.previous_scene

        if event.type == pygame.MOUSEBUTTONDOWN:
            for item in self.menu.items:
                if item.is_mouse_selection(mpos1, mpos2):
                    MENU_SELECT_SOUND.play(0)
                    self.functions[item.text]()

    def on_draw(self, mpos1, mpos2):
        if pygame.mouse.get_rel() != (0, 0):
            self.menu.mouse_is_visible = True
            self.menu.cur_item = None
        self.menu.set_mouse_visibility()

        SCREEN.fill(BLACK)

        if self.previous_scene == game_paused_scene:
            display_game()
        if self.previous_scene == main_menu_scene:
            main_menu_background_draw()

        for item in self.menu.items:
            if self.menu.mouse_is_visible:
                self.menu.set_mouse_selection(item, mpos1, mpos2)
            SCREEN.blit(item.label, item.position)
        if self.destination == main_menu_scene:
            message = self.menu_message
        else:
            message = self.quit_message
        message_width = message.get_rect().width
        SCREEN.blit(message, (round(((WIDTH / 2 ) - (message_width / 2))), round(HEIGHT / 4)))

class HighScoresScene(Scene):
    def __init__(self, director):
        Scene.__init__(self, director)

        def back():
            dir.scene = self.previous_scene
        
        space_render = TABLE_FONT.render(' ', 1, WHITE)
        space_width = space_render.get_rect().width

        self.previous_scene = None
        self.high_scores = []
        self.item_widths = 0
        
        for item in read_high_scores():
            #renders name and score 
            name_render = TABLE_FONT.render(item[0], 1, WHITE)
            score_render = TABLE_FONT.render(str(item[1]), 1, WHITE)
            #calculatesWIDTH of the rendered name and score 
            name_width = name_render.get_rect().width
            score_width = score_render.get_rect().width
            #calculates the amount of remaining available space in each column
            additional_space1 = int(((space_width * 30) - name_width) / space_width)
            additional_space2 = int(((space_width * 20) - score_width) / space_width)
            #makes the tuple into a single string with extra space filled
            item = item[0] + ' '*additional_space1 + str(item[1]) + ' '*additional_space2 + item[2]
            item_render = TABLE_FONT.render(item, 1, WHITE)
            item_width = item_render.get_rect().width
            self.item_widths += item_width
            self.high_scores.append(item)
        
        average_item_width = (int(self.item_widths/len(self.high_scores)))
        self.functions = {'Back': back} 

        self.menu = GameMenu( self.functions.keys(), self.functions, 6, 1.1)
        self.scores_table = HighScoresTable( self.high_scores, average_item_width, 2)

    def on_update(self):
        if self.previous_scene == main_menu_scene:
            main_menu_background_update()

    def on_event(self, event, mpos1, mpos2):
        if event.type == pygame.KEYDOWN:
            self.menu.mouse_is_visible = False
            self.menu.set_keyboard_selection(event.key)
            if event.key == pygame.K_ESCAPE:
                MENU_SELECT_SOUND.play(0)
                dir.scene = self.previous_scene

        if event.type == pygame.MOUSEBUTTONDOWN:
            for item in self.menu.items:
                if item.is_mouse_selection(mpos1, mpos2):
                    MENU_SELECT_SOUND.play(0)
                    self.functions[item.text]()

    def on_draw(self, mpos1, mpos2):

        if pygame.mouse.get_rel() != (0, 0):
            self.menu.mouse_is_visible = True
            self.scores_table.mouse_is_visible = True
            self.menu.cur_item = None
            self.scores_table.cur_item = None
        self.menu.set_mouse_visibility()
        self.scores_table.set_mouse_visibility()

        SCREEN.fill(BLACK)

        for item in self.scores_table.items:
            if self.scores_table.mouse_is_visible:
                self.scores_table.set_mouse_selection(item, mpos1, mpos2)
            SCREEN.blit(item.label, item.position)

        for item in self.menu.items:
            if self.menu.mouse_is_visible:
                self.menu.set_mouse_selection(item, mpos1, mpos2)
            SCREEN.blit(item.label, item.position)

        if self.previous_scene == game_paused_scene:
            display_game()
        if self.previous_scene == main_menu_scene:
            main_menu_background_draw()

class AboutScene(Scene):
    def __init__(self, director):
        Scene.__init__(self, director)

        def back():
            dir.scene = self.previous_scene
        
        self.message = '''This is a game that I decided to make in my sparetime to develope 
                          my python skills. It has been written in python 3.6 and makes use 
                          of the following modules: pygame, operator, random, math, pickle 
                          and datetime. I have used a variety of sound effects from 
                          https://freesound.org and some fonts from various font sites 
                          The graphics have been implemented completely by using pygame's 
                          drawing functions which has involved a bit of math here and 
                          there. The music has been composed by myself as well as a few of 
                          the sound effects. I hope you enjoy. My email address is: 
                          eM7RON@live.com'''
        
        self.previous_scene = None
        self.functions = {'Back': back} 
        self.menu = GameMenu( self.functions.keys(), self.functions, 6, 1.1)

    def on_update(self):
        if self.previous_scene == main_menu_scene:
            main_menu_background_update()

    def on_event(self, event, mpos1, mpos2):
        if event.type == pygame.KEYDOWN:
            self.menu.mouse_is_visible = False
            self.menu.set_keyboard_selection(event.key)
            if event.key == pygame.K_ESCAPE:
                MENU_SELECT_SOUND.play(0)
                dir.scene = self.previous_scene

        if event.type == pygame.MOUSEBUTTONDOWN:
            for item in self.menu.items:
                if item.is_mouse_selection(mpos1, mpos2):
                    MENU_SELECT_SOUND.play(0)
                    self.functions[item.text]()

    def on_draw(self, mpos1, mpos2):

        if pygame.mouse.get_rel() != (0, 0):
            self.menu.mouse_is_visible = True
            self.menu.cur_item = None
        self.menu.set_mouse_visibility()

        SCREEN.fill(BLACK)


        for item in self.menu.items:
            if self.menu.mouse_is_visible:
                self.menu.set_mouse_selection(item, mpos1, mpos2)
            SCREEN.blit(item.label, item.position)

        if self.previous_scene == game_paused_scene:
            display_game()
        if self.previous_scene == main_menu_scene:
            main_menu_background_draw()
        
        blit_text(SCREEN, self.message, (WIDTH *0.2, HEIGHT *0.2), WIDTH *0.8, NEW_BODY_FONT, WHITE)


class GameOverScene(Scene):
    def __init__(self, director):
        Scene.__init__(self, director)
        
        self.game_over_text = TITLE_FONT.render("Game Over", 1, WHITE)
        self.text_width, self.text_height = self.game_over_text.get_size()
        self.music_flag = True
        self.screen_flag = True
        self.ticks = 0
        self.high_scores = read_high_scores()

    def on_event(self, none1, none2, none3):
        pass
    
    def on_update(self):
        if self.music_flag:
            pygame.mixer.music.load(os.path.normpath("sound/game over.wav"))
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(0)
            self.music_flag = False
        if self.screen_flag:
            self.ticks = pygame.time.get_ticks()
            self.screen_flag = False
        time = pygame.time.get_ticks()
        if time > self.ticks + 7000:
            for item in self.high_scores:  
                if item[1] < game_play_scene.score: 
                    high_score_entry_scene.__init__(dir)
                    dir.scene = high_score_entry_scene
            main_menu_scene.__init__(dir)
            dir.scene = main_menu_scene
            
            
    def on_draw(self, none1, none2):
        SCREEN.fill(BLACK)
        SCREEN.blit(self.game_over_text, (round(WIDTH *0.5 - self.text_width *0.5), round(HEIGHT *0.5 - self.text_height *0.5)))


class HighScoreEntryScene(Scene):
    def __init__(self, director):
        Scene.__init__(self, director)
        self.high_score_text = HEADER_FONT.render('Congratulations you achieved a high score!', 1, WHITE)
        self.text_width, self.text_height = self.high_score_text.get_size()
        self.que_text = HEADER_FONT.render('Enter Name:', 1, WHITE)
        self.que_width, self.que_height = self.que_text.get_size()
        self.name = ""
        self.screen_flag = [False, False]
        self.ticks = 0

    def on_event(self, event, none1, none2):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.name = self.name[:-1]
            elif (event.key == pygame.K_RETURN) and (len(self.name) > 0):
                self.screen_flag = [True, True]
                write_high_scores(self.name, game_play_scene.score, game_over_scene.high_scores)
                main_menu_scene.__init__(dir)
                dir.scene = main_menu_scene    
            elif len(self.name) > 11:
                None
            else:
                self.name += event.unicode
        
    def on_update(self):
        if self.screen_flag[0]:
            self.ticks = pygame.time.get_ticks()
            self.screen_flag[0] = False
        if self.screen_flag[1] and pygame.time.get_ticks() > self.ticks + 7000:
            dir.scene = main_menu_scene

    def on_draw(self, none1, none2):
        SCREEN.fill(BLACK)
        SCREEN.blit(self.high_score_text, (round(WIDTH *0.5 - self.text_width *0.5), round(HEIGHT *0.3 - self.text_height *0.5)))
        name = HEADER_FONT.render(self.name, 10, WHITE)
        name_width, name_height = name.get_size()
        SCREEN.blit(name, (round(WIDTH *0.5 - name_width *0.5), round(HEIGHT *0.5 - name_height *0.5)))
        SCREEN.blit(self.que_text, (round(WIDTH * 0.05), round(HEIGHT *0.5 - self.que_height *0.5)))


class IntroCutScene(Scene):

    def __init__(self, director, main_menu_scene):
        Scene.__init__(self, director)
        #lists
        self.particles = []
        self.stars = []

        for particle in main_menu_scene.particles:
            self.particles.append(particle)

        self.starts = main_menu_scene.stars
   
        self.defender = Defender(WIDTH *0.5, HEIGHT - 50)
        self.initial_time = pygame.time.get_ticks()
        self.movement_x = [False, False]
        self.movement_y = [False, False]
        self.draw_orientation = [False, False, False, False]
        self.music_flag = True

        # movement flags
        self.movement_flag_1 = True
        self.movement_flag_2 = True
        self.movement_flag_3 = True
        self.movement_flag_4 = True
        self.movement_flag_5 = True
        self.movement_flag_6 = True
        self.movement_flag_7 = True
        self.movement_flag_8 = True
        self.movement_flag_9 = True
        self.movement_flag_10 = True
        self.movement_flag_11 = True
        self.movement_flag_12 = True

    def on_event(self, event, mpos1, mpos2):
        pass
        
    def on_update(self):

        time = pygame.time.get_ticks()
    
        if self.music_flag:
            pygame.mixer.music.load(os.path.normpath("sound/trojan v 1.0.ogg"))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(-1)
            self.music_flag = False      
        if (time > self.initial_time + 500) and (self.movement_flag_1 == True):
            enemy_detected_sound = pygame.mixer.Sound(os.path.normpath('sound/Enemy Detected Sound.ogg'))
            enemy_detected_sound.set_volume(0.5)
            enemy_detected_sound.play(0)
            self.movement_y[0] = True
            self.movement_flag_1 = False
        if (time > self.initial_time + 600) and (self.movement_flag_2 == True):
            self.movement_x[1] = True
            self.movement_flag_2 = False
        if (time > self.initial_time + 1500) and (self.movement_flag_3 == True):
            self.movement_x = [True, False]
            self.movement_flag_3 = False
        if (time > self.initial_time + 2600) and (self.movement_flag_4 == True):
            self.movement_x = [False, True]
            self.movement_flag_4 = False
        if (time > self.initial_time + 2600) and (self.defender.x > WIDTH *0.5) and (self.movement_flag_5 == True):
            self.defender.x = WIDTH *0.5
            self.movement_x = [False, False]
            self.movement_y = [False, False]
            self.movement_flag_5 = False
        if (time > self.initial_time + 2600) and (self.defender.x == WIDTH *0.5) and (self.movement_flag_6 == True):
            self.defender.y += 1
        if (time > self.initial_time + 2600) and (self.defender.y > HEIGHT *0.5) and (self.movement_flag_7 == True):
            engine_sound = pygame.mixer.Sound(os.path.normpath('sound/Light Speed Engine Sound.ogg'))
            engine_sound.set_volume(0.5)
            engine_sound.play(0)
            self.movement_flag_6 = False
            self.defender.y = HEIGHT *0.5

        if (time > self.initial_time + 9000) and (self.defender.y == HEIGHT *0.5) and (self.movement_flag_8 == True):
            self.movement_flag_7 = False
            for star in self.stars:
                star.thickness += 20
                star.speed = 0
        if (time > self.initial_time + 11000) and (self.defender.y == HEIGHT *0.5) and (self.movement_flag_9 == True):
            self.movement_flag_8 = False
            for star in self.stars:
                star.speed = random.uniform(23, 43)
                star.thickness += 20
        if (time > self.initial_time + 14000) and (self.defender.y == HEIGHT *0.5) and (self.movement_flag_10 == True):
            self.movement_flag_9 = False
            for star in self.stars:
                star.thickness = 4
                star.speed = random.uniform(2, 20)
        if (time > self.initial_time + 15000) and (self.movement_flag_11 == True):
            self.defender.y += 2
            self.movement_flag_10 = False
        if (time > self.initial_time + 15000) and (self.defender.y == HEIGHT - 50) and (self.movement_flag_12 == True):
            self.movement_flag_11 = False
        
        if self.movement_x[0]: 
            self.defender.x += -4.333
            self.draw_orientation[0] = True
        else:
            self.draw_orientation[0] = False
        if self.movement_x[1]: 
            self.defender.x += +4.333
            self.draw_orientation[1] = True
        else:
            self.draw_orientation[1] = False
        if self.movement_y[0]:
            self.defender.y += -2.333
            self.draw_orientation[2] = True
        else:
            self.draw_orientation[2] = False
        if self.movement_y[1]:
            self.defender.y += +2.333
            self.draw_orientation[3] = True
        else:
            self.draw_orientation[3] = False
        if not self.movement_x[0] and not self.movement_x[1]: 
            self.defender.x += 0
            if self.draw_orientation[2]:
                afterburner = AfterBurner(self.defender, self.movement_x, self.movement_y) 
                self.particles.append(afterburner)
        if not self.movement_y[0] and not self.movement_y[1]: 
            self.defender.y += 0
        stars_ = random.randint(0, 13)
        if stars_ == 7:
            star = Star()
            self.stars.append(star)
        booster = Booster(self.defender, self.movement_x, self.movement_y)
        self.particles.append(booster)
        
        self.defender.bounce()
        for particle in self.particles:
            if particle.delete():
                self.particles.remove(particle)
            particle.update()
        for star in self.stars:
            if star.delete():
                self.stars.remove(star)
            star.update()

        if  time > self.initial_time + 16000:
            game_play_scene.__init__(dir, self)
            dir.scene = game_play_scene

        if (time > (self.initial_time + 5000)) and (time < (self.initial_time + 8500)):
            electrical_discharge = Lightning(self.defender.x + random.uniform(-50, 50), 
                                  self.defender.y + random.uniform(-50, 50),
                                  self.defender.x + random.uniform(-HEIGHT *0.3, HEIGHT *0.3), 
                                  self.defender.y + random.uniform(-HEIGHT *0.3, HEIGHT *0.3),
                                  lightning_blue_stem_colours(),
                                  lightning_blue_fork_colours(),
                                  random.uniform(math.pi, math.pi * 2))
            self.particles.append(electrical_discharge)
            
    def on_draw(self, mpos1, mpos2):

        SCREEN.fill(BLACK)
        
        for particle in self.particles:
            particle.display()   
        for star in self.stars:
            star.display()
        
        if (self.draw_orientation[0] and self.draw_orientation[1]) or (self.draw_orientation[2] and self.draw_orientation[3]):
            self.defender.display()
        elif self.draw_orientation[0]: self.defender.display_right()
        elif self.draw_orientation[1]: self.defender.display_left()
        elif self.draw_orientation[2]: self.defender.display_forward()
        elif self.draw_orientation[3]: self.defender.display_back()
        else: self.defender.display()
             

class GamePlayScene(Scene):
    def __init__(self, director, intro_cut_scene):
        Scene.__init__(self, director)           

        #lists
        self.enemies = []  
        self.projectiles = []
        self.particles = []
        self.stars = []
        self.pickups = []
        self.hearts = []
        self.pickups = []
        self.explosion_sounds = []
        self.notifications = []

        for particle in intro_cut_scene.particles:
            self.particles.append(particle)
        for star in intro_cut_scene.stars:
            self.stars.append(star)
        
        gun = Gun(self)
        rocket_launcher = RocketLauncher(self)
        bomb_launcher = BombLauncher(self)
        laser_gun = LaserGun(self)
        lightning_gun = LightningGun(self)
        self.collectable_weapons = [rocket_launcher, bomb_launcher, laser_gun, lightning_gun]
        self.weapon_inventory = [gun, lightning_gun]

        #sound effects
        for number in range(8):
            sound = pygame.mixer.Sound(os.path.normpath("sound/explosion" + str(number) + ".wav"))
            sound.set_volume(0.15)
            self.explosion_sounds.append(sound)
        
        self.weapon_toggle = 0
        self.current_weapon = self.weapon_inventory[self.weapon_toggle]
        
        self.defender = Defender(WIDTH *0.5, HEIGHT - 50)
        self.time = pygame.time.get_ticks()
        self.n = 0
        self.lives = 3
        self.weapon = 0
        self.score = 0
        self.movement_x = [False, False]
        self.movement_y = [False, False]
        self.draw_orientation = [False, False, False, False]
        self.primary_fire = False
        self.secondary_fire = False

        # rendered texts
        self.display_score = HUD_FONT.render(str(self.score), 1, WHITE)
        self.selected_weapon_text = HUD_FONT.render("Weapon:" + self.current_weapon.text, 1, WHITE)
        self.ammo_text = HUD_FONT.render("Ammo:" + str(self.current_weapon.ammo), 1, WHITE)

    def on_event(self, event, mpos1, mpos2):
        if event.type == pygame.KEYDOWN:
            if (event.key == (pygame.K_RSHIFT or pygame.K_SPACE)) and (self.current_weapon.ammo == 0):
                empty_weapon_sound = pygame.mixer.Sound(os.path.normpath("sound/Empty Weapon Sound 1.ogg"))
                empty_weapon_sound.play(0)
            if (event.key == pygame.K_RETURN) and (self.current_weapon.ammo > 0):
                if self.current_weapon.fire_mode == 'semi':
                    self.current_weapon.primary_fire()
                elif self.current_weapon.fire_mode == 'auto':
                    self.primary_fire = True
            if (event.key == pygame.K_SPACE) and (self.current_weapon.ammo > 0):
                if self.current_weapon.fire_mode == 'semi':
                    self.current_weapon.secondary_fire()
                elif self.current_weapon.fire_mode == 'auto':
                    self.secondary_fire = True
            if (event.key == pygame.K_RIGHT) and (self.weapon_toggle == len(self.weapon_inventory) - 1):
                self.weapon_toggle = 0
                self.current_weapon.primary_fire_sound.stop()
                self.current_weapon.secondary_fire_sound.stop()
            elif (event.key == pygame.K_RIGHT) and (self.weapon_toggle < len(self.weapon_inventory) - 1):
                self.current_weapon.primary_fire_sound.stop()
                self.current_weapon.secondary_fire_sound.stop()
                self.weapon_toggle += 1
            if (event.key == pygame.K_LEFT) and (self.weapon_toggle == 0):
                self.weapon_toggle = len(self.weapon_inventory) - 1
            elif (event.key == pygame.K_LEFT) and (self.weapon_toggle > 0):
                self.weapon_toggle -= 1
            if event.key == pygame.K_a:
                self.movement_x[0] = True
            if event.key == pygame.K_d:
                self.movement_x[1] = True
            if event.key == pygame.K_w:
                self.movement_y[0] = True   
            if event.key == pygame.K_s:
                self.movement_y[1] = True        
            if event.key == pygame.K_ESCAPE:
                pygame.mixer.music.pause()
                GAME_PAUSED_SOUND.play(0)
                self.movement_x, self.movement_y = [False, False], [False, False]
                dir.scene = game_paused_scene

        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_RETURN):
                self.primary_fire = False
                self.current_weapon.primary_fire_sound.stop()
            if (event.key == pygame.K_SPACE):
                self.secondary_fire = False
                self.current_weapon.secondary_fire_sound.stop()
            if event.key == pygame.K_a:
                self.movement_x[0] = False
            if event.key == pygame.K_d:
                self.movement_x[1] = False 
            if event.key == pygame.K_w:
                self.movement_y[0] = False
            if event.key == pygame.K_s:
                self.movement_y[1] = False
        
    def on_update(self):
        self.time = pygame.time.get_ticks()
        self.display_score = HUD_FONT.render(str(self.score), 1, WHITE)
        self.selected_weapon_text = HUD_FONT.render("Weapon:" + self.current_weapon.text, 1, WHITE)
        self.ammo_text = HUD_FONT.render("Ammo:" + str(self.current_weapon.ammo), 1, WHITE)
        self.current_weapon = self.weapon_inventory[self.weapon_toggle]

        if self.current_weapon.ammo < 0:
            self.current_weapon.ammo = 0
        
        if self.current_weapon.fire_mode == 'auto':
            if self.primary_fire:
                self.current_weapon.primary_fire()
            if self.secondary_fire:
                self.current_weapon.secondary_fire()
            
        if self.movement_x[0]: 
            self.defender.x += -4.333
            self.draw_orientation[0] = True
        else:
            self.draw_orientation[0] = False
        if self.movement_x[1]: 
            self.defender.x += +4.333
            self.draw_orientation[1] = True
        else:
            self.draw_orientation[1] = False
        if self.movement_y[0]:
            self.defender.y += -2.333
            self.draw_orientation[2] = True
        else:
            self.draw_orientation[2] = False
        if self.movement_y[1]:
            self.defender.y += +2.333
            self.draw_orientation[3] = True
        else:
            self.draw_orientation[3] = False
        if not self.movement_x[0] and not self.movement_x[1]: 
            self.defender.x += 0
            if self.draw_orientation[2]:
                afterburner = AfterBurner(self.defender, self.movement_x, self.movement_y) 
                self.particles.append(afterburner)
        if not self.movement_y[0] and not self.movement_y[1]: 
            self.defender.y += 0
        stars_ = random.randint(0, 13)
        if stars_ == 7:
            star = Star()
            self.stars.append(star)
        
        booster = Booster(self.defender, self.movement_x, self.movement_y)
        self.particles.append(booster)
        if self.lives <= 0:
            game_over_scene.__init__(dir)
            dir.scene = game_over_scene
        if self.n % 77 == 0:
            rand_ = random.randint(1,4)
            if rand_ == 1:
                self.enemy = RedGuy(0, 0)
            elif rand_ == 2:
                self.enemy = BlueGuy(0,0)
            else:
                # rand_ == 3:
                self.enemy = GoldGuy(0,0)  
                #self.enemy = BossGuy(0, 0) 
                #for n in range(self.enemy.layer_one_cube_number):
                    #theta = (n + 1) * self.enemy.inner_circumference_division
                    #boss_cube = BossCube(self.enemy, self.enemy.x + self.enemy.inner_shield_radius * math.sin(theta), self.enemy.y - self.enemy.inner_shield_radius * math.cos(theta), theta, True)
                   # self.enemies.append(boss_cube)  
                #for n in range(self.enemy.layer_two_cube_number):
                   # theta = (n + 1) * self.enemy.outer_circumference_division
                   # boss_cube = BossCube(self.enemy, self.enemy.x + self.enemy.outer_shield_radius * math.cos(theta), self.enemy.y + self.enemy.outer_shield_radius * math.sin(theta), theta, False)
                   # self.enemies.append(boss_cube)
            
            self.enemies.append(self.enemy)
        self.defender.bounce()
        for pickup in self.pickups:
            pickup.update()
            pickup.delete(self)
            if pickup.collected(self.defender):
                notification = PickupNotification(self, pickup)
                notification.play_sound()
                self.notifications.append(notification)
                if (pickup.type == 1) and len(self.collectable_weapons) > 0:
                    self.weapon_inventory.append(self.collectable_weapons[pickup.weapon_type])
                    self.collectable_weapons.remove(self.collectable_weapons[pickup.weapon_type])
                if pickup.type == 2:
                    self.weapon_inventory[pickup.weapon_type].ammo += pickup.contents
                if (pickup.type == 3) and (self.lives < 7):
                    self.lives += 1
                self.pickups.remove(pickup) 
        for particle in self.particles:
            if particle.delete():
                self.particles.remove(particle)
            particle.update()
        for star in self.stars:
            if star.delete():
                self.stars.remove(star)
            star.update()
        for projectile in self.projectiles:
            if projectile.delete():
                self.projectiles.remove(projectile)
            projectile.update()
        for enemy in self.enemies:
            enemy.update()
            enemy.bounce()
            for projectile in self.projectiles:
                if enemy.hit(projectile) == True:
                    self.projectiles.remove(projectile)
                    if enemy.dead() == True:
                        self.score += enemy.score_()
                        if enemy in self.enemies:
                            self.enemies.remove(enemy)
                            self.explosion_sounds[random.randint(0, 7)].play(0)
                            explosion(enemy, self.particles)
                            if random.randint(1, 7) == 7:
                                if len(self.collectable_weapons) == 0:
                                    what_pickup = random.randint(2, 3)
                                else:
                                    what_pickup = random.randint(1, 3)
                                if what_pickup == 1:
                                    pickup = WeaponPickup(self, enemy.x, enemy.y)
                                elif what_pickup == 2:
                                    pickup = AmmoPickup(self, enemy.x, enemy.y)
                                elif what_pickup == 3:
                                    pickup = ExtraLife(self, enemy.x, enemy.y)
                                self.pickups.append(pickup)
                    else:
                        HIT_SOUND.play(0)
                        glancing_hit(enemy, self.particles)
            if enemy.enemy_attack():
                self.lives += -1
                vanish(self.lives + 1, self.particles)
                self.enemies.remove(enemy)
                self.explosion_sounds[random.randint(0, 7)].play(0)
                damage(enemy, self.particles)    
        for notification in self.notifications:
            notification.delete(self)     
        self.n += 1

    def on_draw(self, mpos1, mpos2):

        SCREEN.fill(BLACK)
        for pickup in self.pickups:
            pickup.display()                 
        for i in range(self.lives):
            heart = Heart()
            heart.display(i)
        for particle in self.particles:
            particle.display()   
        for projectile in self.projectiles:
            projectile.display()
        for enemy in self.enemies:
            enemy.display()
        for star in self.stars:
            star.display()
        for notification in self.notifications:
            notification.display()

        if (self.draw_orientation[0] and self.draw_orientation[1]) or (self.draw_orientation[2] and self.draw_orientation[3]):
            self.defender.display()
        elif self.draw_orientation[0]: self.defender.display_right()
        elif self.draw_orientation[1]: self.defender.display_left()
        elif self.draw_orientation[2]: self.defender.display_forward()
        elif self.draw_orientation[3]: self.defender.display_back()
        else: self.defender.display()
        SCREEN.blit(self.display_score, (round(WIDTH *0.84), round(HEIGHT *0.96)))
        SCREEN.blit(self.selected_weapon_text, (round(WIDTH *0.01), round(HEIGHT *0.85)))
        SCREEN.blit(self.ammo_text, (round(WIDTH * 0.01), round(HEIGHT * 0.9)))

class GamePausedScene(Scene):
    def __init__(self, director):
        Scene.__init__(self, director)

        def unpause():
            GAME_PAUSED_SOUND.play(0)
            pygame.mixer.music.unpause()
            dir.scene = game_play_scene
        def settings():
            settings_menu_scene.previous_scene = self
            dir.scene = settings_menu_scene
        def high_scores():
            high_scores_scene.__init__(dir)
            high_scores_scene.previous_scene = self
            dir.scene = high_scores_scene
        def about():
            about_scene.previous_scene = self
            dir.scene = about_scene
        def main_menu():
            quit_menu_scene.previous_scene = self
            quit_menu_scene.destination = main_menu_scene
            dir.scene = quit_menu_scene
        def quit_menu():
            quit_menu_scene.previous_scene = self
            quit_menu_scene.destination = None
            dir.scene = quit_menu_scene

        self.functions = {'Play' : unpause, 'Settings' : settings, 'High Scores' : high_scores, 
                          'About' : about, 'Main Menu' : main_menu, 'Quit' : quit_menu } 
        self.menu = GameMenu( self.functions.keys(), self.functions, 2, 2)
        
    def on_update(self):
        pass
 
    def on_event(self, event, mpos1, mpos2):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                GAME_PAUSED_SOUND.play(0)
                pygame.mixer.music.unpause()
                dir.scene = game_play_scene

            self.menu.mouse_is_visible = False
            self.menu.set_keyboard_selection(event.key)

        if event.type == pygame.MOUSEBUTTONDOWN:
            for item in self.menu.items:
                if item.is_mouse_selection(mpos1, mpos2):
                    MENU_SELECT_SOUND.play(0)
                    self.functions[item.text]()

    def on_draw(self, mpos1, mpos2):
        if pygame.mouse.get_rel() != (0, 0):
            self.menu.mouse_is_visible = True
            self.menu.cur_item = None
        self.menu.set_mouse_visibility()

        SCREEN.fill(BLACK)

        display_game()

        for item in self.menu.items:
            if self.menu.mouse_is_visible:
                self.menu.set_mouse_selection(item, mpos1, mpos2)
            SCREEN.blit(item.label, item.position)

########################################################################################################################
########################################################################################################################
'                                                  **** MAIN ****                                                      '
########################################################################################################################
########################################################################################################################

if __name__ == '__main__':
    dir = Director()

    splash_scene = SplashScene(dir)
    main_menu_scene = MainMenuScene(dir)
    settings_menu_scene = SettingsMenuScene(dir)
    controls_menu_scene = ControlsMenuScene(dir)
    controls_entry_scene = ControlsEntryScene(dir)
    high_scores_scene = HighScoresScene(dir)
    high_score_entry_scene = HighScoreEntryScene(dir)
    about_scene = AboutScene(dir)
    intro_cut_scene = IntroCutScene(dir, main_menu_scene)
    game_play_scene = GamePlayScene(dir, intro_cut_scene)
    game_paused_scene = GamePausedScene(dir)
    game_over_scene = GameOverScene(dir)
    quit_menu_scene = QuitMenuScene(dir)
    dir.scene = splash_scene
    dir.loop()

