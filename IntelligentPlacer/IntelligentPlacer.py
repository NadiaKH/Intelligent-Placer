import IntelligentPlacer
from IntelligentPlacer.image_processing import find_bboxes, delete_spots, find_edges, draw_bbox, get_binary_image

from IntelligentPlacer.placer import find_min_intersection_configuration

from IntelligentPlacer.classification import ObjectsRecognizer

from imageio import imread
from skimage.color import rgb2gray
from matplotlib import pyplot as plt
import numpy as np

import json 
from shapely.geometry import Polygon 
from shapely.affinity import rotate, pi, translate
from itertools import product
import os 
import IntelligentPlacer


def to_singular(arr):
    arr_o = []
    for a in arr:
        if a != 'glass':
            arr_o.append(a[:-1])
        else:
            arr_o.append(a)
    return arr_o


def can_be_placed(img_path, vert, max_area=-1):

    img = imread(img_path)
    cur_dir = os.path.dirname(IntelligentPlacer.__file__)
    objr = ObjectsRecognizer(cur_dir)
    cl, bb = objr.fit_transform(img)

    with open(os.path.join(cur_dir, "objects_boundary.json"), 'r') as f:
        figures = json.load(f)
        objects = {}
        for key, val in figures.items():
            coords = np.array([val['x'], val['y']])
            objects[key] = Polygon((coords.T - np.mean(coords, axis=1)))


    names = to_singular(cl)
    fig = Polygon(vert)
    angles_dict = {"bug": [0, 45, 90, 135]
     , "button" : [0]
     , "glass" : [0]
     , "hairclaw" : [0, 90]
     , "handle" : [0, 45, 90, 135]
     , "heart" : [0, 90]
     , "pencil" : [0, 30, 60, 90, 120, 150]
     , "stone" : [0, 45, 90, 135]
     , "trefoli" : [0, 45]
     , "sharpener" : [0]}

    xs, ys = fig.boundary.xy
    xs = np.linspace(min(xs), max(xs), 7) 
    ys = np.linspace(min(ys), max(ys), 7)

    params = {}
    for name in names:
        obj = objects[name]
        angles = angles_dict[name]
        c = [(x, y, a) for x, y, a in product(xs, ys, angles) if fig.contains(translate(rotate(obj, a), x, y))]
        params[name] = c
    
    init_config = {
        name : (0, 0, 0) for name in names   
    }

    area, conf = find_min_intersection_configuration(names, objects
                                        , init_config, params
                                        , 100, i_state = 0, intersection_area=0)

    if max_area == -1:
        return area < 0.0001
    
    return area < max_area