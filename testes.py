# pip install requests
import requests

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxNzUxNjYwMzA0fQ.wdU9p2kk-9ckZJ42Nbz3GCdbJ0ccUiYAl7Wf0BjCW7c"
}

request = requests.get('http://127.0.0.1:8000/auth/refresh_token', headers=headers)

print(request)
print(request.status_code)
print(request.text)
print(request.json())
print(request.headers)
print(request.cookies)
print(request.url)
print(request.encoding)
print(request.history)
print(request.elapsed)
print(request.request.headers)