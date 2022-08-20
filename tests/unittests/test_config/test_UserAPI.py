

def test_create_user(client) :
    res = client.get("/api/user/all_users").data
    print("RESPONSE : ", res)
