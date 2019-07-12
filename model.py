# Josh Ryan 2019
# tensorflow CNN model

# Still need to load data into numpy/tensorflow
import numpy as np
import cv2
import sys
import os
import glob
from os import listdir
from os.path import isdir

import matplotlib.pyplot as plt

#import tflearn
# from tflearn.layers.conv import conv_2d, max_pool_2d
# from tflearn.layers.core import input_data, dropout, fully_connected
# from tflearn.layers.estimator import regression


# load data
path = "tmp/spec"

# add directories to list
music_folders = [f for f in glob.glob("tmp/spec/*") if isdir(f)]

training_data = []
for folder in music_folders:
	# print(len(folder))
	class = folder.split('/')[-1]
	print(classifier)
	for song in listdir(folder):
		img_array = cv2.imread(os.path.join(folder,song), cv2.IMREAD_GRAYSCALE)
		plt.imshow(img_array,cmap="gray")
		plt.show()

		# resize to 128 x 128
		img_array = cv2.resize(img_array, (128,128))

		# add image/class pair
		training_data.append([img_array, class])

		break
	break
	print('{}: {}'.format(folder, len(os.listdir(folder))))

sys.exit()

####
# CNN Model
# print("[+] Creating model...")

# convnet = input_data(shape=[None, 70, 128, 1], name='input')

# convnet = conv_2d(convnet, 64, 2, activation='elu', weights_init="Xavier")
# convnet = max_pool_2d(convnet, 2)

# convnet = conv_2d(convnet, 128, 2, activation='elu', weights_init="Xavier")
# convnet = max_pool_2d(convnet, 2)

# convnet = conv_2d(convnet, 256, 2, activation='elu', weights_init="Xavier")
# convnet = max_pool_2d(convnet, 2)

# convnet = conv_2d(convnet, 512, 2, activation='elu', weights_init="Xavier")
# convnet = max_pool_2d(convnet, 2)

# convnet = fully_connected(convnet, 1024, activation='elu')
# convnet = dropout(convnet, 0.5)

# convnet = fully_connected(convnet, 24, activation='softmax')
# convnet = regression(convnet, optimizer='rmsprop', loss='categorical_crossentropy')

# model = tflearn.DNN(convnet)
# print("    Model created! ✅")

# model.fit()

