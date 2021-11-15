from flask_restful import Resource, request, reqparse
class Reset(Resource):
    import firestore
    
    def delete(self): #RegistryReset
        auth = None
        auth = request.headers.get("X-Authorization")
        if(auth == None):
            e = new Error()
            return e.set("You do not have permission to reset the registry.", 401)
        
        firestore.delete_all_package_modules()
        return 200