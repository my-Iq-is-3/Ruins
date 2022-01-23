from base import LivingEntity


class PossessedBanner(LivingEntity):
    def __init__(self,x,y):
        super(PossessedBanner, self).__init__('newtester', True, 100, x, y)

    def draw(self,tile_rects,display,scroll):
        self.damage(1)
        super(PossessedBanner, self).draw(tile_rects, display, scroll)
