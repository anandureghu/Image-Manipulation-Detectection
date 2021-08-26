from django.shortcuts import render
from app_detector.models import Test
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from django.core.files.base import ContentFile
import cv2
import numpy as np

# Importing libraries
# import argparse
from PIL import Image
from PIL.ExifTags import TAGS
from metadata_dataset import DataSet
import time


success = False
altered = False



# Create your views here.
# Defining a function to get metadata and detect whether is altered or not!
@xframe_options_exempt
def get_meta_data(request, id):

    # Initialising Flags
    

    # Collecting Data from Dataset
    data = DataSet()
    softwares = data.get_data_set()

    image_obj = Test.objects.get(id=id)

    try:
        global altered, success, metadata_found
        altered = False
        success=False
        metaData = {}

        # Reading image
        img = Image.open("media/"+ str(image_obj.image))

        # print("Getting metadata...")
        info = img._getexif()

        

        # img.show()

        # If metadata is collected
        if info:
            metadata_found = True
            # Collecting each elements of metadata
            for (tag, value) in info.items():
                tagname = TAGS.get(tag, tag)
                metaData[tagname] = value
        

            # Saving current image meta data into a data.txt file
            with open("metadata_data/data.txt", 'w') as file:
                for (tagname, value) in metaData.items():

                    # MakerNote is huge line of metadata, if it is printed it will confuse.
                    # So avoiding if MakerNote comes...
                    if str(tagname) != "MakerNote":
                        # time.sleep(.25)
                        # print(str(tagname) + "\t" + str(value))
                        file.write(str(tagname) + "&emsp;&emsp;" + str(value) + "<br>")

                    # Checking if any software is used for editing.
                    if str(tagname) == "Software":

                        # Collecting Software Details Used
                        # Splitting is used to get every keyword ,
                        # so it can iterate through dataset and check each of them
                        software_tag_data = str(value).lower().split()
                        for software_tag in software_tag_data:
                            for software in softwares:

                                # If found any altration exit from loop and set set flag altered is True.
                                if software_tag.lower() == software.lower():
                                    altered = True
                                    image_obj.status = True
                                    image_obj.save()
                                    break
                            if altered == True:
                                break



            # print("\n\nData collected and saved.")
            success = True
        else:
            metadata_found = False
            with open("metadata_data/data.txt", 'w') as file:
                file.write("No Metadata Found!" + "<br>")

    # If no image Data exists.
    except:
        success = False
    #     # print("Failed. Check your image name again!")

    with open("metadata_data/data.txt", 'r') as file:
        metadata = file.read()
    
    image_obj.save()
    

    # validate(id)
    time.sleep(2)

    return render(request, "metadata.html", {"image": image_obj, "metadata":metadata, "altered":altered, "metadata_found":metadata_found})

@xframe_options_exempt
def get_data(request):
    with open("metadata_data/data.txt", 'r') as file:
        metadata = file.read()

    return render(request, "metadata_data.html", {"metadata": metadata})




def validate(id):

    image_obj = Test.objects.get(id=id)

    cvimg = cv2.imread("media/"+ str(image_obj.image))
    cvimg = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)
    height, width, channel = cvimg.shape
    fake = cv2.imread("static/assets/img/fake.png")
    fake = cv2.cvtColor(fake, cv2.COLOR_BGR2RGB)
    real = cv2.imread("static/assets/img/real.png")
    real = cv2.cvtColor(real, cv2.COLOR_BGR2RGB)

    if width > height:
        size = width
    else:
        size = height

    result_size = int(size * .35)

    fake = cv2.resize(fake, (result_size, result_size))
    real = cv2.resize(real, (result_size, result_size))


    x_offset = int(width * .03)
    y_offset = height - x_offset - result_size
    # x_offset = result_size - x_offset

    if image_obj.status:
        result_img = fake.copy()
        # image_obj.status = True
    else:
        result_img = real.copy()
        # image_obj.status = False

    
    gray_img = cv2.cvtColor(result_img, cv2.COLOR_RGB2GRAY)
    img_inv = cv2.bitwise_not(gray_img)
    masked_img = cv2.bitwise_or(result_img, result_img, mask=img_inv)


    
    x_end = x_offset + result_img.shape[1]
    y_end = y_offset + result_img.shape[0]

    roi = cvimg[y_offset:y_end, x_offset:x_end]
    final_roi = cv2.bitwise_or(roi, masked_img)

    large_img = cvimg
    small_img = final_roi
    

    large_img[y_offset:y_offset + result_img.shape[0], x_offset:x_offset + result_img.shape[1]] = small_img

    final_img = cv2.cvtColor(large_img, cv2.COLOR_RGB2BGR)

    # cvimg[y_offset:y_end, x_offset:x_end] = result_img

    ret, buf = cv2.imencode('.jpg', final_img) # cropped_image: cv2 / np array
    content = ContentFile(buf.tobytes())

    image_obj.result_img.save('output.jpg', content)

    image_obj.save()