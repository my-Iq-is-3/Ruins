import random

import pygame
from pygame.constants import *
import data.engine as e
import Handshake
from CallItemEventHandshake import call_item_event
from Handshake import txt_indicators
from entities.LaserSword import LaserSword


class RPlayer:

    score = 0
    atkdamage = 5
    entity = None
    max_health = 100
    health = 100
    moving_right = False
    moving_left = False
    vertical_momentum = 0
    air_timer = 0
    jump_sound = None
    items = []
    walkspeed = 1
    jumps = 1
    maxjumps = 1
    jumpstrength = 1
    monsters_killed = 0
    iframes = 0
    last_damager = "None"
    attackingframes = 0
    statuseffects = {"poison":0,"slow":0}

    def has_item(self,i):
        return self.items.__contains__(i)

    def __init__(self, jump_sound):
        self.entity = e.entity(100,100,5,13,'player')
        self.jump_sound = jump_sound
        self.dead = False

    def get_x(self):
        return self.entity.x

    def get_y(self):
        return self.entity.y

    def attack(self):
        if self.attackingframes <= 0:
            LaserSword()
            self.attackingframes = 14

    def draw(self,tile_rects,grass_sound_timer,grass_sounds,display,scroll):
        if self.dead:
            Handshake.gamestate = 'dead'
        if self.statuseffects["poison"] > 0:
            self.statuseffects["poison"]-=1
            if self.statuseffects["poison"] % 60 == 0:
                temp = self.iframes
                self.damage(5,"magical_dmg",None)
                self.iframes = temp
        if self.statuseffects["slow"] > 0:
            self.statuseffects["slow"]-=1
            if self.statuseffects["slow"] == 1:
                self.walkspeed*=2
                self.jumpstrength*=2
        self.score+=1
        player_movement = [0, 0]
        if self.moving_right:
            player_movement[0] += 2*self.walkspeed
        if self.moving_left:
            player_movement[0] -= 2*self.walkspeed
        player_movement[1] += self.vertical_momentum
        self.vertical_momentum += 0.2
        if self.vertical_momentum > 3:
            self.vertical_momentum = 3
        if player_movement[0] == 0:
            self.entity.set_action('idle')
        if player_movement[0] > 0:
            self.entity.set_flip(False)
            self.entity.set_action('run')
        if player_movement[0] < 0:
            self.entity.set_flip(True)
            self.entity.set_action('run')
        if self.attackingframes > 0:
            self.attackingframes-=1
        collision_types = self.entity.move(player_movement, tile_rects)

        if collision_types['bottom']:
            self.air_timer = 0
            self.vertical_momentum = 0
            self.jumps = self.maxjumps
            if player_movement[0] != 0:
                if grass_sound_timer == 0:
                    grass_sound_timer = 30
                    random.choice(grass_sounds).play()
        else:
            self.air_timer += 1
        self.iframes-=1
        self.iframes = max(self.iframes,0)
        self.entity.change_frame(1)
        self.entity.display(display, scroll)

    def damage(self,amount,type,entity):
        if self.iframes > 0:
            return
        self.iframes = 20
        self.health = max(self.health-amount,0)
        call_item_event("PLAYER_HURT",[amount,entity])
        txt_indicators.append([amount,type,120,self.entity.x - random.randint(-10,10),self.entity.y - random.randint(-10,10)-20])
        if self.health == 0:
            self.dead = True

    def heal(self,amount,type,emeraldcharm=False):
        if not emeraldcharm:
            call_item_event("PLAYER_HEAL",[amount])
        txt_indicators.append([amount,type,120,self.entity.x - random.randint(-10,10),self.entity.y - random.randint(-10,10) - 20])
        self.health = min(self.health+amount,self.max_health)

    def event(self,event):
        if event.type == KEYDOWN:
            if event.key == K_w:
                pygame.mixer.music.fadeout(1000)
            if event.key == K_RIGHT:
                self.moving_right = True
            if event.key == K_LEFT:
                self.moving_left = True
            if event.key == K_UP:
                if self.jumps > 0:
                    self.jump_sound.play()
                    self.jumps-=1
                    self.vertical_momentum = -3*self.jumpstrength
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                self.moving_right = False
            if event.key == K_LEFT:
                self.moving_left = False