# -*- coding: utf-8 -*-
"""
Created on Sat May 23 17:23:06 2015

@author: bhurn
"""

# This file inserts the contents of the specified JSON file into MongoDB

JSONFILE = "/home/bhurn/Downloads/interpreter.osm.json"

import json
from pymongo import MongoClient
client = MongoClient()
db = client.osmdb

# Read each line of JSON file and write to new collection "cobb"
with open(JSONFILE) as f:
    for line in f:
        db.cobb.insert(json.loads(line))
        
# Check that collection was created successfully by reading one document
print db.cobb.find_one()