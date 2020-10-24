from abc import abstractmethod

from flask import make_response, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError


class MethodCaller(MethodView):

    @property
    def request(self):
        return request

    @property
    def request_body(self):
        return request.get_json()

    def _handle(self, *args, **kwargs):
        try:
            response = self.worker(*args, **kwargs)
            if isinstance(response, dict):
                response = self.make_response(response)
                return response
        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': 'Error'
            }
            return self.make_response(response_object, 503)

    def make_response(self, data: dict, status_code: int = 200):
        return make_response(jsonify(data)), status_code


class NonSecurePostCaller(MethodCaller):

    @abstractmethod
    def worker(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        return self._handle(*args, **kwargs)


class PostCaller(MethodCaller):

    @abstractmethod
    def worker(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        try:
            verify_jwt_in_request()
        except NoAuthorizationError:
            return self.make_response({
                'error': 'User Not Authorize'
            }, 403)
        return self._handle(*args, **kwargs)


class GetCaller(MethodCaller):

    @abstractmethod
    def worker(self, *args, **kwargs):
        pass

    def get(self, *args, **kwargs):
        try:
            verify_jwt_in_request()
        except NoAuthorizationError:
            return self.make_response({
                'error': 'User Not Authorize'
            }, 403)
        return self._handle(*args, **kwargs)
