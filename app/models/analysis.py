class Analysis:
    def __init__(self, 
                 api:str=None, 
                 name:str=None, 
                 direction:str=None, 
                 dominant_direction:str=None,
                 interval:str=None,
                 lateral_length:int=None, 
                 lateral_start_latitude:float=None, 
                 lateral_start_longitude:float=None, 
                 lateral_midpoint_latitude:float=None, 
                 lateral_midpoint_longitude:float=None, 
                 lateral_end_latitude:float=None, 
                 lateral_end_longitude:float=None, 
                 lateral_start_grid_x:float=None,
                 lateral_start_grid_y:float=None,
                 lateral_start_subsurface_depth:float=None,
                 lateral_midpoint_grid_x:float=None, 
                 lateral_midpoint_grid_y:float=None, 
                 lateral_midpoint_subsurface_depth:float=None,
                 lateral_end_grid_x:float=None,
                 lateral_end_grid_y:float=None,
                 lateral_end_subsurface_depth:float=None,
                 subsurface_depth:int=None,
                 first_production_date:str=None,
                 adjacent_1:str=None,
                 adjacent_2:str=None, 
                 distance_1:int=None,
                 distance_2:int=None,
                 hypotenuse_1:int=None,
                 hypotenuse_2:int=None,
                 group_id:str=None,              
                 codevelopment:str=None,
                 average_horizontal_spacing:int=None,
                 group_average_horizontal_spacing:int=None,
                 group_average_hypotenuse_spacing:int=None,
                 parents:str=None,
                 parent_1:str=None,
                 parent_1_first_production_date:str=None,
                 parent_1_delta_first_production_months:str=None,
                 parent_1_interval:str=None,
                 parent_2:str=None,
                 parent_2_first_production_date:str=None,
                 parent_2_delta_first_production_months:str=None,
                 parent_2_interval:str=None,
                 child:str=None,
                 sibling:str=None,
                 adjacent_child:str=None,
                 bound:str=None,
                 gun_barrel_x:int=None,
                 gun_barrel_y:int=None,
                 gun_barrel_z:int=None,
                 target_well_spacing_gun_barrel_plot_flag:bool=None,
                 gun_barrel_index:int=None,
                 cumoil_bblperft:int=None,
                 pct_of_group_cumoil_bblperft:float=None,
                 pct_of_group_cumoil_bblperft_greater_than:str=None):
        
        self._api = api
        self._name = name
        self._direction = direction
        self._dominant_direction = dominant_direction
        self._interval = interval
        self._lateral_length = lateral_length
        self._lateral_start_latitude = lateral_start_latitude
        self._lateral_start_longitude = lateral_start_longitude
        self._lateral_midpoint_latitude = lateral_midpoint_latitude
        self._lateral_midpoint_longitude = lateral_midpoint_longitude
        self._lateral_end_latitude = lateral_end_latitude
        self._lateral_end_longitude = lateral_end_longitude
        self._lateral_start_grid_x = lateral_start_grid_x
        self._lateral_start_grid_y = lateral_start_grid_y
        self._lateral_start_subsurface_depth = lateral_start_subsurface_depth
        self._lateral_midpoint_grid_x = lateral_midpoint_grid_x
        self._lateral_midpoint_grid_y = lateral_midpoint_grid_y
        self._lateral_midpoint_subsurface_depth = lateral_midpoint_subsurface_depth
        self._lateral_end_grid_x = lateral_end_grid_x
        self._lateral_end_grid_y = lateral_end_grid_y
        self._lateral_end_subsurface_depth = lateral_end_subsurface_depth
        self._subsurface_depth = subsurface_depth
        self._first_production_date = first_production_date
        self._adjacent_1 = adjacent_1
        self._adjacent_2 = adjacent_2
        self._distance_1 = distance_1
        self._distance_2 = distance_2
        self._hypotenuse_1 = hypotenuse_1
        self._hypotenuse_2 = hypotenuse_2
        self._group_id = group_id
        self._codevelopment = codevelopment
        self._average_horizontal_spacing = average_horizontal_spacing
        self._group_average_horizontal_spacing = group_average_horizontal_spacing
        self._group_average_hypotenuse_spacing = group_average_hypotenuse_spacing
        self._parents = parents
        self._parent_1 = parent_1
        self._parent_1_first_production_date = parent_1_first_production_date
        self._parent_1_delta_first_production_months = parent_1_delta_first_production_months
        self._parent_1_interval = parent_1_interval
        self._parent_2 = parent_2
        self._parent_2_first_production_date = parent_2_first_production_date
        self._parent_2_delta_first_production_months = parent_2_delta_first_production_months
        self._parent_2_interval = parent_2_interval
        self._child = child
        self._adjacent_child = adjacent_child
        self._sibling = sibling
        self._bound = bound
        self._gun_barrel_x = gun_barrel_x
        self._gun_barrel_y = gun_barrel_y
        self._gun_barrel_z = gun_barrel_z
        self._target_well_spacing_gun_barrel_plot_flag = target_well_spacing_gun_barrel_plot_flag
        self._gun_barrel_index = gun_barrel_index
        self._cumoil_bblperft = cumoil_bblperft
        self._pct_of_group_cumoil_bblperft = pct_of_group_cumoil_bblperft
        self._pct_of_group_cumoil_bblperft_greater_than = pct_of_group_cumoil_bblperft_greater_than

    @property
    def api(self):
        return self._api

    @api.setter
    def api(self, value):
        self._api = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        self._direction = value

    @property
    def dominant_direction(self):
        return self._dominant_direction
    
    @dominant_direction.setter
    def dominant_direction(self, value):
        self._dominant_direction = value

    @property
    def interval(self):
        return self._interval
    
    @interval.setter
    def interval(self, value):
        self._interval = value
        
    @property
    def lateral_length(self):
        return self._lateral_length

    @lateral_length.setter
    def lateral_length(self, value):
        self._lateral_length = value

    @property
    def lateral_start_latitude(self):
        return self._lateral_start_latitude

    @lateral_start_latitude.setter
    def lateral_start_latitude(self, value):
        self._lateral_start_latitude = value

    @property
    def lateral_start_longitude(self):
        return self._lateral_start_longitude

    @lateral_start_longitude.setter
    def lateral_start_longitude(self, value):
        self._lateral_start_longitude = value

    @property
    def lateral_midpoint_latitude(self):
        return self._lateral_midpoint_latitude

    @lateral_midpoint_latitude.setter
    def lateral_midpoint_latitude(self, value):
        self._lateral_midpoint_latitude = value

    @property
    def lateral_midpoint_longitude(self):
        return self._lateral_midpoint_longitude

    @lateral_midpoint_longitude.setter
    def lateral_midpoint_longitude(self, value):
        self._lateral_midpoint_longitude = value

    @property
    def lateral_end_latitude(self):
        return self._lateral_end_latitude

    @lateral_end_latitude.setter
    def lateral_end_latitude(self, value):
        self._lateral_end_latitude = value

    @property
    def lateral_end_longitude(self):
        return self._lateral_end_longitude

    @lateral_end_longitude.setter
    def lateral_end_longitude(self, value):
        self._lateral_end_longitude = value

    @property
    def lateral_start_grid_x(self):
        return self._lateral_start_grid_x
    
    @lateral_start_grid_x.setter
    def lateral_start_grid_x(self, value):
        self._lateral_start_grid_x = value

    @property
    def lateral_start_grid_y(self):
        return self._lateral_start_grid_y
    
    @lateral_start_grid_y.setter
    def lateral_start_grid_y(self, value):
        self._lateral_start_grid_y = value

    @property
    def lateral_start_subsurface_depth(self):
        return self._lateral_start_subsurface_depth
    
    @lateral_start_subsurface_depth.setter
    def lateral_start_subsurface_depth(self, value):
        self._lateral_start_subsurface_depth = value

    @property
    def lateral_midpoint_grid_x(self):
        return self._lateral_midpoint_grid_x
    
    @lateral_midpoint_grid_x.setter
    def lateral_midpoint_grid_x(self, value):
        self._lateral_midpoint_grid_x = value

    @property
    def lateral_midpoint_grid_y(self):
        return self._lateral_midpoint_grid_y
    
    @lateral_midpoint_grid_y.setter
    def lateral_midpoint_grid_y(self, value):
        self._lateral_midpoint_grid_y = value

    @property
    def lateral_midpoint_subsurface_depth(self):
        return self._lateral_midpoint_subsurface_depth
    
    @lateral_midpoint_subsurface_depth.setter
    def lateral_midpoint_subsurface_depth(self, value):
        self._lateral_midpoint_subsurface_depth = value

    @property
    def lateral_end_grid_x(self):
        return self._lateral_end_grid_x
    
    @lateral_end_grid_x.setter
    def lateral_end_grid_x(self, value):
        self._lateral_end_grid_x = value

    @property
    def lateral_end_grid_y(self):
        return self._lateral_end_grid_y
    
    @lateral_end_grid_y.setter
    def lateral_end_grid_y(self, value):
        self._lateral_end_grid_y = value

    @property
    def lateral_end_subsurface_depth(self):
        return self._lateral_end_subsurface_depth
    
    @lateral_end_subsurface_depth.setter
    def lateral_end_subsurface_depth(self, value):
        self._lateral_end_subsurface_depth = value
    
    @property
    def subsurface_depth(self):
        return self._subsurface_depth
    
    @subsurface_depth.setter
    def subsurface_depth(self, value):
        self._subsurface_depth = value

    @property
    def first_production_date(self):
        return self._first_production_date

    @first_production_date.setter
    def first_production_date(self, value):
        self._first_production_date = value

    @property
    def adjacent_1(self):
        return self._adjacent_1
    
    @adjacent_1.setter
    def adjacent_1(self, value):
        self._adjacent_1 = value

    @property
    def adjacent_2(self):
        return self._adjacent_2
    
    @adjacent_2.setter
    def adjacent_2(self, value):
        self._adjacent_2 = value

    @property
    def distance_1(self):
        return self._distance_1
    
    @distance_1.setter
    def distance_1(self, value):
        self._distance_1 = value

    @property
    def distance_2(self):
        return self._distance_2
    
    @distance_2.setter
    def distance_2(self, value):
        self._distance_2 = value

    @property
    def hypotenuse_1(self):
        return self._hypotenuse_1
    
    @hypotenuse_1.setter
    def hypotenuse_1(self, value):
        self._hypotenuse_1 = value

    @property
    def hypotenuse_2(self):
        return self._hypotenuse_2
    
    @hypotenuse_2.setter
    def hypotenuse_2(self, value):
        self._hypotenuse_2 = value

    @property
    def group_id(self):
        return self._group_id
    
    @group_id.setter
    def group_id(self, value):
        self._group_id = value

    @property
    def codevelopment(self):
        return self._codevelopment
    
    @codevelopment.setter
    def codevelopment(self, value):
        self._codevelopment = value

    @property
    def average_horizontal_spacing(self):
        return self._average_horizontal_spacing
    
    @average_horizontal_spacing.setter
    def average_horizontal_spacing(self, value):
        self._average_horizontal_spacing= value

    @property
    def group_average_horizontal_spacing(self):
        return self._group_average_horizontal_spacing
    
    @group_average_horizontal_spacing.setter
    def group_average_horizontal_spacing(self, value):
        self._group_average_horizontal_spacing = value

    @property
    def group_average_hypotenuse_spacing(self):
        return self._group_average_hypotenuse_spacing
    
    @group_average_hypotenuse_spacing.setter
    def group_average_hypotenuse_spacing(self, value):
        self._group_average_hypotenuse_spacing = value

    @property
    def parents(self):
        return self._parents
    
    @parents.setter
    def parents(self, value):
        self._parents = value

    @property
    def parent_1(self):
        return self._parent_1
    
    @parent_1.setter
    def parent_1(self, value):
        self._parent_1 = value

    @property
    def parent_1_first_production_date(self):
        return self._parent_1_first_production_date
    
    @parent_1_first_production_date.setter
    def parent_1_first_production_date(self, value):
        self._parent_1_first_production_date = value

    @property
    def parent_1_delta_first_production_months(self):
        return self._parent_1_delta_first_production_months
    
    @parent_1_delta_first_production_months.setter
    def parent_1_delta_first_production_months(self, value):
        self._parent_1_delta_first_production_months = value

    @property
    def parent_1_interval(self):
        return self._parent_1_interval
    
    @parent_1_interval.setter
    def parent_1_interval(self, value):
        self._parent_1_interval = value

    @property
    def parent_2_delta_first_production_months(self):
        return self._parent_2_delta_first_production_months
    
    @parent_2_delta_first_production_months.setter
    def parent_2_delta_first_production_months(self, value):
        self._parent_2_delta_first_production_months = value

    @property
    def parent_2(self):
        return self._parent_2
    
    @parent_2.setter
    def parent_2(self, value):
        self._parent_2 = value

    @property
    def parent_2_first_production_date(self):
        return self._parent_2_first_production_date
    
    @parent_2_first_production_date.setter
    def parent_2_first_production_date(self, value):
        self._parent_2_first_production_date = value

    @property
    def parent_2_interval(self):
        return self._parent_2_interval
    
    @parent_2_interval.setter
    def parent_2_interval(self, value):
        self._parent_2_interval = value

    @property
    def child(self):
        return self._child
    
    @child.setter
    def child(self, value):
        self._child = value

    @property
    def adjacent_child(self):
        return self._adjacent_child 
    
    @adjacent_child.setter
    def adjacent_child(self, value):
        self._adjacent_child = value

    @property
    def sibling(self):
        return self._sibling
    
    @sibling.setter
    def sibling(self, value):
        self._sibling = value
        
    @property
    def bound(self):
        return self._bound

    @bound.setter
    def bound(self, value):
        self._bound = value

    @property
    def gun_barrel_x(self):
        return self._gun_barrel_x
    
    @gun_barrel_x.setter
    def gun_barrel_x(self, value):
        self._gun_barrel_x = value

    @property
    def gun_barrel_y(self):
        return self._gun_barrel_y
    
    @gun_barrel_y.setter
    def gun_barrel_y(self, value):
        self._gun_barrel_y = value

    @property
    def gun_barrel_z(self):
        return self._gun_barrel_z
    
    @gun_barrel_z.setter
    def gun_barrel_z(self, value):
        self._gun_barrel_z = value
        
    @property
    def target_well_spacing_gun_barrel_plot_flag(self):
        return self._target_well_spacing_gun_barrel_plot_flag
    
    @target_well_spacing_gun_barrel_plot_flag.setter
    def target_well_spacing_gun_barrel_plot_flag(self, value):
        self._target_well_spacing_gun_barrel_plot_flag = value

    @property
    def gun_barrel_index(self):
        return self._gun_barrel_index
    
    @gun_barrel_index.setter
    def gun_barrel_index(self, value):
        self._gun_barrel_index = value

    @property
    def cumoil_bblperft(self):
        return self._cumoil_bblperft
    
    @cumoil_bblperft.setter
    def cumoil_bblperft(self, value):
        self._cumoil_bblperft = value

    @property
    def pct_of_group_cumoil_bblperft(self):
        return self._pct_of_group_cumoil_bblperft
    
    @pct_of_group_cumoil_bblperft.setter
    def pct_of_group_cumoil_bblperft(self, value):
        self._pct_of_group_cumoil_bblperft = value

    @property
    def pct_of_group_cumoil_bblperft_greater_than(self):
        return self._pct_of_group_cumoil_bblperft_greater_than
    
    @pct_of_group_cumoil_bblperft_greater_than.setter
    def pct_of_group_cumoil_bblperft_greater_than(self, value):
        self._pct_of_group_cumoil_bblperft_greater_than = value