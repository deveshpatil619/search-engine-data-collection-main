import os
import base64 ##base64 is used for encoding images as text,
from from_root import from_root # from_root is a custom module that provides a function for getting the root directory of the project
from tqdm import tqdm #tqdm is used to display progress bars for long-running tasks.


# Upload data using boto3 [ Takes a lot of time ]
def upload_bulk_data(root="caltech-101"): ## defines a function called upload_bulk_data that 
#takes an optional argument root that defaults to "caltech-101". This function will be used to upload image data to a cloud service.
    labels = os.listdir(root) #  to get a list of all directories in the root directory, which 
#will correspond to the different image categories (e.g. "airplanes", "butterfly", etc.). These directories will be used as labels for the images.
    for label in tqdm(labels): #line starts a loop over each label directory, using tqdm to display a progress bar for the loop.
        data = [] # list called data
        images = os.listdir(root + "/" + label) #module to get a list of all files (i.e., images) in the directory specified by root and label
        for img in tqdm(images): # loop over each image in the images list, using tqdm to display a progress bar for the loop.
            path = os.path.join(from_root(), root, label, img) ## line constructs a path to the current image file using the os.path.join() method. The resulting path is assigned to the path variable.
            with open(rf'{path}', "rb") as img: ## opens the file specified by the path variable in binary mode using the built-in open() function. The resulting file object is assigned to the img variable.
                data.append(base64.b64encode(img.read()).decode())## line reads the binary data
#from the img file object using the read() method, encodes the data using the base64.b64encode()
#method, and then decodes the resulting bytes-like object to a string using the decode() method.
# The resulting string is then appended to the data list. This process of reading and encoding 
# each image file will continue until all images have been processed by the loop.

    print("/nCompleted")


upload_bulk_data(root="caltech-101")
