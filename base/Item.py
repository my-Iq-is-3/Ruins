from Handshake import elist
import PlayerHandshake
from data.REntity import REntity


class Item(REntity):

    def event(self,event_type,args=[]):
        pass

    def __init__(self, xpos, ypos, type, desc,name):
        super(Item, self).__init__(type, xpos, ypos)
        self.entity.alpha = 50
        self.desc = desc
        self.name = name
    def draw(self, tile_rects, display, scroll):

        if self.dist_to(PlayerHandshake.player.entity) < 3:
            elist.remove(self)
            PlayerHandshake.player.items.append(self)
            self.event("SELF_PICKUP")
            if self.entity.type == "newtester":
                PlayerHandshake.player.maxjumps += 1
            if self.entity.type == "tester":
                PlayerHandshake.player.jumpstrength += 0.3
                PlayerHandshake.player.walkspeed += 0.5
                PlayerHandshake.player.max_health += 50
        else:
            super(Item, self).draw(tile_rects, display, scroll)
