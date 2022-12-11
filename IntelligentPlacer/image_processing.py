from skimage.feature import canny
from skimage.filters import sobel, gaussian
from imageio import imread, imsave
from matplotlib import pyplot as plt 
from skimage.color import rgb2gray
import skimage
from skimage.filters import try_all_threshold, threshold_isodata, threshold_otsu
from skimage.morphology import binary_opening, binary_closing, binary_dilation, binary_erosion
from itertools import product 
from functools import reduce
import numpy as np
from skimage.measure import regionprops
from skimage.measure import label as sk_measure_label
import cv2


def get_side_lengths(x1, y1, x2, y2):
    """
    x1, y1, x2, y2 - rectangle diagonal corners coordinates 
    function returns width and height of a rectangle  
    """
    return np.abs(x1 - x2), np.abs(y1 - y2)


#def create_mask(init_matrix, )

def background_mask(binary_image):
    labels = sk_measure_label(np.logical_not(binary_image))
    props = np.array(regionprops(labels))
    areas = [prop.area for prop in props]
    backgr_label = props[np.argmax(areas)].label
    return labels == backgr_label 
    


def min_diameter(prop):
    return prop.feret_diameter_max ** 2 / prop.convex_area
    
def delete_spots(binary_image, delete_on_background = False):
    """
    Функция служит для очистки изображения от помех
    
    binary_image : 
              двумерная матрица np.array типа bool, 
              где False обозначает черный цвет, считающийся фоновым, 
              True обозначает белый 
    delete_on_background : 
              если False, то удаляет черные пятна из белых областей;
              если True, то удаляет белые пятна из черных областей
    """
    
    backgr_mask = background_mask(binary_image)
    labels_white = sk_measure_label(binary_image) 
    
    labels_black = sk_measure_label(
        np.logical_not(
            np.logical_or(binary_image, backgr_mask)
        )
    )
    
    white_props = regionprops(labels_white)
    black_props = regionprops(labels_black)
    all_props = white_props + black_props
    
    
    areas = [prop.area for prop in all_props]
    min_diameters = [min_diameter(prop) for prop in all_props]
    
    thresh_area = threshold_otsu(np.array(areas))
    thresh_min_diam = threshold_otsu(np.array(min_diameters))
    
    white_spots = [prop.label for prop in white_props 
                   if prop.area <= np.max(areas) / 10]
    
    black_spots = [prop.label for prop in black_props
                   if prop.area <= thresh_area
                   or min_diameter(prop) <= thresh_min_diam ]
    
    white_spot_regions = [labels_white == label for label in white_spots]
    black_spot_regions = [labels_black == label for label in black_spots]
    
    white_spots_mask = reduce(np.logical_or, white_spot_regions
                              , np.zeros_like(binary_image, dtype='bool'))
    black_spots_mask = reduce(np.logical_or, black_spot_regions
                              , np.zeros_like(binary_image, dtype='bool'))
    
    cleared_from_black_spots = np.logical_or(binary_image, black_spots_mask)
    cleared_from_white_spots = np.logical_and(cleared_from_black_spots
                                              , np.logical_not(white_spots_mask)) 
    

    return cleared_from_white_spots

def find_edges1(gray_img):
    padded = np.pad(gray_img, 100, 'symmetric')
    blur_img = gaussian(padded, 0.5)
    edges = canny(blur_img, sigma=2.45, low_threshold=0.01)
    dilated = binary_dilation(edges, footprint=np.ones((20, 20)))
    return dilated[100:-100, 100:-100]
   
    
def find_edges(gray_img):
    padded = np.pad(gray_img, 100, 'symmetric')
    #blur_img = gaussian(padded, 0.5)
    edges = canny(padded, sigma=7, low_threshold=0.01, high_threshold=0.06)
    dilated = binary_dilation(edges, footprint=np.ones((25, 25)))
    return dilated[100:-100, 100:-100]

    
def draw_bbox(img, box):
    b = box 
    img[b[0]:b[2], b[1]-10:b[1]+10] = 0
    img[b[0]:b[2], b[3]-10:b[3]+10] = 0

    img[b[0]-10:b[0]+10, b[1]:b[3]] = 0
    img[b[2]-10:b[2]+10, b[1]:b[3]] = 0
        

