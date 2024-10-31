class GunBarrel:
    def __init__(self,
                 target_well_api: str = None,
                 offset_well_api: str = None,
                 overlap_feet: int = None,
                 overlap_percentage: int = None,
                 cumulative_oil_per_ft: int = None,
                 overlap_cumulative_oil_ft: int = None,
                 months_from_first_production: int = None):
        
        self._target_well_api: str = target_well_api
        self._offset_well_api: str = offset_well_api
        self._overlap_feet: int = overlap_feet
        self._overlap_percentage: int = overlap_percentage
        self._cumulative_oil_per_ft: int = cumulative_oil_per_ft
        self._overlap_cumulative_oil_ft: int = overlap_cumulative_oil_ft
        self._months_from_first_production: int = months_from_first_production

    @property
    def target_well_api(self):
        return self._target_well_api
    
    @target_well_api.setter
    def target_well_api(self, target_well_api: str):
        self._target_well_api = target_well_api

    @property
    def offset_well_api(self):
        return self._offset_well_api
    
    @offset_well_api.setter
    def offset_well_api(self, offset_well_api: str):
        self._offset_well_api = offset_well_api

    @property
    def overlap_feet(self):
        return self._overlap_feet
    
    @overlap_feet.setter
    def overlap_feet(self, overlap_feet: int):
        self._overlap_feet = overlap_feet

    @property
    def overlap_percentage(self):
        return self._overlap_percentage
    
    @overlap_percentage.setter
    def overlap_percentage(self, overlap_percentage: int):
        self._overlap_percentage = overlap_percentage

    @property
    def cumulative_oil_per_ft(self):
        return self._cumulative_oil_per_ft
    
    @cumulative_oil_per_ft.setter
    def cumulative_oil_per_ft(self, cumulative_oil_per_ft: int):
        self._cumulative_oil_per_ft = cumulative_oil_per_ft

    @property
    def months_from_first_production(self):
        return self._months_from_first_production
    
    @months_from_first_production.setter
    def months_from_first_production(self, months_from_first_production: int):
        self._months_from_first_production = months_from_first_production
    
    @property
    def overlap_cumulative_oil_ft(self):
        return self._overlap_cumulative_oil_ft
    
    @overlap_cumulative_oil_ft.setter
    def overlap_cumulative_oil_ft(self, overlap_cumulative_oil_ft: int):
        self._overlap_cumulative_oil_ft = overlap_cumulative_oil_ft

