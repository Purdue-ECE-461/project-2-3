from flask import Flask
import responses
import requests
import main
app = Flask(__name__)
if __name__ == "__main__" :
    request = requests.Request("/reset/",
                       headers={"X-Authorization": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"})
    resp = 200
    with app.app_context():
         resp = registryReset()
    print(resp)