
class Response(object):
    def __init__(self, text="<html></html>", url="", status_code=600, error_msg=''):
        self.text = text
        self.content = b'<html></html>'
        self.status_code = status_code
        self.url = url
        self.error_msg = error_msg
        self.content = b''

    def json(self):
        return {'url': self.url, 'status_code': self.status_code}