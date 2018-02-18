import os
import requests
import socket
from concurrent.futures import ThreadPoolExecutor

ip_address = socket.gethostbyname(socket.gethostname())
KONG_SERVICE_URL = 'http://localhost:8000/auth/'
SERVICE_URL = 'http://localhost:8080/auth/'
TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImNhcmxvc21hcnQiLCJleHAiOjE1MTkxNTgzNDYsImVtYWlsIjoiY2FybG9zbWFydDYyNkBnbWFpbC5jb20ifQ.AByT9mlPBPUI1wP77YlC04fmh50srTnb20QSzYkZDbA"
TEST_QUERY = "mutation{\n  loginUser(input: {username: \"carlosmart\", password:\"123admin123\"}){\n    user{\n      token\n    }\n  }\n}"


def test_service_kong():
    payload = {
        "query": TEST_QUERY
    }
    headers = {
        "authorization": "Bearer {}".format(TOKEN)
    }
    # print(payload)
    response = requests.post(KONG_SERVICE_URL, data=payload, headers=headers)
    # print(response.text)
    return response.elapsed.total_seconds()


def run_test_kong():
    max_time = test_service_kong()
    min_time = max_time
    for n in range(200):
        current_time = test_service_kong()
        if current_time > max_time:
            max_time = current_time
        if current_time < min_time:
            min_time = current_time
    return max_time, min_time


def test_service():
    payload = {
        "query": TEST_QUERY
    }
    # print(payload)
    response = requests.post(SERVICE_URL, data=payload)
    # print(response.text)
    return response.elapsed.total_seconds()


def run_test_service():
    max_time = test_service()
    min_time = max_time
    for n in range(200):
        current_time = test_service()
        if current_time > max_time:
            max_time = current_time
        if current_time < min_time:
            min_time = current_time
    return max_time, min_time


executor = ThreadPoolExecutor(max_workers=100)
results_kong = []
results_service = []
for n in range(5):
    results_kong.append(executor.submit(run_test_kong))

for n in range(5):
    results_service.append(executor.submit(run_test_service))

print("Results kong")
for n in results_kong:
    print(n.result())

print("Results service")
for n in results_service:
    print(n.result())
