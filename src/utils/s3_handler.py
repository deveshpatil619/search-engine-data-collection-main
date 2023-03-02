"""os and sys are imported for handling operating system related tasks.
boto3 is a Python library that provides low-level access to AWS services.
boto3.session is imported for creating a session to connect to the S3 bucket.
Dict is imported from typing for defining the return type of some methods.
image_unique_name is a custom function from src.utils.utils that generates a unique name for an image.
CustomException is a custom exception class from src.exception that formats error messages in a specific way."""

import os, sys
import boto3
import boto3.session

from typing import Dict

from src.utils.utils import image_unique_name
from src.exception import CustomException


class S3Connection: ## S3Connection is a class that provides methods to interact with the S3 bucket.
    """Data Class for reverse image search engine."""

    def __init__(self): 
        """The first line creates a new session object for boto3 with the AWS access key ID and 
        AWS secret access key set in the environment variables AWS_ACCESS_KEY_ID and 
        AWS_SECRET_ACCESS_KEY, respectively."""
        session = boto3.Session( 
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        )
        self.s3 = session.resource("s3") # creates an S3 resource object using the session object.
        self.bucket = self.s3.Bucket(os.environ["AWS_BUCKET_NAME"]) # sets the bucket attribute of the class 
# instance to the S3 bucket specified in the environment variable AWS_BUCKET_NAME

    def add_label(self, label: str) -> Dict:
        """
         This Function is responsible for adding label in s3 bucket.
         param label: label Name
         :return: json Response of state message (success or failure)
         """
        try:
            key = f"images/{label}/" ##key is the S3 object key that specifies the path of the new folder in the S3 bucket.
            response = self.bucket.put_object(Body="", Key=key) #self.bucket.put_object is used to create the new folder in the S3 bucket.
            return {"Created": True, "Path": response.key} ## response.key returns the path of the new folder.
        except Exception as e:
            message = CustomException(e, sys) ##If an exception occurs, CustomException is used to format the error message and return it in a dictionary format.
            return {"Created": False, "Reason": message.error_message}

    def upload_to_s3(self, image_path, label: str):
        """
        This Function is responsible for uploading images in the predefined
        location in the s3 bucket.
        param label: label Name
        :param image_path: Path to the image to upload
        :return: json Response of state message (success or failure)
        """
        try:
            self.bucket.upload_fileobj(
                image_path,
                f"images/{label}/{image_unique_name()}.jpeg",
                ExtraArgs={"ACL": "public-read"},
            )
            return {"Created": True}
        except Exception as e:
            message = CustomException(e, sys)
            return {"Created": False, "Reason": message.error_message}
