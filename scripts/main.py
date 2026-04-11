# main program to run the scripts starting with the data loading, cleaning, prompting and evaluation. 
# The main function will call the other functions in the correct order to execute the entire pipeline.

import os

from scripts.load_data import *
from scripts.clean_data import *
from scripts.prompting import *
from scripts.eval import *
from scripts.aggregate_data import *

data_path = os.getcwd() + "/data/"

def main():
    pass

if __name__ == "__main__":
    main()