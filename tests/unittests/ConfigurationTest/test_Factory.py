import sys
import logging
from app import create_app

logging.basicConfig(stream=sys.stderr)
logging.getLogger("FactoryTestLogger").setLevel(logging.DEBUG)

def test_config():
    app, api, celery, cache = create_app(environment="testing")
    assert app.config["TESTING"] == True
    