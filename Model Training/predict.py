import os
path=os.getcwd()
os.chdir(path)
print(path)
import numpy as np
from keras.preprocessing import image
from keras.models import load_model



#Load Model
model = load_model('classifier-vv-model1.h5')

#Compile
model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

test_image = image.load_img("DATASET/test/NOT_FAKE/real_00012.jpg", target_size = (150, 150))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis = 0)

classes = model.predict_classes(test_image)
print(classes)

if classes[0][0] == 0:
    prediction = 'Real'
else:
    prediction = 'Fake'
    
print(prediction)
prediction_rate = int((model.predict(test_image)[0][0]) * 100)
print(f"The model is {prediction_rate}% sure!")

