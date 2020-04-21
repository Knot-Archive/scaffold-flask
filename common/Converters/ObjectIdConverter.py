from bson import ObjectId
from werkzeug.routing import BaseConverter


class ObjectIdConverter(BaseConverter):
    """
    example https://github.com/Fischerfredl/flask-objectid-converter
    like this:
        app = Flask(__name__)
        app.url_map.converters['objectid'] = ObjectIDConverter
        @app.route('/users/<objectid:oid>')
        def get_user(oid):
            return User.objects.get(id=oid)
    """

    def to_python(self, value):
        return ObjectId(value)

    def to_url(self, value):
        return str(value)
