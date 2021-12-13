class Error(object):
    code = 5
    message = "test"
    
    def get(self):
        return {'message': message}, code
    
    def set(self, message, code):
        self.message = message
        self.code = code
        return {'message': message}, code
    
    def malformed(self):
        return self.set("Malformed request.", 400)
    def unexpected(self):
        return {"code": -1, "message": "An error occurred while retrieving package"}, 500