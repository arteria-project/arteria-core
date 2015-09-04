import tornado.web
import jsonpickle

class BaseRestHandler(tornado.web.RequestHandler):
    """
    A request handler for a REST web interface, taking care of
    writing and reading JSON request/responses
    """

    def data_received(self, chunk):
        raise NotImplementedError("Should be implemented by subclass!")

    def write_object(self, obj):
        """
        Writes the object as JSON

        Only dictionaries or objects containing the __dict__ attribute get serialized.
        """
        if isinstance(obj, dict):
            resp = obj
        elif hasattr(obj, "__dict__"):
            resp = obj.__dict__
        else:
            raise TypeError("The object needs either to be a dict or have the __dict__ attribute")

        # Send to Tornado, which handles the json serialization and content-type header
        self.write(resp)

    def write_json(self, json):
        self.set_header("Content-Type", "application/json")
        self.write(json)

    def body_as_object(self, required_members=[]):
        """Returns the JSON encoded body as a Python object"""
        obj = jsonpickle.decode(self.request.body)
        for member in required_members:
            if member not in obj:
                raise tornado.web.HTTPError("400", "Expecting '{0}' in the JSON body".format(member))
        return obj

    def api_link(self, version="1.0"):
        return "%s://%s/api/%s" % (self.request.protocol, self.request.host, version)

class LogLevelHandler(BaseRestHandler):
    """
    Handles getting/setting the log_level of the running application
    """
    def initialize(self, app_svc):
        self.app_svc = app_svc

    def get(self):
        """
        Get the current log_level of the running server
        """
        log_level = self.app_svc.get_log_level()
        self.write_object({"log_level": log_level})

    def put(self):
        """
        Set the current log_level of the running server. Call with e.g. {'log_level': 'DEBUG'}
        """
        json_body = self.body_as_object(["log_level"])
        log_level = json_body["log_level"]
        self.app_svc.set_log_level(log_level)
        self.write_object({"log_level": log_level})

class ApiHelpHandler(BaseRestHandler):
    """
    Handles requests for the api help, available at the root of the application
    """
    def initialize(self, route_svc):
        self.route_svc = route_svc

    def get(self):
        """Returns the help for the API"""
        base_url = "{0}://{1}".format(self.request.protocol, self.request.host)
        help_doc = self.route_svc.get_help(base_url)
        self.write_object(help_doc)


