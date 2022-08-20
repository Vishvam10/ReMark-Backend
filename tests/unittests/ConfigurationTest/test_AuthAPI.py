import json

def create_dummy_admin(client) :
    ADMIN_DATA = {
        "email_id": "testing_admin@gmail.com",
        "username": "testing_admin",
        "password": "testing123",
        "bio": "Hello World !",
        "authority": "admin",
    }
    res = client.post("/api/user", json=ADMIN_DATA)
    return ADMIN_DATA

def test_login(client, auth):
    admin_data = create_dummy_admin(client)
    data = {
        "username": admin_data["username"],
        "password" : admin_data["password"],
        "authority" : admin_data["authority"]
    }
    res = auth.login(data)
    print("LOGIN RESPONSE : ", res)
    assert res is not None
    assert res.get("status") == 200
    assert res.get("message") == "Logged in successfully"
    
