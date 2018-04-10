from flask import Flask
from flask_restful import Api
from controllers import BlockchainController

app = Flask(__name__)
api = Api(app)

api.add_resource(BlockchainController, '/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)