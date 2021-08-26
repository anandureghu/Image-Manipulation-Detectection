from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten, Activation, Dropout
from keras.layers import Dense
from keras.layers import Dropout
from keras.models import load_model

import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')


# initialising CNN

classifier = Sequential()

# Convolution
classifier.add(Convolution2D(32, (3,3),input_shape = (150,150,3), activation = 'relu'))
# Pooling
classifier.add(MaxPooling2D(2,2))

# 2nd Convolution

classifier.add(Convolution2D(64,(3,3), activation = 'relu'))

# 2nd pooling

classifier.add(MaxPooling2D(2,2))

# 3rd Convolution
classifier.add(Convolution2D(64, (3,3), activation = 'relu'))

# 3rd pooling

classifier.add(MaxPooling2D(2,2))

#Flatten for FC

classifier.add(Flatten())

# Full connections

"""
output_dim = 128, activation = 'relu'
classifier.add(Dense( output_dim = 1, activation = 'sigmoid'))
"""

classifier.add(Dense(128))
classifier.add(Activation("relu"))

classifier.add(Dropout(0.5))

classifier.add(Dense(1))
classifier.add(Activation("sigmoid"))


# Compiling the CNN

classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

# Fitting the CNN to the images

from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=False,
        vertical_flip=True)

test_datagen = ImageDataGenerator(rescale=1/255)

# training set

training_set = train_datagen.flow_from_directory(
        'DATASET/train',
        target_size=(150, 150),
        batch_size=15,
        class_mode='binary')
# Test_set
test_set= test_datagen.flow_from_directory(
        'DATASET/test',
        target_size=(150, 150),
        batch_size=15,
        class_mode='binary')

result = classifier.fit_generator(
        training_set,
        steps_per_epoch=10,
        epochs=10,
        validation_data=test_set,
        validation_steps=10)

# print(result.history['acc'])
# plt.plot(result.history['acc'])

classifier.save('classifier-vv-model1.h5')