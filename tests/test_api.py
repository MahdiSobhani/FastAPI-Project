from fastapi.testclient import TestClient
from main import app
import uuid

client=TestClient(app)

username=f"pytest_{uuid.uuid4().hex[:8]}"
password="123456"

def test_register():
    response=client.post("/auth/register",json={"username":username,"password":password})
    assert response.status_code==201
    assert response.json()["username"]==username


def test_login():
    response=client.post("/auth/login",json={"username":username,"password":password})
    assert response.status_code==200
    assert "access_token" in response.json()
    assert response.json()["token_type"]=="bearer"


def test_unauthorized():
    response=client.get("/tasks")
    assert response.status_code==401


def test_create_task():
    response=client.post("/auth/login",json={"username":username,"password":password})
    token=response.json()["access_token"]
    response=client.post("/tasks",json={"title":"Pytest Task"},headers={"Authorization":f"Bearer {token}"})
    assert response.status_code==201
    assert response.json()["title"]=="Pytest Task"


def test_tasks_crud():
    response=client.post("/auth/login",json={"username":username,"password":password})
    token=response.json()["access_token"]
    headers={"Authorization":f"Bearer {token}"}
    response=client.post("/tasks",json={"title":"CRUD Test"},headers=headers)
    assert response.status_code==201

    task_id=response.json()["id"]
    response=client.get("/tasks",headers=headers)
    assert response.status_code==200

    response=client.get(f"/tasks/{task_id}",headers=headers)
    assert response.status_code==200
    assert response.json()["id"]==task_id

    response=client.patch(f"/tasks/{task_id}",json={"completed":True},headers=headers)
    assert response.status_code==200
    assert response.json()["completed"] is True

    response=client.delete(f"/tasks/{task_id}",headers=headers)
    assert response.status_code==204

    response=client.get(f"/tasks/{task_id}",headers=headers)
    assert response.status_code==404


def test_invalid_login():
    response=client.post("/auth/login",json={"username":username,"password":"wrong_password"})
    assert response.status_code==401
