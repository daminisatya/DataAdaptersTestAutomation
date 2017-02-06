from lxml import etree, objectify
import json

tree = etree.parse('zendesk.xml')

services = tree.xpath('//services/service')

idInputMap = {}

for element in services:
	API_Name = element.get('id')
	idInputMap[API_Name] = []
	for all_tags in element.findall('.//service-input/param'):
		tempInputParam = []
		STATIC_STRING = '------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; '
		inputParamAttributeName = all_tags.get('name')
		inputParamAttributeValue = all_tags.get('defaultvalue')
		tempInputParam.append(STATIC_STRING)
		tempInputParam.append(inputParamAttributeName)
		tempInputParam.append(inputParamAttributeValue)
		idInputMap[API_Name].append(tempInputParam)

file_out = open('damini.txt', 'w')

for key, value in idInputMap.items():
	formPayload = "POST," + "http://localhost:8080/services/ZenDeskSample2/" + key + ","
	for payload in value:
		formPayload += payload[0] + 'name=\"' + payload[1] + '\"\r\n\r\n' + payload[2] + '\r\n'
	formPayload += '------WebKitFormBoundary7MA4YWxkTrZu0gW--'

	file_out.write(repr(formPayload)[1:-1])
	file_out.write('\n')
