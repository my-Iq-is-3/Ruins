from data.REntity import REntity


class ChildEntity(REntity):
    def __init__(self,x,y,owner,etype,sx=5,sy=13):
        self.owner = owner
        super(ChildEntity, self).__init__(etype,x,y,sx,sy)
