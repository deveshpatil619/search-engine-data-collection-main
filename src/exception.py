import os


class IntegrityError(Exception):
    """Label Already Exists"""


def error_message_detail(error, error_detail):

#The purpose of this function is to format error messages that include the file name, line number, and 
#error message. 

    _, _, exc_tb = error_detail.exc_info() #This line extracts information about the current exception using the
#exc_info() method of the error_detail object. The method returns a tuple containing the exception type, value,
#  and traceback. We only need the traceback, so we use the underscore (_) to indicate that we are not interested in the first two elements of the tuple.
    file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1] #This line extracts the file name where the
#error occurred from the traceback object using the os.path.split() method. The method splits the file path into 
# a directory and file name, and we only need the file name, so we use [1] to access it.
    error_message = "Error occurred python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error) ## his line formats the error message as a string using the 
#format() method. The string includes placeholders {0}, {1}, and {2} that are replaced with the values of 
# file_name, exc_tb.tb_lineno, and str(error) respectively.
    )

    return error_message


class CustomException(Exception):
    def __init__(self, error_message, error_detail):
        """
        :param error_message: error message in string format
        """
        super().__init__(error_message)
        self.error_message = error_message_detail(
            error_message, error_detail=error_detail
        )

    def __str__(self):
        return self.error_message
