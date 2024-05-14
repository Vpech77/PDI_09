import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from PIL import Image
import keras
from keras.models import Model
from keras.layers import Conv2D, MaxPooling2D, Input, Conv2DTranspose, Concatenate, BatchNormalization, UpSampling2D
from keras.layers import  Dropout, Activation
from keras.optimizers import Adam, SGD
from keras.layers import LeakyReLU
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, EarlyStopping
from keras import backend as K
from keras.utils import plot_model
import tensorflow as tf
import glob
import random
from random import shuffle
import sys
np.set_printoptions(threshold=sys.maxsize)

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

MODEL_NAME = 'unet_32batch_30epoch'
IMG_TEST_FOLDER = '2006'

if __name__ == "__main__":

    dossier_git = 'model'

    if os.path.isdir(dossier_git):
        contenu_dossier = os.listdir(dossier_git)
        print(contenu_dossier)
    else:
        print("nope")

    # model = keras.models.load_model('unet_32batch_30epoch.keras', custom_objects={"mean_iou": mean_iou})
    test = os.listdir(IMG_TEST_FOLDER)
    # i=1
    for image in test :
        path = os.path.join("./imgCartesAnciennes"+IMG_TEST_FOLDER, image)
        raw = Image.open(path)
        raw = np.array(raw.resize((256, 256)))/255.
        raw = raw[:,:,0:3]
        print(raw)

    #     #predict the mask
    #     pred = model.predict(np.expand_dims(raw, 0))

    #     #mask post-processing
    #     msk  = pred.squeeze()
    #     msk = np.stack((msk,)*3, axis=-1)
    #     msk[msk >= 0.5] = 1
    #     msk[msk < 0.5] = 0

    #     #show the mask and the segmented image
    #     combined = np.concatenate([raw, msk, raw* msk], axis = 1)
    #     plt.axis('off')
    #     plt.imshow(combined)
    #     plt.savefig('./imgCartesAnciennes/'+MODEL_NAME+str(i)+'.png')
    #     #plt.show()
    #     i+=1

