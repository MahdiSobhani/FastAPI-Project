import requests

BASE_URL="http://127.0.0.1:8000"



username="API_Test"
password="111111"

r=requests.post(f"{BASE_URL}/auth/register",json={"username":username,"password":password})
print("REGISTER:",r.status_code,r.json())

r=requests.post(f"{BASE_URL}/auth/login",json={"username":username,"password":password})
print("LOGIN:",r.status_code,r.json())

token=r.json()["access_token"]
headers={"Authorization":f"Bearer {token}"}
r=requests.post(f"{BASE_URL}/tasks",json={"title":"Test FastAPI"},headers=headers)
print("CREATE:",r.status_code,r.json())

task_id=r.json()["id"]
r=requests.get(f"{BASE_URL}/tasks",headers=headers)
print("GET ALL:",r.status_code,r.json())

r=requests.get(f"{BASE_URL}/tasks/{task_id}",headers=headers)
print("GET ONE:",r.status_code,r.json())

r=requests.patch(f"{BASE_URL}/tasks/{task_id}",json={"completed":True},headers=headers)

print("UPDATE:",r.status_code,r.json())

r=requests.delete(f"{BASE_URL}/tasks/{task_id}",headers=headers)
print("DELETE:",r.status_code)

r=requests.get(f"{BASE_URL}/tasks")
print('Fail...',r.status_code)
print(r.json())

r=requests.get(f"{BASE_URL}/tasks",headers=headers)
print('Success',r.status_code)
print(r.json())
