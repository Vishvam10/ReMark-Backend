import datetime
from flask.json import JSONEncoder
from flask import current_app as app


class CustomJSONEncoder(JSONEncoder):
  "Add support for serializing timedeltas"

  def default(o):
    if type(o) == datetime.timedelta:
      return str(o)
    elif type(o) == datetime.datetime:
      return o.isoformat()
    else:
      return super().default(o)

app.json_encoder = CustomJSONEncoder 