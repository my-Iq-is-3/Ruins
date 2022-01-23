import Handshake
import PlayerHandshake
from base.ChildEntity import ChildEntity
from base.LivingEntity import LivingEntity
from data.Vector2D import Vector2D

"""
        direction = Vector2D(player.entity.x, player.entity.y) - (Vector2D(self.entity.x, self.entity.y))
        if direction.__abs__() > 0:
            direction /= direction.__abs__()
        self.velocity.y -= 0.3
        self.velocity += direction
        if self.dist_to(player.entity) < 5:
            player.damage(20,'physical_dmg')
            elist.remove(self)
        super(HomingMissile, self).draw(tile_rects, display, scroll)
"""

class ZuraSlug(LivingEntity):
    def __init__(self,x,y):
        self.gravity = False
        self.projectile_timer = 200
        super(ZuraSlug, self).__init__('ZuraSlug',True,10,x,y)


    def draw(self,tile_rects,display,scroll):

        self.projectile_timer-=1
        if self.projectile_timer <= 0:
            self.projectile_timer = 300
            Handshake.elist.append(ZuraSlime(PlayerHandshake.player.entity.x,PlayerHandshake.player.entity.y,self.entity.x,self.entity.y,self))
        direction = Vector2D(PlayerHandshake.player.entity.x,100) - (Vector2D(self.entity.x,self.entity.y))
        if direction.__abs__() > 0:
            direction /= direction.__abs__()
        self.velocity += direction/2

        super(ZuraSlug, self).draw(tile_rects, display, scroll)

class ZuraSlime(ChildEntity):

    def __init__(self,targetx,targety,x,y,owner):
        self.targetx = targetx
        self.targety = targety
        self.gravity = False
        super(ZuraSlime, self).__init__(x,y,owner,'ZuraSlime',5,5) # TODO change 5,13 to 3,3 or something
        distancex = targetx - self.entity.x
        distancey = targety - self.entity.y
        distancex /= 10
        distancey /= 10
        self.velocity+=Vector2D(distancex,distancey)




    def draw(self,tile_rects,display,scroll):
        if self.entity.rect().colliderect(PlayerHandshake.player.entity.rect()):
            PlayerHandshake.player.statuseffects["poison"]+=300
            if not PlayerHandshake.player.statuseffects["slow"] > 0:
                PlayerHandshake.player.walkspeed*=0.5
                PlayerHandshake.player.jumpstrength*=0.5
            PlayerHandshake.player.statuseffects["slow"]+=300
            PlayerHandshake.player.damage(10,'physical_dmg',self)
            Handshake.elist.remove(self)
        super(ZuraSlime, self).draw(tile_rects, display, scroll)

    def collisions_check(self,collisions):
        if collisions["bottom"]:
            if Handshake.elist.__contains__(self):
                Handshake.elist.remove(self)