from flask import Flask
from flask_restful import Api
from controllers import BlockListController, TransactionController, BlockchainController, NeighbourController

app = Flask(__name__)
api = Api(app)

api.add_resource(BlockListController, '/')
api.add_resource(TransactionController, '/blockchain')
api.add_resource(BlockchainController, '/blockchain/closeblock')
api.add_resource(NeighbourController, '/neighbours')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)