#!env/bin/python
from functools import update_wrapper
from flask import request, Response
import requests


def authenticate(configuration):

    def headers_contain_correct_secret(headers):
        passed_secret = headers.get('auth-secret')
        expected_secret = configuration.get('AUTHENTICATION_SECRET')
        return passed_secret == expected_secret

    def send_unauthorized_access_text(request):
        text_content = buildTextContext(request)
        url = configuration.get('MY_HOUSE_URL') + '/house/notification'
        post_data = {"messageContent": text_content}
        requests.post(url, json=post_data, verify=False)


    def buildTextContext(request):
        data = []
        data.append('method: ' + str(request.method))
        data.append('path: ' + str(request.path))
        data.append('url: ' + str(request.url))
        data.append('headers: ' + str(request.headers))
        data.append('cookies: ' + str(request.cookies))
        data.append('environ: ' + str(request.environ))
        data.append('data: ' + str(request.data))
        data.append('form: ' + str(request.form))
        data.append('args: ' + str(request.args))
        data.append('values: ' + str(request.values))
        data.append('stream: ' + str(request.stream))
        data.append('files: ' + str(request.files))
        data.append('full_path: ' + str(request.full_path))
        data.append('script_root: ' + str(request.script_root))
        data.append('base_url: ' + str(request.base_url))
        data.append('url_root: ' + str(request.url_root))
        data.append('path: ' + str(request.path))
        data.append('full_path: ' + str(request.full_path))
        data.append('script_root: ' + str(request.script_root))
        data.append('base_url: ' + str(request.base_url))
        data.append('url: ' + str(request.url))
        data.append('url_root: ' + str(request.url_root))
        data.append('blueprint: ' + str(request.blueprint))
        data.append('endpoint: ' + str(request.endpoint))
        if request.method != 'GET':
            data.append('json: ' + str(request.json))
        data.append('max_content_length: ' + str(request.max_content_length))
        data.append('routing_exception: ' + str(request.routing_exception))
        data.append('url_rule: ' + str(request.url_rule))
        data.append('view_args: ' + str(request.view_args))
        data.append(str(request))

        print("An unauthorized request was made to the House of Pi application:\n" + "\n".join(data))
        return "An unauthorized request was made to the House of Pi application:\n" + "\n".join(data)

    def decorator(f):

        def decorated(*args, **kwargs):
            if headers_contain_correct_secret(request.headers):
                return f(*args, **kwargs)
            else:
                send_unauthorized_access_text(request)
                return Response('Get out of my house.  I will press charges.', 401)

        return update_wrapper(decorated, f)

    return decorator
