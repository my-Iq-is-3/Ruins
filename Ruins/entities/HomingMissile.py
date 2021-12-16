from Handshake import elist
import PlayerHandshake
from data.REntity import REntity
from data.Vector2D import Vector2D

class HomingMissile(REntity):

    def __init__(self, xpos, ypos):
        super(HomingMissile, self).__init__('tester', xpos, ypos)

    def draw(self, tile_rects, display, scroll):

        direction = Vector2D(PlayerHandshake.player.entity.x, PlayerHandshake.player.entity.y) - (Vector2D(self.entity.x, self.entity.y))
        if direction.__abs__() > 0:
            direction /= direction.__abs__()
        self.velocity.y -= 0.3
        self.velocity += direction
        if self.dist_to(PlayerHandshake.player.entity) < 5:
            PlayerHandshake.player.damage(20,'physical_dmg',self)
            elist.remove(self)
        super(HomingMissile, self).draw(tile_rects, display, scroll)
