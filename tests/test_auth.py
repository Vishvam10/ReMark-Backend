from pydoc import cli
import pytest
from flask import g, session, url_for

def test_login(app):
    with app.app_context() :
    # res = client.get("/api/user")
        print("RESPONSE : ", app.url_map)
    # response = auth.login()
    # print("HEADERS : ", response.headers)
    # with client:
        # client.get('/')
        # assert session['user_id'] == 1
        # assert g.user['username'] == 'test'