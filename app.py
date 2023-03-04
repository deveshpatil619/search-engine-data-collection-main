from src.utils.database_handler import MongodbClient ## importing the MongodbClient
from src.utils.s3_handler import S3Connection  ## importing the S3Connection
from fastapi import FastAPI, File, UploadFile ## File and UploadFile are used to handle file uploads
from fastapi.responses import JSONResponse # JSONResponse is used to send JSON responses.
from typing import List, Union, Any #  imports the List, Union, and Any These classes are used to define the
#types of arguments and return values for functions and methods.
#List: is used to indicate that the argument or return value should be a list of a specific type. For example, List[int] would indicate a list of integers.
#Union: is used to indicate that the argument or return value can be one of several possible types. For example, Union[int, str] would indicate that the value can be either an integer or a string.
#Any: is used to indicate that the argument or return value can be of any type. This is useful when the type of the value is not known or not important.

import uvicorn ## imports the uvicorn module, which is a lightning-fast ASGI 
#(Asynchronous Server Gateway Interface) server implementation that can be used to run Python web applications, including those built with FastAPI.
#uvicorn provides several features, including auto-reloading for code changes, WebSocket support, and support for HTTP/2, among others. It is a popular choice for deploying FastAPI applications to production environments.

## this is an api connection code to run the endpoints

app = FastAPI(title="DataCollection-Server") #creates an instance of the FastAPI class and assigns it to the app variable. The title parameter is used to set the title of the API.
mongo = MongodbClient() ##  initialize instances of two different classes, MongodbClient and S3Connection
s3 = S3Connection()

choices = {} ## empty dictionary


# Fetch All Labels
@app.get("/fetch")  ## It will get the request from fetch endpoint and call method fetch_label()
def fetch_label():   ##  function retrieves data from a MongoDB database and assigns it to the choices dictionary.
    try:
        global choices ##This line declares that the choices variable is a global variable, so it can be accessed and modified inside the function.
        result = mongo.database['labels'].find() ## line retrieves all documents in the labels collection of the MongoDB database connected to the mongo instance.
        documents = [document for document in result] # creates a list of documents by iterating over the documents fetched from labels collection
        choices = dict(documents[0]) ##  line assigns the first document in the documents list to the choices dictionary as key-value pairs.
        response = {"Status": "Success", "Response": str(documents[0])} #line creates a dictionary called
# response with a "Status" key set to "Success" and a "Response" key set to the string representation of the first document in the documents list.
        return JSONResponse(content=response, status_code=200, media_type="application/json")# returns a 
#JSONResponse object with the response dictionary as its content, a success status code of 200, and a media type of "application/json".
    except Exception as e:
        raise e


# Label Post Api
@app.post("/add_label/{label_name}")
def add_label(label_name: str):
    result = mongo.database['labels'].find()
    documents = [document for document in result]
    last_value = list(map(int, list(documents[0].keys())[1:]))[-1]
    response = mongo.database['labels'].update_one({"_id": documents[0]["_id"]},
                                                   {"$set": {str(last_value + 1): label_name}})
    if response.modified_count == 1:
        response = s3.add_label(label_name)
        return {"Status": "Success", "S3-Response": response}
    else:
        return {"Status": "Fail", "Message": response[1]}


@app.get("/single_upload/")
def single_upload():
    info = {"Response": "Available", "Post-Request-Body": ["label", "Files"]}
    return JSONResponse(content=info, status_code=200, media_type="application/json")


# Image Single Upload Api
@app.post("/single_upload/")
async def single_upload(label: str, file: UploadFile = None):
    label = choices.get(label, False)
    if file.content_type == "image/jpeg" and label != False:
        response = s3.upload_to_s3(file.file, label)
        return {"filename": file.filename, "label": label, "S3-Response": response}
    else:
        return {
            "ContentType": f"Content type should be Image/jpeg not {file.content_type}",
            "LabelFound": label,
        }


@app.get("/bulk_upload")
def bulk_upload():
    info = {"Response": "Available", "Post-Request-Body": ["label", "Files"]}
    return JSONResponse(content=info, status_code=200, media_type="application/json")


# Transforms here
@app.post("/bulk_upload")
def bulk_upload(label: str, files: List[UploadFile] = File(...)):
    try:
        skipped = []
        final_response = None
        label: Union[bool, Any] = choices.get(label, False)
        if label:
            for file in files:
                if file.content_type == "image/jpeg":
                    response = s3.upload_to_s3(file.file, label)
                    final_response = response
                else:
                    skipped.append(file.filename)
            return {
                "label": label,
                "skipped": skipped,
                "S3-Response": final_response,
                "LabelFound": label,
            }
        else:
            return {
                "label": label,
                "skipped": skipped,
                "S3-Response": final_response,
                "LabelFound": label,
            }
    except Exception as e:
        return {"ContentType": f"Content type should be Image/jpeg not {e}"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
