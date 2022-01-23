import pygame

import data.engine as e
from data.Vector2D import Vector2D

class REntity:
    entity = None
    max_health = 100
    health = 100
    moving_right = False
    moving_left = False
    air_timer = 0
    velocity = Vector2D(0,0)
    gravity = True
    def __init__(self, e_type,x,y,sx=5,sy=13):
        self.entity = e.entity(x,y,sx,sy,e_type)
        self.velocity.y = 0
        self.velocity.x = 0




    def get_action(self):
        return 'idle'

    def dist_to(self,entity):
        return Vector2D(entity.x,entity.y).distance_to(Vector2D(self.entity.x,self.entity.y))

    def draw(self,tile_rects,display,scroll):
        tile =[[self.entity.x,10]]
        tile_rects.append(pygame.Rect(tile[0][0], tile[0][1] * 16, 16, 16))

        movement = [0, 0]
        movement[0] += self.velocity.x
        if self.moving_right:
            movement[0] += 2
        if self.moving_left:
            movement[0] -= 2
        movement[1] += self.velocity.y
        if self.gravity:
            self.velocity.y += 0.2
            if self.velocity.y > 3:
                self.velocity.y = 3

        self.entity.set_action(self.get_action())

        collision_types = self.entity.move(movement, tile_rects)
        self.collisions_check(collision_types)
        if collision_types['bottom']:
            self.velocity.x-=self.velocity.x/2
            self.air_timer = 0
            self.velocity.y = 0
        else:
            self.air_timer += 1

        self.entity.change_frame(1)
        self.entity.display(display, scroll)

    def collisions_check(self,collisions):
        pass