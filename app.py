from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from controllers import BlockListController, TransactionController, BlockchainController, NeighbourController, BlockDetailController

app = Flask(__name__)
api = Api(app)
cors = CORS(app)

api.add_resource(BlockListController, '/')
api.add_resource(TransactionController, '/blockchain')
api.add_resource(BlockchainController, '/blockchain/closeblock')
api.add_resource(NeighbourController, '/neighbours')
api.add_resource(BlockDetailController, '/blockchain/block/<int:index>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)
