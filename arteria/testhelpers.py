import time
import requests
import re
import json

import unittest


class BaseRestTest(unittest.TestCase):
    def _base_url(self):
        raise NotImplementedError("The method base url must be implemented")

    def _get_full_url(self, url):
        """Replaces a starting . with base url"""
        return re.sub(r'^\.', self._base_url(), url)

    def _validate_response(self, resp, expect):
        if expect is not None:
            self.assertEqual(resp.status_code, expect)

    def put(self, url, obj=None, expect=200):
        """
        Sends a PUT to the url, with the obj as the body

        A starting '.' is replaced with the base url
        :param obj: A Python object
        :param expect: The expected status code
        """
        json_body = json.dumps(obj)
        full_url = self._get_full_url(url)
        resp = requests.put(full_url, json_body)
        self._validate_response(resp, expect)
        return resp

    def get(self, url, expect=200):
        """
        Gets the item at url and returns a Python object based on the json body (if any).

        A starting '.' is replaced with the base url

        :param expect: The expected status code
        """
        full_url = self._get_full_url(url)
        resp = requests.get(full_url)
        self._validate_response(resp, expect)
        try:
            resp.body_obj = jsonpickle.decode(resp.text)
        except ValueError:
            resp.body_obj = None
        return resp


class TestFunctionDelta:
    """
    Checks the results of the same function call made consecutively
    
    Replaces:
        x1 = f()
        do_something()
        x2 = f()
        assert_equal(x2 - x1, expected_delta)

    with:
        function_delta = TestFunctionDelta(lambda: f(), self)
        do_something()
        function_delta.assert_changed_by(expected_delta)

    which can be somewhat more readable
    """
    def __init__(self, func, asserts, sleep=0):
        """
        Initializes the class with one initial call to func

        :param func: The function being called consecutively
        :param asserts: An object that provides an assertEqual method
        :param sleep: Time to sleep in seconds before asserting
        :return: None
        """
        self._current = None
        self._func = func
        self._asserts = asserts
        self._last = self._func()
        self._start = self._last
        self._sleep = sleep

    def _assert_changed_by(self, expected, compare_to):
        def evaluate():
            self._current = self._func()
            return self._current - compare_to

        actual = evaluate()
        if expected != actual and self._sleep > 0:
            # Evaluate again if sleep is provided. Provided for cases where there may be some latency
            time.sleep(self._sleep)
            actual = evaluate()
        self._asserts.assertEqual(expected, actual)
        self._last = self._current

    def assert_changed_by_total(self, expected):
        """
        Asserts that the result of calling the wrapped function
        has increased by the expected number since first called 

        :param expected: The expected increase since the object was created
        """
        self._assert_changed_by(expected, self._start)

    def assert_changed_by(self, expected):
        """
        Asserts that the result of calling the wrapped function
        has increased by the expected number since last asserted 

        :param expected: The expected increase since last asserted 
        """
        self._assert_changed_by(expected, self._last)

