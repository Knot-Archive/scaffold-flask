from flask.json import JSONEncoder
from bson import ObjectId


class MongoJSONEncoder(JSONEncoder):
    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(o, ObjectId):
            return str(o)
        return JSONEncoder.default(self, o)


"""
def create_app():
    app = Flask(__name__)
    app.json_encoder = MongoJSONEncoder
    app.url_map.converters['objectid'] = ObjectIdConverter
    return app
    
reference
https://stackoverflow.com/questions/16586180/typeerror-objectid-is-not-json-serializable
"""
