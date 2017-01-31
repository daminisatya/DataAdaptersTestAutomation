import xml.etree.ElementTree as ET

tree = ET.parse('zendesk.xml')
root = tree.getroot()

for neighbor in root.iter('service'):
	print neighbor.get('id')