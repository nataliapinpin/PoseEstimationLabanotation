# https://www.geeksforgeeks.org/read-json-file-using-python/

import json
import numpy as np


JSON_PATH = "C:\\Users\\natal\\Documents\\HonorsThesis\\PoseEstimationLabanotation\\joints.json"

def read_json_to_list():
    f = open(JSON_PATH,)
 
    # returns JSON object as
    # a dictionary
    data = json.load(f)
    joints = np.zeros((len(data),16,3))
 
    # Iterating through the json list
    for i in range(len(data)):
        joints[i] = np.array(list(data[i].values()))
        #print(data[i].values())
 
    # Closing file
    f.close()

    return joints

def read_json_to_dict():
    f = open(JSON_PATH,)
 
    # returns JSON object as
    # a dictionary
    data = json.load(f)
 
    # Closing file
    f.close()

    return data


if __name__ == "__main__":
    read_json_to_list()
