class GunBarrelTriangleDistances:
    def __init__(self,                 
                 target_well_api: str = None,
                 offset_well_api: str = None,
                 adjacent: int = None,
                 opposite: int = None,
                 hypotenuse: int = None):
            
        self.target_well_api = target_well_api
        self.offset_well_api = offset_well_api
        self.adjacent = adjacent
        self.opposite = opposite
        self.hypotenuse = hypotenuse

        @property
        def target_well_api(self):
            return self.target_well_api
        
        @property
        def offset_well_api(self):
            return self.offset_well_api
        
        @property
        def adjacent(self):
            return self.adjacent
        
        @property
        def opposite(self):
            return self.opposite
        
        @property
        def hypotenuse(self):
            return self.hypotenuse
        
        @target_well_api.setter
        def target_well_api(self, target_well_api: str):
            self.target_well_api = target_well_api

        @offset_well_api.setter
        def offset_well_api(self, offset_well_api: str):
            self.offset_well_api = offset_well_api

        @adjacent.setter
        def adjacent(self, adjacent: int):
            self.adjacent = adjacent

        @opposite.setter
        def opposite(self, opposite: int):
            self.opposite = opposite

        @hypotenuse.setter
        def hypotenuse(self, hypotenuse: int):
            self.hypotenuse = hypotenuse


