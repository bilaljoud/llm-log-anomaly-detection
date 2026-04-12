# main program to run the scripts starting with the data loading, cleaning, prompting and evaluation. 
# The main function will call the other functions in the correct order to execute the entire pipeline.

import os

from load_data import *
from clean_data import *
from prompting import *
from eval import *
from aggregate_data import *

data_path = os.getcwd() + "/data/"

def main():
    print("Starting program...")
    print("Final Results: " + str(eval()))

if __name__ == "__main__":
    main()