from base.LivingEntity import LivingEntity


class TestingEntity(LivingEntity):
    def __init__(self,x,y):
        super(TestingEntity, self).__init__('tester',True,10,x,y)

