

class Stratigraphic:
    def __init__(self,
                 period: str=None,
                 epoch: str=None,	
                 basin: str=None,	
                 formation: str=None,	
                 union_code: str=None,	
                 prism_code: str=None,
                 position: int=None,
                 color: str=None,
                 common_tanks: list=None):
        
        self.period = period
        self.epoch = epoch
        self.basin = basin
        self.formation = formation
        self.union_code = union_code
        self.prism_code = prism_code
        self.position = position
        self.color = color
        self.common_tanks = common_tanks