def find_bboxes(gray_img):
    
    edges = find_edges(gray_img)
    labels = sk_measure_label(edges)
    props = regionprops(labels)
    props = [p for p in props if p.area_convex < gray_img.size // 4]
    
    
    threshold_diameter = max([p.feret_diameter_max for p in props]) 
    threshold_area = max([p.area_convex for p in props]) 
    
    props = [p for p in props if 
             (p.feret_diameter_max > threshold_diameter / 4 or p.area_convex > threshold_area / 4) 
             and not (p.feret_diameter_max < threshold_diameter / 10 or p.area_convex < threshold_area / 10)]
    
    bboxes = [p.bbox for p in props]
    return bboxes


def area(coords):
    x1, y1, x2, y2 = coords
    return (x2 - x1) * (y2 - y1)

def bbox_region_to_binary(obj_img):
    x, y = obj_img.shape
    xs = [int(np.round(v)) for v in np.linspace(0, x, 10)]
    ys = [int(np.round(v)) for v in np.linspace(0, y, int(10 * y / x))]
    z_0 = np.zeros_like(obj_img, dtype='bool')
    
    edges = binary_erosion(find_edges(obj_img), footprint=np.ones((7, 7)))
    thresh_iso = threshold_isodata(obj_img)
    #z_0 = obj_img <= thresh_iso
    
    for (x1, x2), (y1, y2) in product(zip(xs, xs[1:]), zip(ys, ys[1:])):   
        lx, ly = x2 - x1, y2 - y1
        
        if np.any(edges[x1 + lx // 3 : x2 - lx // 3, y1 + ly // 3 : y2 - ly // 3 ]):
            thresh_iso = threshold_isodata(obj_img[x1:x2, y1:y2])
            z_0[x1:x2, y1:y2] = obj_img[x1:x2, y1:y2] <= thresh_iso
            
    xs1 = [int(np.round(v)) for v in np.linspace(x / 20, x * 19 / 20, 9)]
    ys1 = [int(np.round(v)) for v in np.linspace(x / 20, x * 19 / 20, int(10 * y / x) - 1)]
    
    for (x1, x2), (y1, y2) in product(zip(xs1, xs1[1:]), zip(ys1, ys1[1:])):   
        lx, ly = x2 - x1, y2 - y1
        
        if np.any(edges[x1 + lx // 3 : x2 - lx // 3, y1 + ly // 3 : y2 - ly // 3 ]):
            thresh_iso = threshold_isodata(obj_img[x1:x2, y1:y2])
            z_0[x1:x2, y1:y2] = obj_img[x1:x2, y1:y2] <= thresh_iso

    return z_0


def get_binary_image(gray_img):
    bboxes = find_bboxes(gray_img)
    bboxes = sorted(bboxes, key = area, reverse=True)
    z = np.zeros_like(gray_img, dtype='bool')

    for x1, y1, x2, y2 in bboxes:
        z[x1:x2, y1:y2] = bbox_region_to_binary(gray_img[x1:x2, y1:y2])
    

    edges = binary_erosion(find_edges(gray_img), footprint=np.ones((15, 15)))
    z = binary_erosion(np.logical_or(z, edges), footprint=np.ones((10, 10)))
    z = binary_dilation(z, footprint=np.ones((12, 12)))
    
    z[:, 0:100] = False
    z[:, -100:] = False
    z[0:100, :] = False
    z[-100:, :] = False
    
    binary_img = delete_spots(z)
    
    return binary_img


def clip(img, bbox):
    x1, y1, x2, y2 = bbox
    return img[x1:x2, y1:y2]


def pad_bbox(bbox, padding):
    x1, y1, x2, y2 = bbox
    return (x1 - padding, y1 - padding, x2 + padding, y2 + padding)
    
    
def shadow_background(img, prop, sigma=5, padding=20):
    mask = gaussian(np.pad(prop.image_filled, padding), sigma)
    reg = clip(img, pad_bbox(prop.bbox, padding))
    shadowed = np.repeat(mask[:, :, None], axis=2, repeats=3) * reg
    to_int = np.array(np.round(shadowed), dtype='int')
    return to_int


def equal_pad(img):
    shape = np.array(img.shape[:2])
    p1, p2 = np.max([[0, 0],  shape[::-1] - shape], axis=0)
    padding = [(p1 // 2, (p1 + 1) // 2), (p2 // 2, (p2 + 1) // 2), (0, 0)][:len(img.shape)]
    return np.pad(img, padding)


def prep_img(img):
    i, j, _ = img.shape
    x_pad = max(0, j - i)
    y_pad = max(0, i - j)
    a = np.pad(img, ((50, 50 + x_pad), (50, 50 + y_pad), (0, 0)), mode='edge')
    resized = cv2.resize(a, (224, 224), interpolation = cv2.INTER_AREA)
    return resized
