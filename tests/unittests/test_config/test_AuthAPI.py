import json
# import pytest

def create_dummy_admin(client) :
    ADMIN_DATA = {
        "email_id": "testing_admin@gmail.com",
        "username": "testing_admin",
        "password": "testing123",
        "bio": "Hello World !",
        "authority": "admin",
    }
    res = json.loads(client.post("/api/user", json=ADMIN_DATA).data)
    print("RESPONSE : ", res)


def test_login(client, auth):
    # response = auth.login(username='test', password='test')
    # print(response)
    create_dummy_admin(client)