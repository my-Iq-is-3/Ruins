from Handshake import elist
from CallItemEventHandshake import call_item_event
import PlayerHandshake
from base.LivingEntity import LivingEntity
from base.ChildEntity import ChildEntity


class LaserSword(ChildEntity):
    def __init__(self):
        super(LaserSword, self).__init__(PlayerHandshake.player.entity.x,PlayerHandshake.player.entity.y,PlayerHandshake.player.entity,'playerattack',sx=13,sy=10)
        self.gravity = False
        elist.append(self)


    def draw(self,tile_rects,display,scroll):
        self.entity.set_pos(PlayerHandshake.player.entity.x,PlayerHandshake.player.entity.y)
        self.entity.flip = PlayerHandshake.player.entity.flip
        if self.entity.flip:
            self.entity.set_pos(self.entity.x-7,self.entity.y)
        else: self.entity.set_pos(self.entity.x+3,self.entity.y)
        for ent in elist:
            if self.entity.rect().colliderect(ent.entity.rect()):
                if issubclass(type(ent),LivingEntity):
                    ent.damage(PlayerHandshake.player.atkdamage)
                    call_item_event("ENTITY_DAMAGE",[ent,PlayerHandshake.player.atkdamage])
        if PlayerHandshake.player.attackingframes <= 0:
            elist.remove(self)
        super(LaserSword, self).draw(tile_rects, display, scroll)
