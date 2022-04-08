import copy 
from shapely import affinity
from shapely.affinity import rotate, pi, translate
from shapely.geometry import Polygon 

def find_min_intersection_configuration(names, objects
                                        , configuration, params
                                        , area_max, i_state = 0, intersection_area=0):
    if intersection_area > area_max:
        return (-1, None)
    if i_state >= len(names):
        return (intersection_area, configuration)
    
    name = names[i_state]
    obj = objects[name]
    
    min_area = -1
    min_config = None
    
    for x, y, a in params[name]:
        configuration[name] = (x, y, a)
        
        tr_obj = translate(rotate(obj, a), x, y)
        
        add_area = 0
        for other_obj_name in names[:i_state]:
            x_o, y_o, a_o = configuration[other_obj_name]
            
            other_obj = objects[other_obj_name]
            other_tr_obj = translate(rotate(other_obj, a_o), x_o, y_o)
            
            add_area += tr_obj.intersection(other_tr_obj).area
        
        if intersection_area + add_area > area_max:
            continue
        
        
        area, config = find_min_intersection_configuration(names, objects, copy.deepcopy(configuration)
                                            , params, area_max, i_state + 1
                                            , intersection_area + add_area) 
        if area == -1:
            continue
        
        
        if min_area == -1 or area < min_area:
            min_config = config
            min_area = area
            if area_max > min_area:
                area_max = min_area
            
    return (min_area, min_config)
    