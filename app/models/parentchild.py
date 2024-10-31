class ParentChild:
    def __init__(self, 
                parent_api:str=None,
                parent_name:str=None,
                child_api:str=None,
                child_name:str=None,
                sibling_api:str=None,
                sibling_name:str=None,
                adjacent:str=None,
                parent_interval:str=None,
                child_interval:str=None,
                sibling_interval:str=None):
        self._parent_api = parent_api
        self._parent_name = parent_name
        self._child_api = child_api
        self._child_name = child_name
        self._sibling_api = sibling_api
        self._sibling_name = sibling_name
        self._adjacent = adjacent
        self._parent_interval = parent_interval
        self._child_interval = child_interval
        self._sibling_interval = sibling_interval

    @property
    def parent_api(self):
        return self._parent_api
    
    @property
    def parent_name(self):
        return self._parent_name
    
    @property
    def child_api(self):
        return self._child_api
    
    @property
    def child_name(self):
        return self._child_name
    
    @property
    def sibling_api(self):
        return self._sibling_api
    
    @property
    def sibling_name(self):
        return self._sibling_name
    
    @property
    def adjacent(self):
        return self._adjacent
    
    @property
    def parent_interval(self):
        return self._parent_interval
    
    @property
    def child_interval(self):
        return self._child_interval
    
    @property
    def sibling_interval(self):
        return self._sibling_interval
    
    @parent_api.setter
    def parent_api(self, value):
        self._parent_api = value

    @parent_name.setter
    def parent_name(self, value):
        self._parent_name = value

    @child_api.setter
    def child_api(self, value):
        self._child_api = value

    @child_name.setter
    def child_name(self, value):
        self._child_name = value

    @sibling_api.setter
    def sibling_api(self, value):
        self._sibling_api = value

    @sibling_name.setter
    def sibling_name(self, value):
        self._sibling_name = value

    @adjacent.setter
    def adjacent(self, value):
        self._adjacent = value

    @parent_interval.setter
    def parent_interval(self, value):
        self._parent_interval = value

    @child_interval.setter
    def child_interval(self, value):
        self._child_interval = value

    @sibling_interval.setter
    def sibling_interval(self, value):
        self._sibling_interval = value    
        

