from flask.ext.restful import fields

page_fields = {
    'test_id': fields.Integer,
    'page_id': fields.String,
    'hostname': fields.String,
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
    'name': fields.String,
    'data': fields.String,
    'hostname': fields.String,
    'startedDateTime': fields.String,
    'browser_name': fields.String,
    'browser_version': fields.String,
}