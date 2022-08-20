import os
import tempfile
import pytest

from application import create_app
from application.models.User import User
from application.models.Token import Token
from application.database.database import db


@pytest.fixture
def app():
    app, api, celery, cache = create_app(environment="testing")
    app.app_context().push()
    db.create_all()
    
    yield app


@pytest.fixture
def client(app):
    app.testing = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

# AUTH

class AuthActions(object):

    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/api/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)