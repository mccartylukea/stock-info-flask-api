from flask import jsonify

class NoReturnPayload(Exception):
    status_code = 404
    message = 'Invalid API call. Check that the stock symbol is correct.'
    def __init__(self):
        Exception.__init__(self)

    def to_dict(self):
        output = {'status_code': self.status_code, 'message': self.message}
        return output