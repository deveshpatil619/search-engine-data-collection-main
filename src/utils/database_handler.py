import pymongo
import os
import urllib.parse


class MongodbClient:
    client = None

    def __init__(self, database_name=os.environ["DATABASE_NAME"]) -> None:
        #username = urllib.parse.quote_plus(os.environ['ATLAS_CLUSTER_USERNAME'])
        #password = urllib.parse.quote_plus(os.environ['ATLAS_CLUSTER_PASSWORD'])
        if MongodbClient.client is None:
            MongodbClient.client = pymongo.MongoClient(
                "mongodb://localhost:27017"
            )
        self.client = MongodbClient.client
        self.database = self.client[database_name]
        self.database_name = database_name

        # Count the number of documents in the collection
        collection = self.database["my_collection"]
        print(collection.count_documents({}))



