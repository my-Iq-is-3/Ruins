import math
import sys
import pygame
import random


pygame.init()
particles = []
jump_sound = pygame.mixer.Sound('data/audio/jump.wav')
display = pygame.Surface((600, 400)) # 300 200, game camera
font = pygame.font.Font("data/fonts/small_pixel.ttf", 8)
elist = []
total_ticks = 0
bossbar = None # does a boss bar exist
txt_indicators = []
txt_colors = {
    'physical_dmg':(255,58,51),
    'magical_dmg':(156,255,228),
    'magical_heal':(34,255,0),
    'entity_dmg':(62,12,94)
}


gamestate = 'menu'


def circle_surf(size, color):
    surf = pygame.Surface((size * 2 + 2, size * 2 + 2))
    surf.set_colorkey((0,0,0))
    pygame.draw.circle(surf, color, (size + 1, size + 1), size)
    return surf

def particle_burst(amount,clr,x,y):
    for i in range(amount):
        decay_rate = random.random()
        angle = random.randint(1, 360)
        speed = random.randint(1, 10)
        vel = [math.cos(angle) * speed, math.sin(angle) * speed]
        particles.append([random.randint(1,5)*10,clr,x,y,vel[0],vel[1],decay_rate])
def add_particle(size,clr,x,y,xvel,yvel,decay_rate):
    particles.append([size,clr,x,y,xvel,yvel,decay_rate])
def draw_particles(scroll):
    for particle in particles:
        display.blit(circle_surf(particle[0]/10,particle[1]),(particle[2]-scroll[0],particle[3]-scroll[1]))
        particle[2]+=particle[4]
        particle[3]+=particle[5]
        particle[0]-=particle[6]
        if particle[0] <= 0:
            particles.remove(particle)



