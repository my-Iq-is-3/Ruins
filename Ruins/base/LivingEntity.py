import random

from Handshake import elist, txt_indicators, particle_burst
from CallItemEventHandshake import call_item_event
import PlayerHandshake
from RandItemHandshake import randitem
from data.REntity import REntity


class LivingEntity(REntity):
    iframes = 0
    def on_collide(self):
        pass

    def damage(self,amount):

        if self.iframes > 0:
            return
        else:
            self.iframes = PlayerHandshake.player.attackingframes+1
        self.health-=amount
        call_item_event("ENTITY_DAMAGE",[amount,self])
        txt_indicators.append([amount,"entity_dmg",60,self.entity.x - random.randint(-10,10),self.entity.y - random.randint(-10,10)-20]) # txt_indicators.append([amount,type,120,self.entity.x - random.randint(-10,10),self.entity.y - random.randint(-10,10)-20])
        if self.health <= 0:
            elist.remove(self)
            particle_burst(10,(255,255,255),self.entity.x,self.entity.y)
            if random.randint(1,2) == 2:
                particle_burst(5,(0,255,0),self.entity.x,self.entity.y)
                elist.append(randitem(self.entity.x,self.entity.y))
                call_item_event("ENTITY_KILL",[self])
            self.dead = True
        max(self.health,0)



    def draw(self,tile_rects,display,scroll):
        if self.entity.rect().colliderect(PlayerHandshake.player.entity.rect()):
            self.on_collide()
        self.iframes -= 1
        super(LivingEntity, self).draw(tile_rects, display, scroll)

    def __init__(self,eid,grav,max_health,x,y,sx=5,sy=13):
        self.max_health = max_health
        self.gravity = grav
        self.health = max_health
        self.dead = False
        super(LivingEntity, self).__init__(eid,x,y,sx,sy)
