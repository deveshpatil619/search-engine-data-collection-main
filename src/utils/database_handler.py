##The code imports pymongo library to interact with MongoDB database, os library to get environment 
#variables, and urllib.parse to encode the username and password.

import pymongo
import os
import urllib.parse


class MongodbClient:
    client = None ##  class variable client set to None

    def __init__(self, database_name=os.getenv("DATABASE_NAME")) -> None: 

        """The code defines an initializer method for the MongodbClient class, which takes the
        database_name as an argument, and it is set to the environment variable DATABASE_NAME.
        The code encodes the username and password using urllib.parse.quote_plus() method."""

        username = urllib.parse.quote_plus(os.getenv('ATLAS_CLUSTER_USERNAME'))
        password = urllib.parse.quote_plus(os.getenv('ATLAS_CLUSTER_PASSWORD'))

        if MongodbClient.client is None: #The code checks if the client is already created or not. 
            MongodbClient.client = pymongo.MongoClient( ##If it's not created, it creates a new 
#pymongo.MongoClient object by passing the MongoDB Atlas cluster URL, username, and password as arguments.
                "mongodb+srv://{}:{}@cluster0.s8lbkcs.mongodb.net/?retryWrites=true&w=majority".format(username,password)
            )
        self.client = MongodbClient.client ##The code sets the client and database properties 
        self.database = self.client[database_name] ## of the class to the client object and the 
        self.database_name = database_name ##database_name passed to the initializer, respectively.

     
        collection = self.database[database_name] ##The code creates a new collection object by specifying the collection name my_collection
        print(collection.count_documents({})) # Count the number of documents in the collection




