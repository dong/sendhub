class RequestParameterError(Exception):
    def __init__(self, message):
        super(RequestParameterError, self).__init__(message)
        self.message = message

