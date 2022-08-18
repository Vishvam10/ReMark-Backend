from pydoc import cli
import pytest
from flask import g, session, url_for

def test_login(client, auth):
    res = client.get("/api/login")
    print("RESPONSE : ", res)
    # response = auth.login()
    # print("HEADERS : ", response.headers)
    # with client:
        # client.get('/')
        # assert session['user_id'] == 1
        # assert g.user['username'] == 'test'