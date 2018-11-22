
import unittest
import mock

from tornado.testing import AsyncHTTPSTestCase
from tornado.web import Application
from tornado.web import URLSpec as url

from arteria.web.handlers import BaseRestHandler
import json


class TestHandlersSerialization(unittest.TestCase):
    def test_cant_deserialize_list(self):
        """
        It shouldn't be possible to deserialize to json lists:
        http://haacked.com/archive/2009/06/25/json-hijacking.aspx/
        """
        handler = BaseRestHandler(mock.MagicMock(), mock.MagicMock())
        obj = "This would be bad".split(' ')
        self.assertRaises(TypeError, handler.write_object, obj)

    def test_can_deserialize_plain_object(self):
        """Sending an non-list/non-dict object to write_object deserializes it as json"""
        handler = BaseRestHandler(mock.MagicMock(), mock.MagicMock())
        handler._write_buffer = []
        obj = SerializeMe()
        obj.key = "value"
        handler.write_object(obj)
        res = json.loads(handler._write_buffer[0])
        self.assertDictEqual(res, {"key": "value"})

    def test_can_deserialize_dict(self):
        handler = BaseRestHandler(mock.MagicMock(), mock.MagicMock())
        handler._write_buffer = []
        obj = {"key": "value"}
        handler.write_object(obj)
        res = json.loads(handler._write_buffer[0])
        self.assertDictEqual(res, {"key": "value"})

    def test_cant_deserialize_tuple(self):
        handler = BaseRestHandler(mock.MagicMock(), mock.MagicMock())
        obj = ("this", "that")
        self.assertRaises(TypeError, handler.write_object, obj)


class SerializeMe:
    pass

