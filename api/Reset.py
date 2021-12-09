from flask import Flask
from flask_classful import FlaskView, route
import responses
import requests

import firestore as Firestore
app = Flask(__name__)
class Reset(FlaskView):
    excluded_methods = ['delete_all']
    @route('/reset/')
    def delete(self): #RegistryReset
        auth = None
        auth = request.headers.get("X-Authorization")
        if(auth == None):
            e = Error()
            return e.set("You do not have permission to reset the registry.", 401)
        
        Firestore.delete_all_package_modules()
        from Packages import Packages
        p = Packages()
        return p.delete_all()

Reset.register(app)
if __name__ == "__main__" :
    test = Reset()
    request = requests.Request("/reset/",
                       headers={"X-Authorization": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"})
    resp = 200
    with app.app_context():
         resp = test.delete()
    print(resp)