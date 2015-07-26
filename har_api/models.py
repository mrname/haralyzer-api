import json

from dateutil import parser as date_parser
from flask.ext.sqlalchemy import SQLAlchemy
from haralyzer import HarParser, HarPage
from sqlalchemy import func

db = SQLAlchemy()


class Test(db.Model):
    """
    Represents one 'test run' which could contain multiple pages.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=True)
    data = db.Column(db.Text, nullable=False)
    hostname = db.Column(db.String(256), nullable=False)
    startedDateTime = db.Column(db.DateTime, nullable=True)
    browser_name = db.Column(db.String(20), nullable=True)
    browser_version = db.Column(db.String(10), nullable=True)
    pages = db.relationship('Page', backref='test',
                            cascade='all, delete-orphan')

    def __init__(self, data, name=None):
        """
        :param data: String of JSON data representing a HAR test run
        :type data: String
        :param name: Optional string of a custom name for the test
        :type name: String
        """
        self.data = data
        self.name = name
        self.har_parser = HarParser(har_data=json.loads(self.data))
        self.browser_name = self.har_parser.browser['name']
        self.browser_version = self.har_parser.browser['version']
        self.hostname = self.har_parser.hostname
        # A bit of a hack here, grabbing the start time of the first page
        start = date_parser.parse(self.har_parser.pages[0].startedDateTime)
        self.startedDateTime = start

    def save(self):
        self.data = func.compress(self.data)
        db.session.add(self)
        # Need to save it to get the test ID
        db.session.commit()
        for page in self.har_parser.pages:
            p = Page(self.id, page.page_id, self.har_parser)
            db.session.add(p)
        db.session.commit()


class Page(db.Model):
    """
    Represents one page from a test run.
    """
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable=False)
    page_id = db.Column(db.String(64), nullable=False)
    hostname = db.Column(db.String(256))
    time_to_first_byte = db.Column(db.Float)
    html_load_time = db.Column(db.Float)
    video_load_time = db.Column(db.Float)
    audio_load_time = db.Column(db.Float)
    js_load_time = db.Column(db.Float)
    css_load_time = db.Column(db.Float)
    image_load_time = db.Column(db.Float)
    page_load_time = db.Column(db.Float)
    page_size = db.Column(db.Float)
    image_size = db.Column(db.Float)
    css_size = db.Column(db.Float)
    text_size = db.Column(db.Float)
    js_size = db.Column(db.Float)
    audio_size = db.Column(db.Float)
    video_size = db.Column(db.Float)

    attrs = ['hostname']

    load_times = ['time_to_first_byte', 'html_load_time', 'video_load_time',
                  'video_load_time', 'audio_load_time', 'js_load_time',
                  'css_load_time', 'image_load_time', 'page_load_time']

    page_sizes = ['page_size', 'css_size', 'image_size', 'text_size', 'js_size',
                  'audio_size', 'video_size']

    har_page_fields = attrs + load_times + page_sizes

    def __init__(self, test_id, page_id, har_parser=None):
        """
        :param test_id: Maps to the ID of the full test run containing the page
        :type test_id: Integer
        :param page_id: ID of the page
        :type test_id: String
        :param har_parser: Optional instance of a `HarParser` object
        :type har_parser: HarParser
        """
        self.test_id = test_id
        self.page_id = page_id
        if har_parser is None:
            # TODO - Load the data from the test object and make a harparser
            pass
        else:
            self.har_parser = har_parser
        self.har_page = HarPage(self.page_id, self.har_parser)
        self._map_page_to_model()

    def _map_page_to_model(self):
        """
        Helper function that maps our HarPage object to the DB model.
        """
        for field in self.har_page_fields:
            if getattr(self.har_page, field, None) is not None:
                setattr(self, field, getattr(self.har_page, field))
