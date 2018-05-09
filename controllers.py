from flask import request
from flask_restful import Resource
from blockchain import Blockchain, Block, Transaction
from flask_restful import marshal_with
from node import Node

class BlockchainHolder:
	node = Node()

class BlockListController(Resource):

	node = BlockchainHolder.node

	@marshal_with(Block.api_fields)
	def get(self):
		return self.node.to_list()

class TransactionController(Resource):

	node = BlockchainHolder.node

	@marshal_with(Transaction.api_fields)
	def post(self):
		data = request.get_json()
		self.node.add_neighbour(request.remote_addr)
		if("hash" in data and "timestamp" in data):
			return self.node.add_transaction(data["sender"], data["receiver"], float(data["amount"]), timestamp=data["timestamp"], thash=data["hash"])
		return self.node.add_transaction(data["sender"], data["receiver"], float(data["amount"]))
		

class BlockchainController(Resource):

	node = BlockchainHolder.node

	def put(self):
		data = {}
		
		if request.data: data = request.get_json()

		if "index" in data:
			print (data["index"]) 
			self.node.close_last_block(data["index"])
		else:
			self.node.close_last_block()
		self.node.add_neighbour(request.remote_addr)
		return {}

class NeighbourController(Resource):

	node = BlockchainHolder.node

	def get(self):
		return list(self.node.neighbours)

class BlockDetailController(Resource):

	node = BlockchainHolder.node

	@marshal_with(Block.api_fields)
	def get(self, index):
		return self.node.get_block(index)

