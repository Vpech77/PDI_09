# -*- coding: utf-8 -*-
####################################################
# Test du modèle sur de vraies images              #
# Par l'équipe LostInSwamp                         #
####################################################

##################### Import des librairies #####################
import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image
import keras
from keras import backend as K
import tensorflow as tf

##################### Variables à définir #####################
MODEL_NAME = 'unet_32batch_30epoch'
IMG_TEST_NAME = '2006'

##################### Variables #####################
PATH_IMG_TEST = "./imgCartesAnciennes/" + IMG_TEST_NAME
PATH_MODEL_FILE = "./model/" + MODEL_NAME + ".keras"
PATH_OUTPUT = "./output_testing/" + MODEL_NAME

def mean_iou(y_true, y_pred):
    '''
    Parameters
    ----------
    y_true : TYPE
        masque réel.
    y_pred : TYPE
        masque prédit.

    Returns
    -------
    iou : TYPE
        intersection over union metric.
    '''
    yt0 = y_true[:,:,:,0]
    yp0 = K.cast(y_pred[:,:,:,0] > 0.5, 'float32')
    inter = tf.math.count_nonzero(tf.logical_and(tf.equal(yt0, 1), tf.equal(yp0, 1)))
    union = tf.math.count_nonzero(tf.add(yt0, yp0))
    iou = tf.where(tf.equal(union, 0), 1., tf.cast(inter/union, 'float32'))
    return iou

if __name__ == "__main__":

    model = keras.models.load_model(PATH_MODEL_FILE, custom_objects={"mean_iou": mean_iou})
    test = os.listdir(PATH_IMG_TEST)
    os.makedirs(PATH_OUTPUT)

    cpt=1
    for image in test :
        path = os.path.join(PATH_IMG_TEST, image)
        raw = Image.open(path)
        raw = np.array(raw.resize((256, 256)))/255.
        raw = raw[:,:,0:3]

        #predict the mask
        pred = model.predict(np.expand_dims(raw, 0))

        #mask post-processing
        msk  = pred.squeeze()
        msk = np.stack((msk,)*3, axis=-1)
        msk[msk >= 0.5] = 1
        msk[msk < 0.5] = 0

        #show the mask and the segmented image
        combined = np.concatenate([raw, msk, raw* msk], axis = 1)
        plt.axis('off')
        plt.imshow(combined)
        plt.savefig(PATH_OUTPUT+'/cartes_'+IMG_TEST_NAME+'_'+MODEL_NAME+str(cpt)+'.png')
        cpt+=1

