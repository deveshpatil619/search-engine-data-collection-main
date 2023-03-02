import uuid
"""This Python function generates a unique name for an image by using the UUID (Universally Unique Identifier)
 library. The function uses the uuid.uuid1() method to generate a UUID version 1, which is based on the current
time, the computer's MAC address, and a random number."""


# Generate Unique Names for all the images
def image_unique_name():
    return "img-" + str(uuid.uuid1()) ## The UUID is then converted to a string and concatenated with the 
#prefix "img-" to form the unique image name. The resulting name is a string in the format "img-<uuid>", 
# where <uuid> is a unique identifier.





