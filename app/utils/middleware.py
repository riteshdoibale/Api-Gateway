import uuid

class Middleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        try:
            trackingId = environ.get("HTTP_TRACKINGID", str(uuid.uuid4()))
            environ["HTTP_TRACKINGID"] =  trackingId

            def custom_start_response(status, headers, exc_info=None):
                headers.append(("trackingId", trackingId))
                return start_response(status, headers, exc_info)

            response = self.app(environ, custom_start_response)
            return response
        except Exception as e:
            print("Exception : ", e)