from http.client import HTTPResponse
from flask import current_app as app


@app.route("/api/dummy", methods=["GET"])
def dummy():
    return HTTPResponse("HELLO WORLD")
