from flask import current_app as app
from flask import jsonify, request

import json

@app.route('/api/dummy', methods=["POST"])
def dummy() :
    data = request.json
    print(data)
    