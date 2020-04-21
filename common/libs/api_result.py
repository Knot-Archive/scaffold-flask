from flask import jsonify


def api_result(code=200, message="success", data=None, total=None):
    result = {
        "code": code,
        "message": message,
        "data": data,
        "total": total
    }

    for key in ("data", "total"):
        if not result[key]:
            result.pop(key)
    return result
    # return jsonify(result)
