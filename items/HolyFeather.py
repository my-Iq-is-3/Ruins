import PlayerHandshake
from base.Item import Item


class HolyFeather(Item):
    def __init__(self,x,y):
        super(HolyFeather, self).__init__(x,y,"HolyFeather","Grants +1 max jumps","Holy Feather")

    def event(self,event_type,args=[]):
        if event_type == "SELF_PICKUP":
            PlayerHandshake.player.maxjumps+=1
