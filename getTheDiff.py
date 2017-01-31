import requests
import json

requestInformation = [request.rstrip('\n') for request in open('inputPayloads.txt')]
NumberOfRequestsInQueue = len(requestInformation)
countOfRequestsDone = 0

headers = {
    'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    'X-Kony-Authorization': "eyAidHlwIjogImp3dCIsICJhbGciOiAiUlMyNTYiIH0.eyAiX3ZlciI6ICJ2MS4xIiwgImlzcyI6ICJodHRwOi8vbG9jYWxob3N0OjgwODAvYXV0aFNlcnZpY2UvMTAwMDAwMDAyIiwgIl9zY29wZSI6ICJnIiwgIl9pc3NtZXRhIjogIi9tZXRhZGF0YS92Q3hOM3FjZjF4dE40b3ZhWjA3M1B3PT0iLCAiX3Nlc3Npb25faWQiOiAiMDk5MDM2MzgtZWFjYi00NjZhLTkwOWMtNWQyZDg4YjI4YjAxIiwgIl9wdWlkIjogNCwgIl9hdXRoeiI6ICJleUp3WlhKdGFYTnphVzl1Y3lJNmUzMHNJbkp2YkdWeklqcGJYWDAiLCAiX2lkcCI6ICJ6ZW5kZXNrSWRlbnRpdHkiLCAiZXhwIjogMTQ4NTg1NTk4MSwgImlhdCI6IDE0ODU4NTIzODEsICJfc2Vzc2lvbl90aWQiOiAiMTAwMDAwMDAyIiwgIl9wcm92X3VzZXJpZCI6ICJhdXRoZW50aWNhdGVkdXNlciIsICJqdGkiOiAiNDk0OTI5NWYtMjRjZC00YmYzLTkzZDktYWI0Y2M0ODQ1ZTA0IiwgIl9hY3MiOiAiMTAwMDAwMDAyIiwgIl9wcm92aWRlcnMiOiBbICJ6ZW5kZXNrSWRlbnRpdHkiIF0gfQ.GhiDaySR-KL63UBT4_KPIEgcuR_nxkV-dHYMuGtoy_z-hgcssSC8uCoVo_eQcPEevQq3FpMPYQqnV05Rn1vRkYDgCS9KKv2nFODQe5tMWYwGAjDBrl0qi7Iuhdet7v0eyrWwpYxvoAXmEWnDT4Vs_YkD1AO3NkvCJFXe4f5U5t_bGwafl4VcbVh8G0dv33X4-YRfkJnBrttsvD_xH4pQRGEnbVwyHfZXAJz-mKflxXIrGk-UoPQF3386BgPHAIWN73h6ce1EjYsXjiYnkMgTgkxzopUeVp9WJHGjvMHWfkLN7ZTBd5l75Nhj9b3FUq6TrHJkgrExMVJPkWQNCOqp8Q",
    'cache-control': "no-cache"
    }

def find_key(dic):
	keys=[]
	if isinstance(dic,dict): 
		for key,value in dic.items():
			if isinstance(value,dict):
				keys.append(key)
				keys.append(find_key(value))
			elif isinstance(value,list):
				keys.append(key)
				keys.append(find_key(value[0]))
			else:
				keys.append(key)
	return keys

while countOfRequestsDone != NumberOfRequestsInQueue:
	dataPayload = requestInformation[countOfRequestsDone].split(',')
	method = dataPayload[0].strip()
	url = dataPayload[1].strip()
	payload = dataPayload[2].strip()

	filenameTest = 'ZendeskTest/' + url.split('/')[-1] + '.txt'
	filename = 'Zendesk/' + url.split('/')[-1] + '.txt'

	with open(filename, 'r') as file1:
		with open(filenameTest, 'r') as file2:
			# json_objectTest = json.loads(file2)

			# json_object = json.loads(file1)

			# fileNameTestKeys = find_key(json_objectTest)
			# fileNameKeys = find_key(json_object)
			differentKeys = set(file1).difference(file2)

	differentKeys.discard('\n')
	
	print 
	for line in differentKeys:
		errorLogFileName = 'testFailures/ErrorLog' + url.split('/')[-1] + '.txt'
		with open(errorLogFileName, 'w') as file_out:
			file_out.write(line)

	countOfRequestsDone += 1

print "done"