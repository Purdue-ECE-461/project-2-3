class Error(object):
    code = 5
    message = "test"
    
    def get(self):
        return {'message': message}, code
    
    def set(message, code):
        self.message = message
        self.code = code
        return {'message': message}, code
    