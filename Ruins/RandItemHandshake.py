from items.HolyFeather import HolyFeather
from items.emeraldCharm import EmeraldCharm
import random

def randitem(x,y):
    items = [EmeraldCharm(x,y),HolyFeather(x,y)]
    return items[random.randint(0,len(items)-1)]