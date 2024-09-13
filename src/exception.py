import sys
import logging
import logger

## this method customises the error message in a format we prefer
def error_message_detail (error, error_details:sys):
    _,_,exc_tb = error_details.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename

    error_message = "Error occured in file [{0}] line no. [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str (error)
    )

    return error_message

## custom exception class with a local variable 'error_message' which is loaded/formatted using the method above
class CustomException (Exception):

    ## constructor which overrides constructor of the 'Exception' class using 'super' keyword
    ## self is equal to 'this' in C#
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_details=error_detail)

    ## __x__ are 'dunder methods' for Python’s built-in operators and functions 
    ## __str__() method returns a human-readable, or informal, string representation of an object
    def __str__(self):
        return self.error_message



# if __name__== "__main__":

#     try:
#         a=1/0
#     except Exception as e:
#         logging.info("Divide by 0 error !")
#         raise CustomException(e, sys)
    