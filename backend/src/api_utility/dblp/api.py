from backend.src.api_utility.api import BaseRestApi, BaseRestEndpoint, BaseRestService


class BaseDblpEndpoint(BaseRestEndpoint):
    pass


class BaseDblpService(BaseRestService):
    pass


class BaseDblpApi(BaseRestApi):
    pass


DBLP_API = BaseDblpApi()
DBLP_API["author"] = BaseDblpService("author", [BaseDblpEndpoint("get", "/")])
