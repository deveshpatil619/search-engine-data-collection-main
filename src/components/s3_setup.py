"""os and sys are imported for handling operating system related tasks."""
import os 
import sys
from zipfile import ZipFile # Class with methods to open, read, write, close, list zip files.
import shutil #Utility functions for copying and archiving files and directory trees.
from src.exception import CustomException   ## importing the custom exceptions
from from_root import from_root  ## to get the root girectory of working project

# https://www.kaggle.com/datasets/imbikramsaha/caltech-101 [ Get data from kaggle and put it into data folder ]

class DataStore: ## this datastore class that contains methods to prepare and sync image data
    def __init__(self):
        self.root = os.path.join(from_root(), "data")##  This sets the root attribute to the current working directory joined with a subdirectory named "data".
        self.zip = os.path.join(self.root, "archive.zip") ## This sets the images attribute to the root directory 'data' joined with a subdirectory named "archive.zip".
        self.images = os.path.join(self.root, "caltech-101") ## This sets the images attribute to the root directory 'data' joined with a subdirectory named "caltech-101".
        self.list_unwanted = ["BACKGROUND_Google"]#self.list_unwanted is a list containing a single string element "BACKGROUND_Google"
##The purpose of this list is to hold the names of classes that should be removed from the dataset during 
# data preparation. In the remove_unwanted_classes() method, this list is iterated over and each class is removed
#  from the dataset using the shutil.rmtree() function.

    def prepare_data(self): ##This method is used to extract the image data from a zip file located at self.zip.
        try:
            print(" Extracting Data ") ## displaying message Extracting Data
            with ZipFile(self.zip, 'r') as files: ## Open the ZIP file "archive.zip" with mode read 'r'
                files.extractall(path=self.root)# extracts all files and directories from the zip archive to the directory specified by self.root.

            files.close() #closes the zip file.
            print(" Process Completed ")
        except Exception as e:
            message = CustomException(e, sys)
            return {"Created": False, "Reason": message.error_message} ## This returns a dictionary with a 
        #Created key set to False and a Reason key set to the error message.

    def remove_unwanted_classes(self): #This code defines a method called remove_unwanted_classes that removes unwanted classes from a set of images stored in a directory.
        try:
            print(" Removing unwanted classes ")
            for label in self.list_unwanted: ## for loop that iterates over the labels in self.list_unwanted, which is a list of class names that should be removed.
                path = os.path.join(self.images,label) #This line constructs the path to the directory that contains the images for the current label by joining the self.images directory and the current label.
                shutil.rmtree(path, ignore_errors=True) #This line removes the directory specified by path using
#the rmtree function from the shutil module. The ignore_errors parameter is set to True, which will cause any errors to be ignored if they occur during the removal process.
            print(" Process Completed ")
        except Exception as e:
            message = CustomException(e, sys)
            return {"Created": False, "Reason": message.error_message}## This returns a dictionary with a 
        #Created key set to False and a Reason key set to the error message.

    def sync_data(self):#This method is used to sync the image data to an AWS S3 bucket.
        try:
            print("\n====================== Starting Data sync ==============================\n")
            os.system(f"aws s3 sync { self.images } s3://search-image619/images/") # Executes a shell command using 
#the os.system function to sync data from a local directory (self.images) to an Amazon S3 bucket (s3://search-image619/images/).
#  The aws s3 sync command is a command-line tool provided by the AWS CLI for syncing files and directories between local and S3 storage.
            print("\n====================== Data sync Completed ==========================\n")

        except Exception as e:
            message = CustomException(e, sys)
            return {"Created": False, "Reason": message.error_message}## This returns a dictionary with a 
        #Created key set to False and a Reason key set to the error message.

    def run_step(self): #This method runs the prepare_data(), remove_unwanted_classes(), and sync_data() methods in sequence.
        try:
            self.prepare_data()
            self.remove_unwanted_classes()
            self.sync_data()
            return True
        except Exception as e:
            message = CustomException(e, sys)
            return {"Created": False, "Reason": message.error_message}


if __name__ == "__main__":
    store = DataStore() ##creates an instance of the DataStore class and calls the run_step() method on it. 
    store.run_step() #This initiates the preparation and syncing of the image data.
