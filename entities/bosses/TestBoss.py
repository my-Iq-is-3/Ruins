from base.Boss import Boss


class TestBoss(Boss):
    def __init__(self,x,y):
        super(TestBoss, self).__init__("tester",x,y,False,100,(255,0,0))