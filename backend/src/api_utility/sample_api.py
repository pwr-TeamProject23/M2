from backend.src.api_utility.api import BaseRestApi, BaseRestEndpoint, BaseRestService


class SampleEndpoint(BaseRestEndpoint):
    pass


class SampleRestService(BaseRestService):
    pass


class SampleRestApi(BaseRestApi):
    pass


SAMPLE_API = SampleRestApi()
SAMPLE_API["auth"] = SampleRestService(
    "auth", [SampleEndpoint("authenticate", "/auth/token", "POST")],
)
SAMPLE_API["sample_endpoint"] = SampleRestService(
    "sample_endpoint", [SampleEndpoint("get", "/sample_endpoint")]
)
