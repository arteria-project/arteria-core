import os

from arteria.web.app import AppService
from unittest import TestCase


class AppServiceTest(TestCase):

    this_file_path = os.path.dirname(os.path.realpath(__file__))

    def test_can_load_configuration(self):
        app_svc = AppService.create(
                product_name="arteria-test",
                config_root="{}/../templates/".format(self.this_file_path))
        self.assertIsNotNone(app_svc.config_svc)
        app_config = app_svc.config_svc.get_app_config()
        logger_config = app_svc.config_svc.get_logger_config()

        self.assertEquals(app_config["port"], 10000)
        self.assertEquals(logger_config["version"], 1)
