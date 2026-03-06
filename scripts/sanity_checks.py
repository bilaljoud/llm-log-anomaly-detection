import os
import pandas as pd

# project_path = '/mnt/c/Users/bilal/Documents/Tech/CAP6640-Final-Project/'
# data_path = os.path.join(project_path, 'data/')
data_path = os.getcwd() + "/data/"

rt = pd.read_csv(data_path + 'auth_attacks.csv', header=None, nrows=10)

print(rt)
