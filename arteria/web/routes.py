import threading
import re
import itertools


class RouteInfo:
    """Information about a method in a route"""
    def __init__(self, route, method, description):
        self.route = route
        self.method = method
        self.description = description

    def __repr__(self):
        return "[{0} method={1}: {2}]".format(self.route, self.method, self.description)


class RouteService:
    """Encapsulates Tornado routes and generates help from their class definitions"""

    def __init__(self, app_svc, debug):
        """
        Initialize the route service. Routes need to be set via set_routes.

        :param routes: A list of tuples with tornado routing definitions
        :param debug: True if debugging
        """
        self._app_svc = app_svc
        self._debug = debug
        self._help_generated_lock = threading.Lock()
        self._help_generated = False

        # NOTE: The routes are not set in the constructor because a reference
        # to the route service is needed in the api help route handler
        self._routes = None

    def set_routes(self, routes):
        self._routes = routes

    def get_routes(self):
        return self._routes

    def get_help(self, base_url):
        """Returns the API help based on the routes"""
        return self._generate_help(False, base_url)

    def _get_route_infos(self, tornado_routes, base_url):
        """
        Generates RouteInfo objects from routes. Help is generated
        by inspecting the route handlers.

        Returns nothing if no documentation is found.
        """
        if tornado_routes is None:
            raise RoutesNotSetError("Routes must be set before RouteInfos can be generated")

        for tornado_route in tornado_routes:
            route = tornado_route[0]
            cls = tornado_route[1]
            for method_name in "get", "post", "put", "delete":
                doc = self._doc_string_from_class_attribute(cls, method_name)
                if doc is not None:
                    yield RouteInfo("{0}{1}".format(base_url, route), method_name, doc)

    def _doc_string_from_class_attribute(self, cls, attr_name):
        """
        Returns the doc string for the attribute

        Ignores the documentation if it has the undocumented attribute
        and is not running in debug mode
        """
        attr = getattr(cls, attr_name)
        doc = attr.__doc__
        is_undocumented = hasattr(attr, "undocumented")

        # Return the documentation if available. Skip it if it should be
        # undocumented, unless in debug mode.
        if (doc is not None) and (not is_undocumented or self._debug):
            doc = doc.strip()
            doc = re.sub(r'\s+', ' ', doc)
            if is_undocumented:
                doc = "(UNDOCUMENTED): {0}".format(doc)
            return doc

    def _get_route_infos_grouped(self, tornado_routes, base_url):
        """
        Returns the method help strings grouped by route, e.g.:

        route: <url>
        methods:
            get: "help string for get"
            put: "help string for put"
            ...
        """
        route_infos = list(self._get_route_infos(tornado_routes, base_url))
        by_route = lambda entry: entry.route
        route_infos_sorted = sorted(route_infos, key=by_route)
        grouped = itertools.groupby(route_infos_sorted, key=by_route)
        routes = []
        for key, groups in grouped:
            route_info = {"route": key}
            methods = dict()
            for group in groups:
                methods[group.method] = group.description
            route_info["methods"] = methods
            routes.append(route_info)
        routes = sorted(routes, key=lambda item: item["route"])
        return routes

    def _generate_help(self, regenerate, base_url):
        """Generates help from self._routes"""
        if not self._help_generated or regenerate:
            with self._help_generated_lock:
                if not self._help_generated:
                    self._route_infos = self._get_route_infos_grouped(self._routes, base_url)
                    self._help_generated = True
        return self._route_infos

class RoutesNotSetError(Exception):
    pass
