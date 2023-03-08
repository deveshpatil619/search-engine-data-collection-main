"""os and sys are imported for handling operating system related tasks."""
import os
import sys
from src.utils.database_handler import MongodbClient  ## importing the MongodbClient class 
from src.exception import CustomException   ## importing the CustomException class
from from_root import from_root ## to get the root girectory of working project

class MetaDataStore: ## MetaDataStore is the class that provides the methods to store the metadata information about image-data

    def __init__(self):
        self.root = os.path.join(from_root(), "data") ##  This sets the root attribute to the current working directory joined with a subdirectory named "data".
        self.images = os.path.join(self.root, "caltech-101") ## This sets the images attribute to the root directory 'data' joined with a subdirectory named "caltech-101".
        self.labels = os.listdir(self.images) # This sets the labels attribute to the list of filenames in the images directory.
        self.mongo = MongodbClient() # This sets the mongo attribute to an instance of the MongodbClient class.

    def register_labels(self): # This method is used to register the labels associated with the image data in the database.
        try:
            records = {} #This creates an empty dictionary to hold the label records.
            for num, label in enumerate(self.labels): # This iterates over the labels attribute, assigning each label to the label variable and a unique number to the num variable.
                records[f"{num}"] = label #  This adds the label to the records dictionary using the unique number as the key.

            existing_records = self.mongo.database['labels'].find_one(records) ## to check if the records already exists in the database and avoid the duplication
            
            if existing_records is None: ## if no duplicates found in database
                self.mongo.database['labels'].insert_one(records) ## This inserts the records dictionary into the labels collection of the MongoDB database.

            else:
            # Duplicate records found, do not insert and print error message
                print("Duplicate records found, skipping insertion.")
        

        except Exception as e:
            message = CustomException(e, sys)
            return {"Created": False, "Reason": message.error_message} ##  This returns a dictionary with a 
        #Created key set to False and a Reason key set to the error message.

    def run_step(self): #This method is used to run a step in the image data processing pipeline.
        try:
            self.register_labels() #This calls the register_labels() method to register the labels associated with the image data.
        except Exception as e:
            message = CustomException(e, sys)
            return {"Created": False, "Reason": message.error_message} # ##  This returns a dictionary with a 
        #Created key set to False and a Reason key set to the error message.


if __name__ == "__main__":
    meta = MetaDataStore() ##  The meta variable creates an instance of this class.
    meta.run_step() ##The meta.run_step() method is then called on this instance.






