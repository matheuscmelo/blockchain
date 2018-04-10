from flask_restful import Resource
from blockchain import Blockchain, Block
from flask_restful import marshal_with
class BlockchainController(Resource):

	blockchain = Blockchain()

	@marshal_with(Block.api_fields)
	def get(self):
		self.blockchain.add_block(Block())
		return self.blockchain.to_list
