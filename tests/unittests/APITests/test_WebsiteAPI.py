import json

BASE_API_URL = "/api"
USER_API_URL = "{}/user".format(BASE_API_URL)

# def test_1a_create_new_user(client) :   
    
    # res = json.loads(client.post(USER_API_URL, json=USER_DATA).data)
    # assert res is not None
    # assert res.get("status") == 201
    # assert res.get("message") == "New user created"
