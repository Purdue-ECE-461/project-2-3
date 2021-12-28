class User(object):
    name = None
    isAdmin = True
    def get_data():
        return self
    def set_data(data):
        self.name = data["name"]
        self.isAdmin = data["isAdmin"]
        return self
    def get_name():
        return self.name
    def get_isAdmin():
        return self.isAdmin