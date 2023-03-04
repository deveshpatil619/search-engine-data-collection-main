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


# code defines a POST endpoint /add_label/{label_name} that allows a user to add a new label to a collection
#  of labels stored in a MongoDB database and in an S3 bucket.
@app.post("/add_label/{label_name}") ##  line uses the @app.post decorator to associate the add_label function
#with the /add_label/{label_name} endpoint. This endpoint expects a POST request with a URL parameter 
# label_name, which is a string representing the name of the new label to be added.
def add_label(label_name: str):
    result = mongo.database['labels'].find() # line fetches all the documents from the MongoDB database 
#collection 'labels' using the find method and assigns the resulting cursor object to result.
    documents = [document for document in result] #list comprehension to iterate over the cursor object result and convert the documents to a list of dictionaries, documents.
    last_value = list(map(int, list(documents[0].keys())[1:]))[-1] #This line gets the last key in the
#dictionary stored in the first document in the documents list. This key represents the index of the last 
# label in the collection. It does this by converting all the keys to integers, taking only the keys after 
# the first key (which is the "_id" key), and then taking the last key in that list.
    response = mongo.database['labels'].update_one({"_id": documents[0]["_id"]},{"$set": {str(last_value + 1): label_name}}) #This line updates 
#the MongoDB document with the new label. It does this by calling the update_one method on the 'labels' 
# collection with a filter to find the document with the same _id as the first document in documents, and 
# a $set update operator to add a new key-value pair to the dictionary stored in that document. 
# The key is str(last_value + 1) (i.e., the index of the new label), and the value is the label_name.
    if response.modified_count == 1: #This line checks if the MongoDB update was successful by verifying that exactly one document was modified.
        response = s3.add_label(label_name) #This line calls the add_label method of the s3 object to add the new label to the S3 bucket.
        return {"Status": "Success", "S3-Response": response} #line returns a dictionary indicating that the new label was successfully added to both the MongoDB database and the S3 bucket.
    else:
        return {"Status": "Fail", "Message": response[1]}#This line returns a dictionary indicating that the update failed and includes the error message.


@app.get("/single_upload/") #This is a decorator that registers a GET endpoint with the specified URL path "/single_upload/".
def single_upload():# defines a function called single_upload that will handle the GET request.
    info = {"Response": "Available", "Post-Request-Body": ["label", "Files"]} #creates a dictionary object called
#info with two keys and values. The "Response" key has the value "Available", and the "Post-Request-Body" key has a list of two strings, "label" and "Files".
    return JSONResponse(content=info, status_code=200, media_type="application/json") #eturns a JSONResponse object 
#with the content set to the info dictionary, a status code of 200, and a media type of "application/json". The response will contain the info dictionary as a JSON object.


# Image Single Upload Api
@app.post("/single_upload/") ##decorator that registers a POST endpoint with the specified URL path "/single_upload/".
async def single_upload(label: str, file: UploadFile = None): #defines an asynchronous function called single_upload that takes two parameters: label as a string and file as an optional UploadFile object.
    label = choices.get(label, False) #retrieves the label for the given label parameter from the global choices dictionary, or sets label to False if the label is not found.
    if file.content_type == "image/jpeg" and label != False: #checks if the content_type of the uploaded file is "image/jpeg" and if a label was found for the given label parameter.
        response = s3.upload_to_s3(file.file, label) #uploads the file to Amazon S3 using the upload_to_s3 method of the s3 object, passing in the file object and the label as arguments.
        return {"filename": file.filename, "label": label, "S3-Response": response}# returns a dictionary containing the filename of the uploaded file, the label, and the response from the S3 upload.
    else:
        return {
            "ContentType": f"Content type should be Image/jpeg not {file.content_type}", # returns a dictionary 
            "LabelFound": label,# with an error message indicating that the content type of the uploaded file should be "image/jpeg",
        }        # and the label found (or False if no label was found) for the given label parameter.


@app.get("/bulk_upload")# decorator that registers a GET endpoint with the specified URL path "/bulk_upload".
def bulk_upload(): #
    info = {"Response": "Available", "Post-Request-Body": ["label", "Files"]} #creates a dictionary called info with
#two keys: "Response" and "Post-Request-Body". The value of "Response" is "Available", and the value of "Post-Request-Body" is a list containing the strings "label" and "Files".
    return JSONResponse(content=info, status_code=200, media_type="application/json") ##eturns a JSONResponse object 
#with the content set to the info dictionary, a status code of 200, and a media type of "application/json". The response will contain the info dictionary as a JSON object.



# Transforms here
@app.post("/bulk_upload") ####decorator that registers a POST endpoint with the specified URL path "/bulk_upload".
def bulk_upload(label: str, files: List[UploadFile] = File(...)): #defines the bulk_upload function, which takes in 
#two parameters: label and files. The label parameter is a string that represents the label to apply to the uploaded
# files. The files parameter is a list of UploadFile objects, which represent the files to upload.
    try:
        skipped = [] ## creating empty list skipped that will store any files that were skipped during the upload process
        final_response = None #final_response is None for now but will later store the final response from the S3 upload.
        label: Union[bool, Any] = choices.get(label, False) #retrieves the label from the choices dictionary using 
#the get method. If the label is found, it is stored in the label variable. If the label is not found, False is stored in label.
        if label: #checks if label is truthy. If it is, the code inside the if block is executed. If it is not, the code inside the else block is executed.
            for file in files: # loop that iterates over each file in the files list.
                if file.content_type == "image/jpeg": # if the content type of the current file is "image/jpeg". If it is, the code inside the if block is executed. If it is not, the code inside the else block is executed.
                    response = s3.upload_to_s3(file.file, label)#uploads the file to Amazon S3 using the upload_to_s3 method of the s3 object, passing in the file object and the label as arguments.
                    final_response = response #. The response from the upload is stored in the response variable, and then copied to the final_response variable.
                else:
                    skipped.append(file.filename) ##adds the filename of the current file to the skipped list because its content type is not "image/jpeg".
            return { # returns a dictionary containing information about the upload process.
                "label": label, # The label key contains the label that was applied to the uploaded files.
                "skipped": skipped, # The skipped key contains a list of filenames that were skipped during the upload process.
                "S3-Response": final_response, # The S3-Response key contains the final response from the S3 upload.
                "LabelFound": label, #The LabelFound key contains the value of the label variable, which is either
                 # the label that was found in the choices dictionary or False.
            }
        else:
            return {
                "label": label,
                "skipped": skipped,
                "S3-Response": final_response,
                "LabelFound": label,
            }
    except Exception as e:
        return {"ContentType": f"Content type should be Image/jpeg not {e}"} #The exception is assigned to the 
    #variable e, and a JSON response is returned with the error message that includes the exception.


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080) #the specified host and port (in this case, 0.0.0.0:8080).
#This block ensures that the server is only started when the script is run directly, and not when it is imported as a module.
