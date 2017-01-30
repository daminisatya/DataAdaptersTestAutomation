import requests
import json

requestInformation = [request.rstrip('\n') for request in open('Zendesk/inputPayloads.txt')]
NumberOfRequestsInQueue = len(requestInformation)
countOfRequestsDone = 0

headers = {
    'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    'X-Kony-Authorization': "eyAidHlwIjogImp3dCIsICJhbGciOiAiUlMyNTYiIH0.eyAiX3ZlciI6ICJ2MS4xIiwgImlzcyI6ICJodHRwOi8vbG9jYWxob3N0OjgwODAvYXV0aFNlcnZpY2UvMTAwMDAwMDAyIiwgIl9zY29wZSI6ICJnIiwgIl9pc3NtZXRhIjogIi9tZXRhZGF0YS85YUxQMmtDaWFHQktlOEJLMTh6WTh3PT0iLCAiX3Nlc3Npb25faWQiOiAiZDliM2FhNTMtMTViNy00YWE5LWE1ZGItYTMwMzcyYzYwNjAyIiwgIl9wdWlkIjogNCwgIl9hdXRoeiI6ICJleUp3WlhKdGFYTnphVzl1Y3lJNmUzMHNJbkp2YkdWeklqcGJYWDAiLCAiX2lkcCI6ICJ6ZW5kZXNrIiwgImV4cCI6IDE0ODU3MDcxNzEsICJpYXQiOiAxNDg1NzAzNTcxLCAiX3Nlc3Npb25fdGlkIjogIjEwMDAwMDAwMiIsICJfcHJvdl91c2VyaWQiOiAiYXV0aGVudGljYXRlZHVzZXIiLCAianRpIjogIjkwN2MxYWFjLThkNjQtNDNjNC1hNjIwLTVmMzVmNjc1MjA1YiIsICJfYWNzIjogIjEwMDAwMDAwMiIsICJfcHJvdmlkZXJzIjogWyAiemVuZGVzayIgXSB9.Hwg8uqKouT5pc7a0TKyouuytxkPYmLPbMBfIsjDGQ1qO1FhOsxwAY4EZFgfmiWKGxDHKHWCpbg0DWYoNwohsxJidRDFhOLcpUe-DmlNPtoVCLagA1CxCocQ4rERH-Q42te5WUul7x4ktaCdYhlMklelhxpCfCmEUqCEdXv4XeEkuAao7y2EUpae9aSavkefHEucJLs1gmXHxiGg_XCseSoxZUIILUq5UYTcKNepywSHr1WowLu0rEO6KOuaNusL8r1u-IWgScGJrwbmjqlgRQXPWywQbKwdDl4u1G2Zk-RvrQjI7xtFT-75OkZ_QEjuysVp4vlio6lZQeeKtHQkNCw",
    'cache-control': "no-cache"
    }

while countOfRequestsDone != NumberOfRequestsInQueue:
	dataPayload = requestInformation[countOfRequestsDone].split(',')
	method = dataPayload[0].strip()
	url = dataPayload[1].strip()
	payload = dataPayload[2].strip()

	filename = 'ZendeskTest/' + url.split('/')[-1] + '.txt'
	response = requests.request(method, url, data=payload, headers=headers).json()

	outputFile = open(filename, 'w')

	outputFile.write(json.dumps(response, indent=4))
	countOfRequestsDone += 1

print "done"
