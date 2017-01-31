import requests
import json

requestInformation = [request.rstrip('\n') for request in open('inputPayloads.txt')]
NumberOfRequestsInQueue = len(requestInformation)
countOfRequestsDone = 0

headers = {
    'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    'x-kony-authorization': "eyAidHlwIjogImp3dCIsICJhbGciOiAiUlMyNTYiIH0.eyAiX3ZlciI6ICJ2MS4xIiwgImlzcyI6ICJodHRwOi8vbG9jYWxob3N0OjgwODAvYXV0aFNlcnZpY2UvMTAwMDAwMDAyIiwgIl9zY29wZSI6ICJnIiwgIl9pc3NtZXRhIjogIi9tZXRhZGF0YS92Q3hOM3FjZjF4dE40b3ZhWjA3M1B3PT0iLCAiX3Nlc3Npb25faWQiOiAiMDk5MDM2MzgtZWFjYi00NjZhLTkwOWMtNWQyZDg4YjI4YjAxIiwgIl9wdWlkIjogNCwgIl9hdXRoeiI6ICJleUp3WlhKdGFYTnphVzl1Y3lJNmUzMHNJbkp2YkdWeklqcGJYWDAiLCAiX2lkcCI6ICJ6ZW5kZXNrSWRlbnRpdHkiLCAiZXhwIjogMTQ4NTg1NTk4MSwgImlhdCI6IDE0ODU4NTIzODEsICJfc2Vzc2lvbl90aWQiOiAiMTAwMDAwMDAyIiwgIl9wcm92X3VzZXJpZCI6ICJhdXRoZW50aWNhdGVkdXNlciIsICJqdGkiOiAiNDk0OTI5NWYtMjRjZC00YmYzLTkzZDktYWI0Y2M0ODQ1ZTA0IiwgIl9hY3MiOiAiMTAwMDAwMDAyIiwgIl9wcm92aWRlcnMiOiBbICJ6ZW5kZXNrSWRlbnRpdHkiIF0gfQ.GhiDaySR-KL63UBT4_KPIEgcuR_nxkV-dHYMuGtoy_z-hgcssSC8uCoVo_eQcPEevQq3FpMPYQqnV05Rn1vRkYDgCS9KKv2nFODQe5tMWYwGAjDBrl0qi7Iuhdet7v0eyrWwpYxvoAXmEWnDT4Vs_YkD1AO3NkvCJFXe4f5U5t_bGwafl4VcbVh8G0dv33X4-YRfkJnBrttsvD_xH4pQRGEnbVwyHfZXAJz-mKflxXIrGk-UoPQF3386BgPHAIWN73h6ce1EjYsXjiYnkMgTgkxzopUeVp9WJHGjvMHWfkLN7ZTBd5l75Nhj9b3FUq6TrHJkgrExMVJPkWQNCOqp8Q",
    'cache-control': "no-cache",
}

while countOfRequestsDone != NumberOfRequestsInQueue:
	dataPayload = requestInformation[countOfRequestsDone].split(',')
	method = dataPayload[0].strip()
	url = dataPayload[1].strip()
	payload = dataPayload[2].strip()

	url = "http://localhost:8080/services/zendeskApp/get_account_settings_mediaTypeExtension"

	payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"mediaTypeExtension\"\r\n\r\n.json\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"domain\"\r\n\r\nkonyhelp\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"

	filename = 'Zendesk/' + url.split('/')[-1] + '.txt'
	response = requests.request(method, url, data=payload, headers=headers).json()

	print response

	outputFile = open(filename, 'w')

	outputFile.write(json.dumps(response, indent=4))
	countOfRequestsDone += 1

print "done"
