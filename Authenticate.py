from flask_restful import Resource, request, reqparse
class Authenticate(Resource):
    import User
    import UserAuthenticationInfo
    def put(self):
        return 501