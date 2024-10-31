class WellGroupMember:
    def __init__(self, 
                 group_name: str, 
                 well_api: str,
                 well_name: str):
        self._group_name = group_name
        self._well_api = well_api
        self._well_name = well_name

    @property
    def group_name(self):
        return self._group_name
    
    @property
    def well_api(self):
        return self._well_api
    
    @property
    def well_name(self):
        return self._well_name
    
    @group_name.setter
    def group_name(self, value):
        self._group_name = value

    @well_api.setter
    def well_api(self, value):
        self._well_api = value
        
    @well_name.setter
    def well_name(self, value):
        self._well_name = value
