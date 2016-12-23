from functools import update_wrapper
from flask import request, Response


def authenticate(secret):

    def headers_contain_correct_secret(headers):
        passed_secret = headers.get('auth-secret')
        return passed_secret == secret

    def decorator(f):

        def decorated(*args, **kwargs):
            if headers_contain_correct_secret(request.headers):
                return f(*args, **kwargs)
            else:
                return Response('Get out of my house.  I will press charges.', 401)

        return update_wrapper(decorated, f)

    return decorator
