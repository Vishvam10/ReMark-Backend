import logging
import sys
import pytest
import urllib

from app import create_app

from flask import Flask, jsonify


logging.basicConfig(stream=sys.stderr)
logging.getLogger("TestUserAPILogger").setLevel(logging.DEBUG)


def test_request_example(app):
    # url = "http://172.19.22.209:5000/api" + "/dummy"
    # response = client.get(url)
    # logger = logging.getLogger("TestUserAPILogger")
    # logger.debug(url)
    # logger.debug(client)
    # logger.debug(response)
    # for rule in app.url_map.iter_rules():
    #     print(rule)
    # with app.app_context(), app.test_request_context():
    endpoints = [rule.rule for rule in app.url_map.iter_rules()
                 if rule.endpoint != 'static']
    print(dict(api_endpoints=endpoints))

    assert 1 == 2
