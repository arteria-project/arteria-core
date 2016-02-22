import os

from arteria.web.app import AppService
from unittest import TestCase

class AppServiceTest(TestCase):

    this_file_path = os.path.dirname(os.path.realpath(__file__))

    def test_can_load_configuration(self):
        app_svc = AppService.create("arteria-test", "{}/../templates/".format(self.this_file_path))
        self.assertIsNotNone(app_svc.config_svc)
        app_config = app_svc.config_svc.get_app_config()
        logger_config = app_svc.config_svc.get_logger_config()
        self.assertTrue(app_config["port"] == 10000)
        self.assertTrue(logger_config["version"] == 1)
