from base.Boss import Boss


class CelestialAnomaly(Boss):
    def __init__(self,x,y):
        #flash
        #set blocks
        super(CelestialAnomaly, self).__init__('CelestialAnomaly',x,y,False,200,(255, 87, 51),32,32)

    def draw(self,tile_rects,display,scroll):



        super(CelestialAnomaly, self).draw(tile_rects, display, scroll)