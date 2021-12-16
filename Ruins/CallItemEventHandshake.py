import PlayerHandshake


def call_item_event(event,args=[]):
    for item in PlayerHandshake.player.items:
        item.event(event,args)
