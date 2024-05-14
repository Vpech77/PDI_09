####################################################
#     Entraînement du modèle Unet                  #
#                   Par l'équipe LostInSwamp       #
####################################################


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
import tensorflow.keras.backend as K
from keras.utils import plot_model
import tensorflow as tf
import glob
import random
#import cv2
from random import shuffle

"""# Dataset"""

def image_generator(files, batch_size = 32, sz = (256, 256)):
    '''
    Parameters
    ----------
    files : list
        ensemble du dataset d'images d'entraînement ou de test.
    batch_size : int, optional
        taille des lots (batch_x et batch_y), nombre d'images/masques par lot.
        The default is 32.
    sz : tuple, optional
        dimensions d'une image en pixels.
        The default is (256, 256).

    Yields
    ------
    batch_x : array
        matrice des images de shape (batch_size, sz[0], sz[1], 3).
        MATRICE 4D ATTENDUE PAR CNN (convolutional neural network)
    batch_y : array
        matrice des masques de shape (batch_size, sz[0], sz[1], 1).
        MATRICE 4D ATTENDUE PAR CNN (convolutional neural network)
    '''

    while True:

      #extract a random batch
      batch = np.random.choice(files, size = batch_size)

      #variables for collecting batches of inputs and outputs
      batch_x = []
      batch_y = []

      for f in batch:
          if f[:5] != ".ipynb" :

                #get the masks. Note that masks are png files
                mask = Image.open(f'./Dataset/annotations/{f[:-4]}_mask.png')
                mask = np.array(mask.resize(sz))

                #preprocess the mask
                mask[mask>0] = 1

                batch_y.append(mask)

                #preprocess the raw images
                raw = Image.open(f'./Dataset/images/{f}')
                raw = raw.resize(sz)
                raw = np.array(raw)
                #check the number of channels because some of the images are RGBA or GRAY
                if len(raw.shape) == 2:
                  raw = np.stack((raw,)*3, axis=-1)
                else:
                  raw = raw[:,:,0:3]

                batch_x.append(raw)

      #preprocess a batch of images and masks
      batch_x = np.array(batch_x)/255
      batch_y = np.array(batch_y)
      batch_y = np.expand_dims(batch_y,3)

      yield (batch_x, batch_y)

batch_size = 16

all_files = os.listdir('./Dataset/images')
shuffle(all_files)

split = int(0.95 * len(all_files))

#split into training and testing
train_files = all_files[0:split]
test_files  = all_files[split:]

train_generator = image_generator(train_files, batch_size = batch_size)
test_generator  = image_generator(test_files, batch_size = batch_size)

x, y= next(train_generator)

plt.axis('off')
img = x[0]
msk = y[0].squeeze()
msk = np.stack((msk,)*3, axis=-1)

plt.imshow(np.concatenate([img, msk, img*msk], axis = 1))

"""# Metric"""

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

"""# Model"""


def unet(sz = (256, 256, 3)):
  '''
    Parameters
    ----------
    sz : tuple
        shape des 'images' (256x256 pixels, 3 canaux RVB).

    Returns
    -------
    model : TYPE
        DESCRIPTION.
    '''
  x = Input(sz)
  inputs = x

  #down sampling
  f = 8
  layers = []

  for i in range(0, 6):
    x = Conv2D(f, 3, activation='relu', padding='same') (x)
    x = Conv2D(f, 3, activation='relu', padding='same') (x)
    layers.append(x)
    x = MaxPooling2D()(x)
    f = f*2
  ff2 = 64

  #bottleneck
  j = len(layers) - 1
  x = Conv2D(f, 3, activation='relu', padding='same') (x)
  x = Conv2D(f, 3, activation='relu', padding='same') (x)
  x = Conv2DTranspose(ff2, 2, strides=(2, 2), padding='same') (x)
  x = Concatenate(axis=3)([x, layers[j]])
  j = j -1

  #upsampling
  for i in range(0, 5):
    ff2 = ff2//2
    f = f // 2
    x = Conv2D(f, 3, activation='relu', padding='same') (x)
    x = Conv2D(f, 3, activation='relu', padding='same') (x)
    x = Conv2DTranspose(ff2, 2, strides=(2, 2), padding='same') (x)
    x = Concatenate(axis=3)([x, layers[j]])
    j = j -1


  #classification
  x = Conv2D(f, 3, activation='relu', padding='same') (x)
  x = Conv2D(f, 3, activation='relu', padding='same') (x)
  outputs = Conv2D(1, 1, activation='sigmoid') (x)

  #model creation
  model = Model(inputs=[inputs], outputs=[outputs])
  model.compile(optimizer = 'rmsprop', loss = 'binary_crossentropy', metrics = [mean_iou])

  return model

model = unet()

"""# Callbacks

"""

df = pd.DataFrame()

def build_callbacks():
        checkpointer = ModelCheckpoint(filepath='unet.weights.h5', verbose=0, save_best_only=True, save_weights_only=True)
        callbacks = [checkpointer, PlotLearning()]
        return callbacks


# inheritance for training process plot
class PlotLearning(keras.callbacks.Callback):

    def on_train_begin(self, logs={}):
        self.i = 0
        self.x = []
        self.losses = []
        self.val_losses = []
        self.acc = []
        self.val_acc = []
        #self.fig = plt.figure()
        self.logs = []
    def on_epoch_end(self, epoch, logs={}, df=df):
        self.logs.append(logs)
        self.x.append(self.i)
        self.losses.append(logs.get('loss'))
        self.val_losses.append(logs.get('val_loss'))
        self.acc.append(logs.get('mean_iou'))
        self.val_acc.append(logs.get('val_mean_iou'))
        self.i += 1

        print('i=',self.i,'loss=',logs.get('loss'),'val_loss=',logs.get('val_loss'),'mean_iou=',logs.get('mean_iou'),'val_mean_iou=',logs.get('val_mean_iou'))

        #choose a random test image and preprocess
        path = np.random.choice(test_files)
        raw = Image.open(f'./Dataset/images/{path}')
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
        plt.savefig(str(self.i)+'.png')
        plt.show()

    def on_train_end(self,logs={}):
      df['nb_epoch'] = self.x
      df['loss'] = self.losses
      df['val_loss'] = self.val_losses
      df['mean_iou'] = self.acc
      df['val_mean_iou'] = self.val_acc
      df.to_csv('df_epochs1_batch8', sep=',', index=False, encoding='utf-8')
      df.plot(x='nb_epoch',y=['loss','val_loss','mean_iou','val_mean_iou'], marker = '.')
      plt.savefig('df_epochs1_batch8.png')



train_steps = len(train_files)//batch_size
print(len(train_files), batch_size, train_steps)
test_steps = len(test_files)//batch_size
model.fit(train_generator,epochs = 10, steps_per_epoch = train_steps,
          validation_data = test_generator, validation_steps = test_steps,
          callbacks = build_callbacks(), verbose = 1)

model.save("model.keras")
