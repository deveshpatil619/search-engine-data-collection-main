import requests #using the requests library to send HTTP requests to a web API


def test_fetch_api():
    url = "http://localhost:8080/fetch"
    x = requests.get(url) # sends an HTTP GET request to the /fetch endpoint on the local API server and prints the response content.
    print(x.content)


def test_add_label(label): # takes a parameter label.
    res = requests.post("http://localhost:8080/add_label", ##  Send an HTTP POST request to the "add_label" endpoint on the local API server.
                        headers={ 
                            'Content-type': 'application/json' # Set the "Content-type" header of the request 
                            #to "application/json", indicating that the request body will be in JSON format.
                        },
                        json={"label_name": label}, # Set the JSON payload of the request to a dictionary 
# containing a single key-value pair, where the key is "label_name" and the value is the label parameter passed to the function.
                        )
    print(res.content) #Print the content of the response returned by the API server


def test_single_upload(data):#This is a function definition for a test case called test_single_upload. It takes in one parameter called data.
    res = requests.post("http://localhost:8080/single_upload", #  This line creates a POST request to the
            # URL http://localhost:8080/single_upload. The response object is stored in the variable res.
                        headers={ #
                            'Content-type': 'application/json'# Set the "Content-type" header of the request 
                            #to "application/json", indicating that the request body will be in JSON format.
                        },
                        json={"label": "test1", "image": data.decode()}, #This line creates a JSON payload 
#to be sent with the request. The payload includes a label key with the value "test1" and an image key with the value data.decode().
                        )
    print(res.content)#Print the content of the response returned by the API server


def test_bulk_upload(label, data): ## This is defining a Python function called test_bulk_upload that takes two arguments: a label string and a data list of binary image data.
    res = requests.post("http://localhost:8080/bulk_upload", # This is sending an HTTP POST request to the URL http://localhost:8080/bulk_upload.
                        headers={
                            'Content-type': 'application/json' #This is specifying the headers for the HTTP request, which include the content type application/json.
                        },
                        json={"label": label, "images": data}, #  This is specifying the JSON payload for the
                    # HTTP request, which includes the label string and the data list of binary image data.
                        )
    print(res.content) #This is printing the content of the HTTP response, which is returned by the API endpoint at http://localhost:8080/bulk_upload.


# Write your test case here
if __name__ == "__main__":
    test_fetch_api()




    