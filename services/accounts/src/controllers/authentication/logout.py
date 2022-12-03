from flask import jsonify


def controller():
    res = jsonify(message="Logout Successful")
    res.delete_cookie(
        'user-token',
        path='/',
        httponly=True,
    )
    return res, 200
