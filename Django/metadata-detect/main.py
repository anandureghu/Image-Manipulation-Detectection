# import os
# try:
#     os.system('cls')
# except:
#     os.system('clear')

# heading = """
# ██╗███╗░░░███╗░█████╗░░██████╗░███████╗
# ██║████╗░████║██╔══██╗██╔════╝░██╔════╝
# ██║██╔████╔██║███████║██║░░██╗░█████╗░░
# ██║██║╚██╔╝██║██╔══██║██║░░╚██╗██╔══╝░░
# ██║██║░╚═╝░██║██║░░██║╚██████╔╝███████╗
# ╚═╝╚═╝░░░░░╚═╝╚═╝░░╚═╝░╚═════╝░╚══════╝
# ░█████╗░██╗░░░░░████████╗██████╗░░█████╗░████████╗██╗░█████╗░███╗░░██╗
# ██╔══██╗██║░░░░░╚══██╔══╝██╔══██╗██╔══██╗╚══██╔══╝██║██╔══██╗████╗░██║
# ███████║██║░░░░░░░░██║░░░██████╔╝███████║░░░██║░░░██║██║░░██║██╔██╗██║
# ██╔══██║██║░░░░░░░░██║░░░██╔══██╗██╔══██║░░░██║░░░██║██║░░██║██║╚████║
# ██║░░██║███████╗░░░██║░░░██║░░██║██║░░██║░░░██║░░░██║╚█████╔╝██║░╚███║
# ╚═╝░░╚═╝╚══════╝░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░╚═╝░╚════╝░╚═╝░░╚══╝
# ██████╗░███████╗████████╗███████╗░█████╗░████████╗░█████╗░██████╗░
# ██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗
# ██║░░██║█████╗░░░░░██║░░░█████╗░░██║░░╚═╝░░░██║░░░██║░░██║██████╔╝
# ██║░░██║██╔══╝░░░░░██║░░░██╔══╝░░██║░░██╗░░░██║░░░██║░░██║██╔══██╗
# ██████╔╝███████╗░░░██║░░░███████╗╚█████╔╝░░░██║░░░╚█████╔╝██║░░██║
# ╚═════╝░╚══════╝░░░╚═╝░░░╚══════╝░╚════╝░░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝\n\n"""
# print(heading)

# Importing libraries
# import argparse
from PIL import Image
from PIL.ExifTags import TAGS
from metadata_dataset import DataSet
import time

# Initialising Flags
success = False
altered = False

# Collecting Data from Dataset
data = DataSet()
softwares = data.get_data_set()


# Defining a function to get metadata and detect whether is altered or not!
def get_meta_data(img):

    # Declaring Gobal Flags
    global altered, success
    try:
        metaData = {}

        # Reading image
        img = Image.open(f"Images/{img}")
        # print("Getting metadata...")
        info = img._getexif()

        # If metadata is collected
        if info:
            print("Found metadata")

            # Collecting each elements of metadata
            for (tag, value) in info.items():
                tagname = TAGS.get(tag, tag)
                metaData[tagname] = value
            #     if not out:
            #         print(tagname, value)
            # if out:
            #     print("Outputing to file...")
            #     with open(out, 'w') as file:
            #         for (tagname, value) in metaData.items():
            #             file.write(str(tagname)+"\t"+str(value)+"\n")

            # Saving current image meta data into a data.txt file
            print("Outputing to file...\n\n")
            with open("Data/data.txt", 'w') as file:
                for (tagname, value) in metaData.items():

                    # MakerNote is huge line of metadata, if it is printed it will confuse.
                    # So avoiding if MakerNote comes...
                    if str(tagname) != "MakerNote":
                        time.sleep(.25)
                        print(str(tagname) + "\t" + str(value))
                        file.write(str(tagname) + "\t" + str(value) + "\n")

                    # Checking if any software is used for editing.
                    if str(tagname) == "Software":

                        # Collecting Software Details Used
                        # Splitting is used to get every keyword ,
                        # so it can iterate through dataset and check each of them
                        software_tag_data = str(value).lower().split()
                        for software_tag in software_tag_data:
                            for software in softwares:

                                # If found any altration exit from loop and set set flag altered is True.
                                if software_tag == software.lower():
                                    altered = True
                                    break
                            if altered == True:
                                break



            print("\n\nData collected and saved.")
            success = True

    # If no image Data exists.
    except:
        success = False
        print("Failed. Check your image name again!")

    if altered == True:
        return True
    else:
        return False


# To give instructions from command line

# def Main():
#     parser = argparse.ArgumentParser()
#     parser.add_argument("img", help="name of an image file")
#     parser.add_argument("--output", "-o", help="dump data out to file")
#     args = parser.parse_args()
#     if args.img:
#         get_meta_data(args.img, args.output)
#     else:
#         print(parser.usage)


if __name__ == "__main__":

    # To give instructions from command line
    # Main()

    # Getting image and passing it to the function to check
    img = input("Enter the image name: ")
    altered = get_meta_data(img)
    if success:
        print("Finished...\n\n")

        if altered:
            result = "The Image is Altered!"
        else:
            result = "The Image is Not Altered!"

        # Printing Result
        result_len = len(result)
        print(f"\n+{'-' * (result_len + 6)}+")
        print(f"|{' ' * (6//2) }{result}{' ' * (6//2) }|")
        print(f"+{'-' * (result_len + 6)}+\n\n")