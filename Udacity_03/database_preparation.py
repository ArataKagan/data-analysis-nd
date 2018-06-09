import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET

import cerberus

import schema

OSM_PATH = "mid_sample.osm"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema

#Street name cleaning function
mapping = {'St': 'Street',
		   'Ave.': 'Avenue',
		   'Ave': 'Avenue',
		   'Blvd': 'Boulevard',
		   'Boulevar': 'Boulevard',
		   'Cir': 'Circle',
		   'Ct': 'Court',
		   'Dr.': 'Drive',
		   'Dr': 'Drive',
		   'Ln': 'Lane',
		   'Rd': 'Road'
			}

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

def update_name(data):
	m = street_type_re.search(data)
	if m:
		street = m.group()
		if street not in expected:
			if street in mapping.keys():
				better_name = mapping[street]
				data = street_type_re.sub(better_name, data)
			return data
	else:
		return data

#Zipcode cleaning function

upper_case = re.compile(r'^[A-Z]')

def clean_zipcode(data):
	if upper_case.search(data):
		data = data.split(' ')[1]
		return data
	elif '-' in data:
		data = data.split('-')[1]
		return data

#City name cleaning function

upper_case = re.compile(r'^[A-Z]+[A-Z]+[A-Z]')
lower_case = re.compile(r'^[a-z]+[a-z]+[a-z]')

def clean_cityname(city):
	if upper_case.search(city):
		city = city.title()
		return city 
	elif lower_case.search(city):
		city = city.title()
		return city
	else:
		if ',' in city:
			city = city.split(',')[0]
		return city

#Tiger county data function 

def tiger_county(data):
	if ';' in data:
		f = data.split(';')[0]
		data = f.split(', ')[0]
	else:
		data = data.split(', ')[0]
	return data


#Lesson Quiz's codes 

NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = [] 

    if element.tag == 'node':
        for attrib in NODE_FIELDS:
            if element.get(attrib):
            	node_attribs[attrib] = element.attrib[attrib]
            else:
            	return
        for child in element:
            if PROBLEMCHARS.match(child.attrib['k']):
                continue
            elif LOWER_COLON.match(child.attrib['k']):
                tag = {}
                tag['id'] = element.attrib['id']
                tag['key'] = child.attrib['k'].split(':',1)[1]
                tag['type'] = child.attrib['k'].split(':',1)[0]
                if child.attrib['k'] == 'addr:street':
                	if update_name(child.attrib['v']):
                		tag['value'] = update_name(child.attrib['v'])
                	else:
                		continue 
                elif child.attrib['k'] == 'addr:postcode':
                	if clean_zipcode(child.attrib['v']):
                		tag['value'] = clean_zipcode(child.attrib['v'])
                	else:
                		continue 
                elif child.attrib['k'] == 'addr:city':
                	if clean_cityname(child.attrib['v']):
                		tag['value'] = clean_cityname(child.attrib['v'])
                	else:
                		continue 	
                elif child.attrib['k'] == 'tiger:county':
                	if tiger_county(child.attrib['v']):
                		tag['value'] = tiger_county(child.attrib['v']) 
                	else:
                		continue
                else:
                	tag['value'] = child.attrib['v']
                tags.append(tag)
            else:
                tag = {}
                tag['id'] = element.attrib['id']
                tag['key'] = child.attrib['k']
                tag['value'] = child.attrib['v']
                tag['type'] = 'regular'
                tags.append(tag)
        return {'node': node_attribs, 'node_tags': tags}
    
    elif element.tag == 'way':
        for attrib in WAY_FIELDS:
            if element.get(attrib):
                way_attribs[attrib] = element.attrib[attrib]
            else:
            	return
        
        position = 0
        
        for child in element:
        	way_tag = {}
        	way_node = {}
        	if child.tag == 'tag':
        		if PROBLEMCHARS.match(child.attrib['k']):
        			continue
        		elif LOWER_COLON.match(child.attrib['k']):
        			way_tag['type'] = child.attrib['k'].split(':',1)[0]
        			way_tag['key'] = child.attrib['k'].split(':',1)[1]
        			way_tag['id'] = element.attrib['id']
        			if child.attrib['k'] == 'addr:street':
        				if update_name(child.attrib['v']):
        					way_tag['value'] = update_name(child.attrib['v']) 
        				else:
        					continue 
        			elif child.attrib['k'] == 'addr:postcode':
        				if clean_zipcode(child.attrib['v']):
        					way_tag['value'] = clean_zipcode(child.attrib['v'])
        				else:
        					continue 
        			elif child.attrib['k'] == 'addr:city':
        				if clean_cityname(child.attrib['v']):
        					way_tag['value'] = clean_cityname(child.attrib['v'])
        				else:
        					continue 
        			elif child.attrib['k'] == 'tiger:county':
        				if tiger_county(child.attrib['v']):
        					way_tag['value'] = tiger_county(child.attrib['v'])
        				else:
        					continue
        			else:
        				way_tag['value'] = child.attrib['v']
        			tags.append(way_tag)
        			
        		else:
        			way_tag['type'] = 'regular'
        			way_tag['key'] = child.attrib['k']
        			way_tag['id'] = element.attrib['id']
        			way_tag['value'] = child.attrib['v']
        			tags.append(way_tag)
        	elif child.tag == 'nd':
        		way_node['id'] = element.attrib['id']
        		way_node['node_id'] = child.attrib['ref']
        		way_node['position'] = position
        		way_nodes.append(way_node)                
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    process_map(OSM_PATH, validate=False)
