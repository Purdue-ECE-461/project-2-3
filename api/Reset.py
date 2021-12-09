from flask import Flask
from flask_classful import FlaskView
app = Flask(__name__)
class Reset(FlaskView):
    import firestore
    import Packages
    
    @route('/reset/')
    def static delete(self): #RegistryReset
        auth = None
        auth = request.headers.get("X-Authorization")
        if(auth == None):
            e = Error()
            return e.set("You do not have permission to reset the registry.", 401)
        
        firestore.delete_all_package_modules()
        return Packages.delete_all()

Reset.register(app)