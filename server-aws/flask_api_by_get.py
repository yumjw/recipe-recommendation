from flask_restful import Resource
from flask_restful import reqparse
from modules import recipe_recomm
import json
import ast
from flask_cors import CORS


class Plus(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('user_musts', required=False, type=str, help='x cannot be blank')
            parser.add_argument('user_options', required=False, type=str, help='y cannot be blank')
            args = parser.parse_args()
            print(args)
            model = recipe_recomm(user_musts=ast.literal_eval(args['user_musts']),
                                  user_options=ast.literal_eval(args['user_options']))

            data = model.return_output()
            return data
        except Exception as e:
            return {'error': str(e)}

from flask import Flask
from flask_restful import Api

app = Flask('My First App')
cors = CORS(app)
api = Api(app)
api.add_resource(Plus, '/plus')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10001, debug=True)