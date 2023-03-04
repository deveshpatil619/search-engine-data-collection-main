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


def test_single_upload(data):
    res = requests.post("http://localhost:8080/single_upload",
                        headers={
                            'Content-type': 'application/json'
                        },
                        json={"label": "test1", "image": data.decode()},
                        )
    print(res.content)


def test_bulk_upload(label, data):
    res = requests.post("http://localhost:8080/bulk_upload",
                        headers={
                            'Content-type': 'application/json'
                        },
                        json={"label": label, "images": data},
                        )
    print(res.content)


# Write your test case here
if __name__ == "__main__":
    test_fetch_api()




    