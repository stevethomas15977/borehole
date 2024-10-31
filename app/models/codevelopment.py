class Codevelopment:
    def __init__(self, 
                 reference_api: str,
                 target_api: str,
                 reference_name: str=None, 
                 target_name: str=None):
        self._reference_api = reference_api
        self._target_api = target_api
        self._reference_name = reference_name
        self._target_name = target_name

    @property
    def reference_api(self):
        return self._reference_api
    
    @reference_api.setter
    def reference_api(self, value):
        self._reference_api = value

    @property
    def target_api(self):
        return self._target_api
    
    @target_api.setter
    def target_api(self, value):
        self._target_api = value

    @property
    def reference_name(self):
        return self._reference_name

    @reference_name.setter
    def reference_name(self, value):
        self._reference_name = value

    @property
    def target_name(self):
        return self._target_name

    @target_name.setter
    def target_name(self, value):
        self._target_name = value