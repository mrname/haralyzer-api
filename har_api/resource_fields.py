from flask.ext.restful import fields

page_fields = {
    'id': fields.Integer,
    'test_id': fields.Integer,
    'page_id': fields.String,
    'startedDateTime': fields.DateTime,
    'hostname': fields.String,
    'url': fields.String,
    'time_to_first_byte': fields.Float,
    'html_load_time': fields.Float,
    'video_load_time': fields.Float,
    'audio_load_time': fields.Float,
    'js_load_time': fields.Float,
    'css_load_time': fields.Float,
    'image_load_time': fields.Float,
    'page_load_time': fields.Float,
    'page_size': fields.Float,
    'image_size': fields.Float,
    'css_size': fields.Float,
    'text_size': fields.Float,
    'js_size': fields.Float,
    'audio_size': fields.Float,
    'video_size': fields.Float,
}

test_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'hostname': fields.String,
    'startedDateTime': fields.DateTime,
    'browser_name': fields.String,
    'browser_version': fields.String,
    'pages': fields.Nested(page_fields, allow_null=True, attribute='pages')
}

test_collection_fields = {
    'tests': fields.Nested(test_fields, allow_null=True)
}
