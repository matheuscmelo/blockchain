from flask_restful import Resource
from blockchain import Blockchain

class BlockchainController(Resource):

	blockchain = Blockchain()

	def get(self):
		return {'hello':'oi'}
