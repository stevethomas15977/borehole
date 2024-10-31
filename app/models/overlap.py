

class Overlap:
    def __init__(self, 
                 reference_api: str,
                 reference_name:str, 
                 target_api: str,
                 target_name:str, 
                 overlap_feet:int=None, 
                 overlap_percentage:float=None):
        
        self._reference_api = reference_api
        self._target_api = target_api
        self._reference_name = reference_name
        self._target_name = target_name
        self._overlap_feet = overlap_feet
        self._overlap_percentage = overlap_percentage

    @property
    def reference_api(self):
        return self._reference_api
    
    @reference_api.setter
    def reference_api(self, value):
        self._reference_api = value

    @property
    def reference_name(self):
        return self._reference_name

    @reference_name.setter
    def reference_name(self, value):
        self._reference_name = value

    @property
    def target_api(self):
        return self._target_api
    
    @target_api.setter
    def target_api(self, value):
        self._target_api = value
        
    @property
    def target_name(self):
        return self._target_name

    @target_name.setter
    def target_name(self, value):
        self._target_name = value

    @property
    def overlap_feet(self):
        return self._overlap_feet
    
    @overlap_feet.setter
    def overlap_feet(self, value):
        self._overlap_feet = value

    @property
    def overlap_percentage(self):
        return self._overlap_percentage
    
    @overlap_percentage.setter
    def overlap_percentage(self, value):
        self._overlap_percentage = value