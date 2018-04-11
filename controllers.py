from flask import request
from flask_restful import Resource
from blockchain import Blockchain, Block
from flask_restful import marshal_with

class BlockchainHolder:
	blockchain = Blockchain()

class BlockListController(Resource):

	blockchain = BlockchainHolder.blockchain

	@marshal_with(Block.api_fields)
	def get(self):
		return self.blockchain.to_list

class TransactionController(Resource):

	blockchain = BlockchainHolder.blockchain

	def post(self):
		data = request.get_json()
		self.blockchain.add_transaction(data["sender"], data["receiver"], float(data["amount"]))
		return data

class BlockchainController(Resource):

	blockchain = BlockchainHolder.blockchain

	def post(self):
		self.blockchain.close_last_block()
		return {}