import os
import sys
import string
def file_checker(filein):
    """
    Check if the file exists and is not empty.
    """
    if os.path.exists(filein):
        # check if file is empty
        if os.stat(filein).st_size == 0:
            print("File is empty")
            return False
        else:
            print("File exists and is not empty")
            return True

    else:
        print("File does not exist")
        return False
    
