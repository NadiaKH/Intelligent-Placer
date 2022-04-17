import IntelligentPlacer.image_processing
from IntelligentPlacer.image_processing import find_bboxes, delete_spots, find_edges, get_binary_image
from IntelligentPlacer.image_processing import clip, pad_bbox, shadow_background, equal_pad
from IntelligentPlacer.image_processing import prep_img


import skimage
from skimage.color import rgb2gray
from skimage.measure import label as sk_measure_label, regionprops
from skimage.transform import resize, rescale

import os 
import numpy as np
import pandas as pd 
import cv2
from imageio import imread, imsave
from matplotlib import pyplot as plt 

from tensorflow.keras.applications import VGG19

from sklearn.ensemble import RandomForestClassifier as RF


class ObjectsRecognizer:
    def __init__(self, csv_dir):
        self.df_prepared = pd.read_csv(os.path.join(csv_dir, "prepared.csv"), index_col=0)
        self.df_binary = pd.read_csv(os.path.join(csv_dir, "binary.csv"), index_col=0)
        self.df_shadowed = pd.read_csv(os.path.join(csv_dir,"shadowed.csv"), index_col=0)
                                       
        
        
        self.model = VGG19(include_top=True, weights="imagenet", 
                           input_tensor=None, input_shape=None,
                           pooling=None, classes=1000, 
                           classifier_activation="softmax")
        
        self.rf_prepared = RF(n_estimators=100
                         , max_depth=7
                         , min_samples_leaf=3).fit(self.df_prepared.drop('class', axis=1)
                                                   , self.df_prepared['class'])
        self.rf_shadowed = RF(n_estimators=100
                         , max_depth=7
                         , min_samples_leaf=3).fit(self.df_shadowed.drop('class', axis=1)
                                                   , self.df_shadowed['class'])
        self.rf_binary = RF(n_estimators=100
                       , max_depth=7
                       , min_samples_leaf=3).fit(self.df_binary.drop('class', axis=1)
                                                 , self.df_binary['class'])
        
        
    def __select_objects_and_apply_filters(self, img):
        gray_img = rgb2gray(img)
        binary_img = get_binary_image(gray_img)
        props = regionprops(sk_measure_label(binary_img))
        
        shadowed = []
        prepared = []
        masks = []
        
        for p in props:
            shadowed.append(equal_pad(shadow_background(img, p)))
    
        for p in props:
            x1, y1, x2, y2 = p.bbox
            prepared.append(prep_img(img[x1:x2, y1:y2]))
    
        for p in props:
            im = np.array(np.repeat(equal_pad(p.image_filled)[:, :, None], axis=2, repeats=3), dtype='float')
            masks.append(np.pad(im, [(100, 100), (100, 100), (0, 0)]))
    
        for i, im in enumerate(shadowed):
            shadowed[i] = cv2.resize(np.array(im, dtype='uint8'), (224, 224), interpolation = cv2.INTER_AREA)

        for i, im in enumerate(masks):
            masks[i] =  cv2.resize(np.array(im * 255, dtype='uint8'), (224, 224), interpolation = cv2.INTER_AREA)
            
        bboxes = [p.bbox for p in props]
        shadowed = np.array(shadowed) / 255
        prepared = np.array(prepared) / 255
        masks = np.array(masks) / 255
        
        return shadowed, prepared, masks, bboxes
    
        
    def __predict_classes(self, pred_shadowed, pred_prepared, pred_masks):
        cl_pr = self.rf_prepared.predict(pred_prepared)
        cl_bin = self.rf_binary.predict(pred_masks) 
        cl_sh = self.rf_shadowed.predict(pred_shadowed)
        
        classes = []
        for p, b, s in zip(cl_pr, cl_bin, cl_sh):
            if b == 'circles':
                if p == 'sharpeners' or p == 'buttons':
                    classes.append(p)
                elif s == 'sharpeners' or s == 'buttons':
                    classes.append(s)
                else:
                    classes.append(p)
            else:
                values, counts = np.unique([p, b, s], return_counts=True)
                classes.append(values[np.argmax(counts)])
        
        return classes
    
    def fit_transform(self, img):

        shadowed, prepared, masks, bboxes = self.__select_objects_and_apply_filters(img)
    
        pred_shadowed = self.model.predict(shadowed)
        pred_prepared = self.model.predict(prepared)
        pred_masks = self.model.predict(masks)
        
        classes = self.__predict_classes(pred_shadowed, pred_prepared, pred_masks)
        
        return classes, bboxes
        