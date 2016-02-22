from unittest import TestCase
import arteria
from arteria.web.routes import RouteService
import mock

class RoutesServiceTest(TestCase):
    def test_help_doc_generated(self):
        app_svc = mock.MagicMock()
        route_svc = RouteService(app_svc, debug=False)
        routes = [
            ("/route0", TestHandler),
            ("/route1", TestHandler)
        ]
        route_svc.set_routes(routes)
        base_url = "http://self"
        help = route_svc.get_help(base_url).get("doc")
        self.assertEqual(len(help), len(routes))

        for index, entry in enumerate(help):
            self.assertEqual(help[index]["route"], "{base_url}/route{index}"
                             .format(base_url=base_url, index=index))
            methods = entry["methods"]
            self.assertEqual(len(methods), 2)
            actual = set([(key, value.split(':')[0] == "True")
                           for key, value in methods.items()])
            expected = set([("get", True), ("delete", True)])
            self.assertEqual(actual, expected)

class TestHandler:
    """Used in RoutesServiceTest.test_help_doc_generated"""
    def get(self):
        """True: Documentation should show up"""
        pass

    def put(self):
        pass  # Documentation should not show up

    @arteria.undocumented
    def post(self):
        """False: Documentation should not show up"""
        pass

    def delete(self):
        """True: Documentation should show up"""
        pass
