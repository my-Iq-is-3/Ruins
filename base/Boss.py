import random
import sys

import Handshake
from base.LivingEntity import LivingEntity


class Boss(LivingEntity):
    def __init__(self,eid,x,y,grav,max_health,color,sx=5,sy=13):
        self.owns_bb = False
        self.color = color
        super(Boss, self).__init__(eid,grav,max_health,x,y,sx,sy)

    def damage(self,amount):
        super(Boss, self).damage(amount)
    def on_death(self):
        Handshake.bossbar = None
    def draw(self,tile_rects,display,scroll):
        if Handshake.bossbar is None:
            Handshake.bossbar = self

        # if Handshake.total_ticks % 20 == 0:
        #     Handshake.add_particle(random.randint(1,3),self.color,self.entity.x+random.randint(-3,3),self.entity.y-self.entity.size_y,0,0,0.5)
        super(Boss, self).draw(tile_rects, display, scroll)