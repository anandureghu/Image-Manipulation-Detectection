# Creating a class to access data set in main.py
class DataSet:

    # Defining function to collect data from data set and remove "\n"
    def get_data_set(self):

        # Initializing a list to save the software list
        softwares = []

        # Opening Data set for collecting data
        with open('metadata_data/dataset.txt', 'r') as file:

            # Iterating through each element and replacing "\n"
            for item in file:
                if "\n" in item:
                    item = item.replace("\n", "")

                # Adding all element to software list
                softwares.append(item)

        return softwares
