import xml.etree.cElementTree as ET
import pprint
file = 'small_sample.osm'

def get_zipcode(filename):
	tag_type = set()
	for event, elem in ET.iterparse(filename):
		if elem.tag == 'node' or elem.tag == 'way':
			for tag in elem.iter('tag'):
				if tag.attrib['k'] == 'addr:city':
					tag_type.add(tag.attrib['v'])
	return tag_type
			
item_list = get_zipcode(file)
pprint.pprint(item_list)

'''
1.Fix all cap into lower cap ex. MORGAN HILL
2.Make the first letter a capital letter ex. sacramento
3. Remove the state after comma ex. , CA
'''
