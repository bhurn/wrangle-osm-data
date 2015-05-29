# -*- coding: utf-8 -*-

# This program audits the street types for unexpected values and was used to 
# iteratively build the expected array and mapping dictionary in prepare_xml

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "/home/bhurn/Downloads/interpreter.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

# This array includes all expected street types that will not need correction
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "Way", "41", "Branches", "Circle", "Connector",
            "Cove", "Creekwood", "Crossing", "E", "Extension", "Glen", "Glenn", "Highway",
            "Hollow", "Loop", "Meadows", "NE", "NW", "North", "Overlook", "Pass",
            "Path", "Ridge", "Run", "SE", "SW", "Tarn", "Trace", "W", "Walk"]


# Checks the street type from regex function and adds to dictionary if not in
# expected
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

# Logical test for street tags
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

# Function that iterates through the elements in the OSM file and calls the
# function that checks the street names in node and way tags
def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])

    return street_types

# Main function that calls the audit function and prints the results
def test():
    st_types = audit(OSMFILE)
    pprint.pprint(dict(st_types))

    '''
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name
    '''

if __name__ == '__main__':
    test()