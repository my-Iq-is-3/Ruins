import sys

player = None
def init_player(p):
    print("Before: " + str(player))
    setattr(sys.modules[__name__],"player", p)
    print("after: " + str(player))

