from Handshake import font, display


class ItemHoverable:
    def __init__(self, x1, y1, x2, y2, name, desc):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.name = name
        self.desc = desc

    def onhover(self, mx, my):

        mx/=2
        my/=2
        if self.x1 < mx < self.x2 and self.y1 < my < self.y2:
            iname = font.render(self.name, False, (255, 255, 255), (0, 0, 0))
            idesc = font.render(self.desc, False, (100,100,100),(0,0,0))
            display.blit(idesc,(mx,my+iname.get_size()[1]))
            display.blit(iname, (mx, my))
