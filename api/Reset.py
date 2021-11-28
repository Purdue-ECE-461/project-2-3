import Flask-RESTful
class Reset(Resource):
    import firestore
    import Packages
    
    def delete(self): #RegistryReset
        auth = None
        auth = request.headers.get("X-Authorization")
        if(auth == None):
            e = new Error()
            return e.set("You do not have permission to reset the registry.", 401)
        
        firestore.delete_all_package_modules()
        return Packages.delete_all()