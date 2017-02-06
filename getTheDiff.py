import requests
import json

requestInformation = [request.rstrip('\n') for request in open('damini.txt')]
NumberOfRequestsInQueue = len(requestInformation)
countOfRequestsDone = 0

headers = {
    'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    'X-Kony-Authorization': "eyAidHlwIjogImp3dCIsICJhbGciOiAiUlMyNTYiIH0.eyAiX3ZlciI6ICJ2MS4xIiwgImlzcyI6ICJodHRwOi8vbG9jYWxob3N0OjgwODAvYXV0aFNlcnZpY2UvMTAwMDAwMDAyIiwgIl9zY29wZSI6ICJnIiwgIl9pc3NtZXRhIjogIi9tZXRhZGF0YS9GX3V1Z29NQUFvbU1ZaURWaFlUSFFnPT0iLCAiX3Nlc3Npb25faWQiOiAiYTlkZWUyYjYtNTUzZS00ZDJkLTk3NzktODdkODExZWRjMTNiIiwgIl9wdWlkIjogNCwgIl9hdXRoeiI6ICJleUp3WlhKdGFYTnphVzl1Y3lJNmUzMHNJbkp2YkdWeklqcGJYWDAiLCAiX2lkcCI6ICJaZW5EZXNrIiwgImV4cCI6IDE0ODYzNTg2ODEsICJpYXQiOiAxNDg2MzU1MDgxLCAiX3Nlc3Npb25fdGlkIjogIjEwMDAwMDAwMiIsICJfcHJvdl91c2VyaWQiOiAiYXV0aGVudGljYXRlZHVzZXIiLCAianRpIjogIjExNDc3YWFhLTMwMDItNGJiMS1iZjZjLWUyN2VhZGVjMmM0OSIsICJfYWNzIjogIjEwMDAwMDAwMiIsICJfcHJvdmlkZXJzIjogWyAiWmVuRGVzayIgXSB9.iJ4M7ktzvHJzYlmprcOhG-b_x9kgPZE4QvdSYultXF30-Ok3BpQpVSi8PtL4bLlJToSE9bg5_xrwVYl3l4iZ351NR4ZT5R1EKJtJ4PGFxv6iPhnei-TLBAcDNRfTgd4iJTuKvKNSQXL7Fm1A64FHDWKvnO6kS7kcoBuwooWx9vemEcT8OYsGJa4rAyiY7uM7gef9ZHlWZeaI0pNzNZ2-spZrpGthW8xHVNclyeHvYGnymZUq6JJJemtm_ETva0_aY0k-rT5kK4ttbcwaG2aJZlwlt9AZMcQjKjvpSdBOkC235XpFZ7YiiesSSZByxSZvg4dW-O5ACsz4yTVolHn5lg",
    'cache-control': "no-cache"
    }

def getKeysFromTheJson(jsonObject, keys_list):
    if isinstance(jsonObject, dict):
        keys_list += jsonObject.keys()
        map(lambda x: getKeysFromTheJson(x, keys_list), jsonObject.values())
    elif isinstance(jsonObject, list):
        map(lambda x: getKeysFromTheJson(x, keys_list), jsonObject)

while countOfRequestsDone != NumberOfRequestsInQueue:
	dataPayload = requestInformation[countOfRequestsDone].split(',')
	method = dataPayload[0].strip()
	url = dataPayload[1].strip()
	payload = dataPayload[2].strip()

	filenameTest = 'DemoTest/' + url.split('/')[-1] + '.txt'
	filename = 'Demo/' + url.split('/')[-1] + '.txt'

	with open(filename, 'r') as file1:
		with open(filenameTest, 'r') as file2:

			originalData = json.load(file1)
			testData = json.load(file2)
			originalKeys = []
			testKeys = []
			getKeysFromTheJson(originalData, originalKeys)
			getKeysFromTheJson(testData, testKeys)

			differentKeys = set(originalKeys).difference(testKeys)

	differentKeys.discard('\n')
	
	errorLogFileName = 'testFailures/ErrorLog' + url.split('/')[-1] + '.txt'
	with open(errorLogFileName, 'w') as file_out:
		for line in differentKeys:
			file_out.write(line)
			file_out.write('\n')

	countOfRequestsDone += 1

print "done"