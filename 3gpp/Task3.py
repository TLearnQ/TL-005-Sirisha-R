import logging

logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp":"%(asctime)s","level":"%(levelname)s","module":"%(name)s","message":"%(message)s"}',
   
)
logger = logging.getLogger("Client")
class APIResponseError(Exception):
    def __init__(self, message, code=None):
        super().__init__(message)
        self.code = code
class MockAPIClient:
    def __init__(self, auth_type=None):
        self.auth_type = auth_type
    def call_api(self, endpoint):
        try:
            if self.auth_type not in ["Bearer", None]:
                raise APIResponseError("Unsupported auth type", "UNSUPPORTED_AUTH")
            if endpoint == "/ok":
                response = {"status": 200, "schema": {"type": "object"}}
            elif endpoint == "/no-schema":
                response = {"status": 200, "schema": None}
            else:
                response = {"status": 500, "schema": {"type": "object"}}
            if response["status"] != 200:
                raise APIResponseError(
                    f"Bad status {response['status']}", "BAD_STATUS"
                )
            if not response["schema"]:
                raise APIResponseError("Missing schema", "MISSING_SCHEMA")
            logger.info(f"API call successful: {endpoint}")
            return response
        except APIResponseError as e:
            logger.error(f"{e} | ExceptionCode={e.code}")
client = MockAPIClient(auth_type="Bearer")
client.call_api("/ok")
client.call_api("/no-schema")
client.call_api("/unknown")
client_bad_auth = MockAPIClient(auth_type="OAuth2")
client_bad_auth.call_api("/ok")
