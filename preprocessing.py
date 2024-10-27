import pandas as pd
import csv
import json
import yaml
import requests

def main3(uploaded_file):

    if ('csv' in str(uploaded_file)) == True :
        data = pd.read_csv(uploaded_file)
    elif ('json' in str(uploaded_file)) == True :
        data = pd.read_json(uploaded_file)
    elif ('yaml' in str(uploaded_file)) == True :
        data = yaml.safe_load(uploaded_file)
    else :
        data = None
    return data
