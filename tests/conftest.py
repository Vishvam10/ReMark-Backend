import sys
import logging
import pytest
from app import create_app

# logging.basicConfig(stream=sys.stderr)
# logging.getLogger("TestUserAPILogger").setLevel(logging.DEBUG)


@pytest.fixture()
def app():
    app, api, celery, cache = create_app(environment="testing")
    logger = logging.getLogger("TestUserAPILogger")
    logger.debug(app)
    return app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
