class AuthenticationRequest(object):
    import User
    import UserAuthenticationInfo
    self.User = new User()
    self.Secret = new UserAuthenticationInfo()
    def get_data():
        return self
    def set_data(data):
        self.User = data["User"]
        self.Secret = data["Secret"]
        return self