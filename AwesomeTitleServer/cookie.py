from flask import request, make_response


def get_cookie(name):
    # TODO: safety check for 'now in request'
    return request.cookies.get(name)


def add_cookies(cookies, ret=('', 200)):
    # TODO: typing check
    resp = make_response(ret)
    for key, value in cookies.items():
        resp.set_cookie(key, value)
    return resp


def del_cookie(key, ret):
    # TODO: typing ceck
    resp = make_response(ret)
    resp.set_cookie(key, None)
    return resp
