import requests
import json
import polling
import os
from lxml import etree


with open('properties.json') as data_file:    
    data = json.load(data_file)


url = data["login"]["url"] + "/" + data["login"]["type"] + "/login?provider=" + data["login"]["prov"]

payload = { "userid": "maverick123nerd@gmail.com",
			"password" : "maverick123nerd"
		}

headers = {
    'content-type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache"
    }

responseAuthKeys = polling.poll(
    lambda: requests.request("POST", url, data=payload, headers=headers).json(),
	step=20,
    poll_forever=True
)

def loadAPIsResponseInformation() :
	requestInformation = [request.rstrip('\n') for request in open(data["requestAPIsInformationFileName"])]
	NumberOfRequestsInQueue = len(requestInformation)
	countOfRequestsDone = 0

	if not os.path.exists(data["OriginalResponse"]):
		fileName = data["OriginalResponse"]
	else:
		fileName = data["TestResponse"]
		
	os.makedirs(fileName)
		
	while countOfRequestsDone != NumberOfRequestsInQueue:
		dataPayload = requestInformation[countOfRequestsDone].split(',')
		method = dataPayload[0].strip()
		url = dataPayload[1].strip()
		payload = dataPayload[2].strip()		
		filename = fileName + "/" + url.split('/')[-1] + '.txt'
		data["headers"]["x-kony-authorization"] = responseAuthKeys["claims_token"]
		response = requests.request(method, url, data=payload, headers=data["headers"]).json()
		outputFile = open(filename, 'w')
		outputFile.write(json.dumps(response, indent=4))
		countOfRequestsDone += 1

	print "Done loading API Response Information"

def list_difference(list1, list2):
	return list([list(list1 - list2) , list(list2 - list1)])

def loadAPIsRequestInformation() :
	tree = etree.parse(data["ServiceDefFileName"])

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

	file_out = open(data["requestAPIsInformationFileName"], 'w')

	for key, value in idInputMap.items():
		formPayload = "POST," + data["HostName"] +"/services/" + data["serviceName"] + "/" + key + ","
		for payload in value:
			formPayload += payload[0] + 'name=\"' + payload[1] + '\"\r\n\r\n' + payload[2] + '\r\n'
		formPayload += '------WebKitFormBoundary7MA4YWxkTrZu0gW--'

		file_out.write(repr(formPayload)[2:-1])
		file_out.write('\n')
	print "Done loading API Request Information"

def getKeysFromTheJson(jsonObject, keys_list):
    if isinstance(jsonObject, dict):
        keys_list += jsonObject.keys()
        map(lambda x: getKeysFromTheJson(x, keys_list), jsonObject.values())
    elif isinstance(jsonObject, list):
        map(lambda x: getKeysFromTheJson(x, keys_list), jsonObject)

def getDiffBetweenResponses():
	requestInformation = [request.rstrip('\n') for request in open(data["requestAPIsInformationFileName"])]
	NumberOfRequestsInQueue = len(requestInformation)
	countOfRequestsDone = 0

	while countOfRequestsDone != NumberOfRequestsInQueue:
		dataPayload = requestInformation[countOfRequestsDone].split(',')
		url = dataPayload[1].strip()

		filenameTest = data["OriginalResponse"]+ "/" + url.split('/')[-1] + '.txt'
		filename = data["TestResponse"]+ "/" + url.split('/')[-1] + '.txt'

		with open(filename, 'r') as file1:
			with open(filenameTest, 'r') as file2:

				originalData = json.load(file1)
				testData = json.load(file2)
				originalKeys = []
				testKeys = []
				getKeysFromTheJson(originalData, originalKeys)
				getKeysFromTheJson(testData, testKeys)

				differentKeys = list_difference(set(originalKeys), set(testKeys))

		if not os.path.exists('testFailures'):
			os.makedirs('testFailures')

		if len(differentKeys) > 0:
			errorLogFileName = 'testFailures/ErrorLog_' + url.split('/')[-1] + '.txt'
			with open(errorLogFileName, 'w') as file_out:
				file_out.write(str(differentKeys))

		countOfRequestsDone += 1


if  not os.path.exists(data["OriginalResponse"]) or not os.path.exists(data["TestResponse"]):
	if os.path.exists(data["requestAPIsInformationFileName"]) and os.path.getsize(data["requestAPIsInformationFileName"]) > 0:
		loadAPIsResponseInformation()
	else:
		loadAPIsRequestInformation()
		loadAPIsResponseInformation()
else:
	getDiffBetweenResponses()
