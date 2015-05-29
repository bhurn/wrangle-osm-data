# -*- coding: utf-8 -*-
"""
Created on Sat May 23 20:44:40 2015

@author: bhurn
"""

# This file contains a series of pymongo queries that were run independently
# to exlpore the database created in this project.

from pymongo import MongoClient
import pprint
client = MongoClient()
db = client.osmdb
"""
# Find known entry with problem street
prob_street = db.cobb.find_one({'address.street': 'Ernest W Barrett Parkway Suite 4015'})
pprint.pprint(prob_street)

# Fix the problematic street entry
db.cobb.update({'address.street': 'Ernest W Barrett Parkway Suite 4015'},{"$set": {'address.street': 'Ernest W Barrett Parkway'}})
             
# Check that street entry was fixed
prob_street = db.cobb.find_one({'address.street': 'Ernest W Barrett Parkway'})
pprint.pprint(prob_street)

# Find all documents with problematic zip code that lies outside area
for prob_zip_entry in db.cobb.find({'address.postcode': '30092'}):
    pprint.pprint(prob_zip_entry)

# Check that entry with "Rd." was changed to "Road" 
for prob_street in db.cobb.find({'address.street': 'Cooper Lake Road'}):
    pprint.pprint(prob_street)

# These pipelines were used to check for various statistics of the database

# Find the most active contributor
pipeline = [{"$group": {"_id": "$created.user", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            { "$limit": 1}]

# Get count of unique users
pipeline = [{"$group": {"_id": "$created.user", "count": {"$sum": 1}}},
            {"$group": {"_id": "_id", "count": {"$sum": 1}}}]

# Get list of amenities sorted by count
pipeline = [{"$group": {"_id": "$amenity", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}]

# Count entries with these two problematic zip codes
pipeline = [{"$match": {"address.postcode": {"$in": ["30092", "30114"]}}},
            {"$group": {"_id": "$address.postcode", "count": {"$sum": 1}}}]

# Optional approach to same question
db.cobb.find({"address.postcode": "30092"}).count()

# Code to run and print the pipelines above
users = db.cobb.aggregate(pipeline)
for user in users:
    pprint.pprint(user)
"""
 
# Code to confirm that "Rd" was updated to "Road" in street ending in direction
for prob_street in db.cobb.find({'address.street': 'Lake Road W'}):
    pprint.pprint(prob_street)

            