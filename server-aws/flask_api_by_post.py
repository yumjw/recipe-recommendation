from flask import Flask
from flask import request
import json
import modules
from flask_cors import CORS

app = Flask(__name__)
print('reassign completed')
cors = CORS(app)
#CORS(app,resources={r'*': {'origins': '*'}})


@app.route('/recipes/', methods=['POST'])
def return_recipes():
    print(request)
    json_data = request.get_json()
    print(json_data)
    print(type(json_data))
    model = modules.recipe_recomm(user_musts=json_data['user_musts'], user_options=json_data['user_options'])
    data = model.return_output()

    return json.dumps(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)