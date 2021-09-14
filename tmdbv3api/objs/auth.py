from tmdbv3api.tmdb import TMDb


class Authentication(TMDb):
    _urls = {
        "create_request_token": "/authentication/token/new",
        "validate_with_login": "/authentication/token/validate_with_login",
        "create_session": "/authentication/session/new",
    }

    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password
        self.expires_at = None
        self.request_token = self._create_request_token()
        self._authorise_request_token_with_login()
        self._create_session()

    def _create_request_token(self):
        """
        Create a temporary request token that can be used to validate a TMDb user login.
        """
        response = self._request_obj(self._urls["create_request_token"])
        self.expires_at = response.expires_at
        return response.request_token

    def _create_session(self):
        """
        You can use this method to create a fully valid session ID once a user has validated the request token.
        """
        response = self._request_obj(
            self._urls["create_session"],
            method="POST",
            data={"request_token": self.request_token}
        )
        self.session_id = response.session_id

    def _authorise_request_token_with_login(self):
        """
        This method allows an application to validate a request token by entering a username and password.
        """
        self._request_obj(
            self._urls["validate_with_login"],
            method="POST",
            data={
                "username": self.username,
                "password": self.password,
                "request_token": self.request_token,
            }
        )
