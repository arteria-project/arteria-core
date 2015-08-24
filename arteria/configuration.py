import logging
import yaml
import threading

class ConfigurationService:
    def __init__(self, logger=None, logger_config_path=None, app_config_path=None):
        """
        Initializes a configuration service

        :param logger: The logger instance to use. Will default to one named like the module
        :param logger_config_path: The path to the logger config file
        :param app_config_path: The path to the application specific config file

        Usage example:
        config_svc = ConfigurationService(logger_config_path="/opt/product/etc/logger.config",
                                          app_config_path="/opt/product/etc/app.config")

        # The app config and logger config will now be accessible through:
        config_svc.get_app_config()
        config_svc.get_logger_config()

        # Config files are cached in-memory
        # The config files should be YAML
        """
        self._logger = logger or logging.getLogger(__name__)
        self._logger_config_path = logger_config_path
        self._app_config_path = app_config_path
        self._cache_lock = threading.Lock()
        self._cache = {}

    def get_app_config(self):
        """Returns the application specific config file"""
        return self._load_config_file(self._app_config_path)

    def get_logger_config(self):
        """Returns the logger config file"""
        return self._load_config_file(self._logger_config_path)

    def __getitem__(self, key):
        """Returns the value for the key from the app config"""
        app_config = self.get_app_config()
        return app_config[key]

    def _load_config_file(self, path, from_cache=True):
        """Loads the config file, possibly from cache"""
        must_fetch = lambda: (not from_cache) or (path not in self._cache)
        if must_fetch():
            # TODO: Code review threading code
            with self._cache_lock:
                if must_fetch():
                    config_file = ConfigurationService.read_yaml(path)
                    self._cache[path] = config_file
                    self._logger.info("Read config file from {0}, format={1}, from_cache={2}"
                                      .format(path, format, from_cache))
        return self._cache[path]

    @staticmethod
    def read_yaml(path):
        """Deserializes the content of the yaml file"""
        with open(path, 'r') as f:
            config = yaml.load(f.read())
            return config
