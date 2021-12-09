from flask import Flask
from flask_classful import FlaskView
app = Flask(__name__)
class Authenticate(FlaskView):
    import User
    import UserAuthenticationInfo
    
    @route('/authenticate/')
    def put(self):
        return 501
    
Authenticate.register(app)