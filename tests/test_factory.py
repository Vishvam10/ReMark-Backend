import sys
import logging
from app import create_app

logging.basicConfig(stream=sys.stderr)
logging.getLogger("FactoryTestLogger").setLevel(logging.DEBUG)

def test_config():
    app, api, celery, cache = create_app(environment="testing")
    print(app)
    # assert not create_app().testing
    # assert create_app(environment="testing").testing


# def test_hello(client):
#     response = client.get('/hello')
#     assert response.data == b'Hello, World!'