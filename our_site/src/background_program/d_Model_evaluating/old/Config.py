class Config(object):
    def __init__(self,**entries):
        self.__dict__.update(entries)
#对象生成调用：obj=change(**dict),obj.key值