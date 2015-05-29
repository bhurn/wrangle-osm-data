# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 21:11:12 2015

@author: bhurn
"""

# This program prepares the contents of the OSM XML file, selects the node and
# way tags, cleans the street names, and writes the results to a JSON file.

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import re
import codecs
import json

OSMFILE = "/home/bhurn/Downloads/interpreter.osm"

problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

# This list includes all expected street types that will not need correction
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "Way", "41", "Branches", "Circle", "Connector",
            "Cove", "Creekwood", "Crossing", "E", "Extension", "Glen", "Glenivy", "Glenn", "Highway",
            "Hollow", "Loop", "Meadows", "NE", "NW", "North", "Overlook", "Pass",
            "Path", "Point", "Pointe", "Ridge", "Run", "SE", "SW", "Tarn", "Terrace",
            "Trace", "W", "Walk", "4015"]

# This dictionary provides the mapping of the problematic street types to their
# correct versions
mapping = { "Ave": "Avenue",
            "Ave.": "Avenue",
            "Blvd": "Boulevard",
            "Cir": "Circle",
            "Cobb": "Cobb Parkway",
            "Ct": "Court",
            "Dr": "Drive",
            "Exd": "Extension",
            "Hwy": "Highway",
            "Ln": "Lane",
            "North": "N",
            "Northeast": "NE",
            "Northwest": "NW",
            "Pkwy": "Parkway",
            "Pky": "Parkway",
            "Pl": "Place",
            "Pt": "Point",
            "Rd": "Road",
            "Rd.": "Road",
            "South": "S",
            "Southeast": "SE",
            "Southwest": "SW",
            "St": "Street",
            "St.": "Street",
            "Ter": "Terrace",
            "Trce": "Trace",
            "Trl": "Trail",
            "Xing": "Crossing"
            }

# Main street audit function that checks for street name tags and calls
# audit_street_type function for required corrections
def street_audit(elem):

    for tag in elem.iter("tag"):
        if tag.attrib['k'] == "addr:street":
            tag.attrib['v'] = audit_street_type(tag.attrib['v'])

    return elem
    
# This function corrects street types not found in the expected list using the
# mapping dictionary. 
def audit_street_type(street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_name = update_name(street_name, -1)
    
    # check for name ending in a directional indicator and audit preceding word
    m2 = street_type_re.search(street_name)
    if m2:
        directional = m2.group()
        if directional in ["N", "S", "E", "W", "NE", "NW", "SE", "SW"]:       
            street_type2 = street_name.split()[-2]
            if street_type2 not in expected:
                street_name = update_name(street_name, -2)        
    
    return street_name     

# Update problematic street types using the mapping dictionary. The variable
# pos selects the last  (-1) or second to last (-2) word. The latter is used for
# street names that end in a directional indicator (such as "W" or "SW").
def update_name(name, pos):

    bad_street = name.split()[pos]
    name = name.replace(bad_street, mapping[bad_street])
    return name

# Build dictionary from node and way elements to return to json writer  
def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        
        # clean up street names
        street_audit(element)
        
        # set node type        
        node["type"] = element.tag
        
        # process keys        
        for key in element.attrib.keys():
            if key == "lat":
                node["pos"] = [float(element.attrib["lat"]), float(element.attrib["lon"])]
            elif key == "lon":
                continue
            elif key in ["changeset", "user", "version", "uid", "timestamp"]:
                if "created" not in node.keys():
                    node["created"] = {}
                node["created"][key] = element.attrib[key]               
            else:
                node[key] = element.attrib[key]  
        
        # process tags
        for tag in element.iter("tag"):
            if problemchars.search(tag.attrib["k"]):
                continue
            if tag.attrib["k"].startswith("addr:"):
                k_words = tag.attrib["k"].split(":")
                if len(k_words) > 2:
                    continue
                else:
                    if "address" not in node.keys():
                        node["address"] = {}
                    node["address"][k_words[1]] = tag.attrib["v"]
            else:
                node[tag.attrib["k"]] = tag.attrib["v"]
        
        # process node refs for way elements        
        if element.tag == "way":
            if "node_refs" not in node.keys():
                node["node_refs"] = []
            for ref in element.iter("nd"):
                node["node_refs"].append(ref.attrib["ref"])

        return node
    else:
        return None


# This function calls the main shape_element function and writes the results 
# to the .json file.
def process_map(file_in, pretty = False):
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return

def test():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    process_map(OSMFILE, False)
    #pprint.pprint(data)


if __name__ == "__main__":
    test()
