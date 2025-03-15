class HttpResponse:
    def __init__(self, code, data, msg):
        self.code = code
        self.data = data
        self.msg = msg

    def to_dict(self):
        return self.__dict__


class HttpStatus:
    """
    状态码
    """
    # 常规
    OK = 200

    # 客户端错误
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    FIELD_ERROR = 410

    # 服务器错误
    INTERNAL_SERVER_ERROR = 500
