import yaml
import json
import os

def getConfig(file):
    print(file)
    with open(file) as f:
        y = yaml.safe_load(f)
        j = json.loads("Policies")

        print(y)
        print(j)
        return j