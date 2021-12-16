import PlayerHandshake
from base.Item import Item


class EmeraldCharm(Item):

    def __init__(self,x,y):
        super(EmeraldCharm, self).__init__(x,y,'EmeraldCharm','increased healing effectiveness','emerald charm')

    def event(self,event_type,args=[]):
        if event_type == "PLAYER_HEAL":
            PlayerHandshake.player.heal(int(args[0]/2),'magical_heal',True)