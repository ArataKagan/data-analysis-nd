import xml.etree.cElementTree as ET
import re
import pprint 
from collections import defaultdict
file = 'small_sample.osm'


LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')

def get_zipcode(filename):
	tag_type = set()
	for event, elem in ET.iterparse(filename):
		if elem.tag == 'node' or elem.tag == 'way':
			for tag in elem.iter('tag'):
				if tag.attrib['k'] == 'addr:postcode':
					tag_type.add(tag.attrib['v'])
	return tag_type
			
item_list = get_zipcode(file)
pprint.pprint(item_list)

'''
1. Get only the first block of zipcode
95004-9506

2. fix the zipcode with CA in the beginning
CA 95110
CA 95762
'''

