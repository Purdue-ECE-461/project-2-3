from flask import Flask
from flask_restful import Resource, Api, request, reqparse
import pandas as pd
import ast
import Packages
import Reset
import Package

app = Flask(__name__)
api = Api(app)
api.add_resource(Packages, '/packages')
api.add_resource(Reset, '/reset')
api.add_resource(Packages.get_package_by_ID(id), '/package/{id}')
api.add_resource(Package, '/package')
api.add_resource(PackageRating.rate_by_ID(id), '/package/{id}/rate')
api.add_resource(Authenticate, '/authenticate')
api.add_resource(Packages.get_package_by_Name(Name), '/package/byName/{Name}')
api.add_resource(Packages.delete_package_by_Name(Name), '/package/byName/{Name}')
