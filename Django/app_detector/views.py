from django.db import reset_queries
import numpy as np
from keras.preprocessing import image
from keras.models import load_model
from PIL import Image
import os
path=os.getcwd()
os.chdir(path)
#Load Model
model = load_model('classifier-vv-model1.h5')
#Compile
model.compile(loss='binary_crossentropy',
            optimizer='adam',
            metrics=['accuracy'])

from django.shortcuts import redirect, render
from.models import Test

# Create your views here.
def home(request):
    images = Test.objects.all()
    images.delete()
    for image in images:
        image.delete()
    # if request.method == 'POST':
    #     images = Test()
    #     if len(request.FILES) != 0:
    #         images.image = request.FILES.get('img')
    #     images.save()
    #     return render(request, 'index.html', {"image":images})
    return render(request, 'index.html')

def validate(request, id):
    image_obj = Test.objects.get(id=id)

    img = "media/"+ str(image_obj.image)

    # img = Image.open(img)
    # img.show()
    test_image = image.load_img(img, target_size = (150, 150))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis = 0)

    classes = model.predict_classes(test_image)

    if classes[0][0] == 0:
        prediction = 'Real'
    else:
        prediction = 'Fake'

    prediction_rate = int((model.predict(test_image)[0][0]) * 100)

    if prediction_rate > 70:
        color_theme = "success"
    elif prediction_rate > 40:
        color_theme = "warning"
    else:
        color_theme = "danger"


    return render(request, 'ai.html', {"prediction":prediction, "prediction_rate":prediction_rate, "image":image_obj, "color_theme": color_theme})


def upload(request):
    images = Test.objects.all()
    # images.delete()
    for image in images:
        image.delete()
    
    if request.method == 'POST':
        images = Test()
        if len(request.FILES) != 0:
            images.image = request.FILES.get('img')
        images.save()
        return render(request, 'upload.html', {"image":images})
    return render(request, "upload.html")

def upload_with_image(request, id):
    image = Test.objects.get(id=id)
    return render(request, 'upload.html', {"image":image})


