# coding: utf-8
import hashlib
from flask_restful import fields
from datetime import datetime
class Transaction:

	api_fields = {
		'sender': fields.String,
		'receiver': fields.String,
		'amount': fields.Float,
		'timestamp': fields.String,
		'hash': fields.String
	}

	def __init__(self, sender, receiver, amount, timestamp=None, thash=None):
		self.sender = sender
		self.receiver = receiver
		self.amount = amount
		if timestamp: self.timestamp = timestamp
		else: self.timestamp = str(datetime.now())
		
		if not thash: self.hash = self.calculate_hash()
		else: self.hash=thash 

	def calculate_hash(self):
		bhash = hashlib.sha256()
		bhash.update(self.sender.encode('utf-8'))
		bhash.update(self.receiver.encode('utf-8'))
		bhash.update(str(self.amount).encode('utf-8'))
		bhash.update(self.timestamp.encode('utf-8'))
		return bhash.hexdigest()

	def __eq__(self, other):
		return self.hash == other.hash

class Block:

	api_fields = {
		'hash': fields.String,
		'index': fields.Integer,
		'transactions': fields.Nested(Transaction.api_fields)
	}

	def __init__(self, next_block=None, index=0):
		self.index = index
		self.transactions = []
		self.next_block = next_block
		self.hash = ''
		self.is_closed = False 

	def add_transaction(self, sender, receiver, amount, timestamp, thash):
		transaction = Transaction(sender, receiver, amount, timestamp, thash)
		if transaction not in self.transactions:
			self.transactions.append(transaction)
			return transaction, True
		return transaction, False

	def close(self):
		self.hash = self.calculate_hash()
		self.is_closed = True

	def calculate_hash(self):
		bhash = hashlib.sha256()
		bhash.update(str(self.index).encode('utf-8'))
		for transaction in self.transactions:
			bhash.update(transaction.hash.encode('utf-8'))
		return bhash.hexdigest()

	def size(self):
		return len(self.transactions)

class Blockchain:

	def __init__(self, genesis=Block()):
		self.genesis = genesis
		self.last_block = genesis

	@property
	def to_list(self):
		blocks = []
		block = self.genesis
		while block:
			blocks.append(block)
			block = block.next_block
		return blocks

	def size(self):
		block = self.genesis
		size = 0
		while block:
			size += 1
			block = block.next_block
		return size

	def add_block(self, block):
		if not self.last_block.is_closed:
			block.index = self.size()
			if(self.last_block):
				self.last_block.next_block = block
				self.last_block = block
			else:
				self.genesis = block
				self.last_block = block

	def is_valid(self):
		block = self.genesis

		while block:
			bhash = block.calculate_hash()

			if block.hash: 
				if bhash != block.hash: return False
			block = block.next_block

		return True

	def close_last_block(self, index=None): 
		if int(index) == self.last_block.index:
			block = self.last_block
			block_index = block.index
			self.add_block(Block())
			block.close()
			return block
		return None

	def add_transaction(self, sender, receiver, amount, timestamp=None, thash=None):
		return self.last_block.add_transaction(sender, receiver, amount, timestamp, thash)

	def new_blockchain(self, blockchain):
		print(blockchain.last_block.size())
		if blockchain.is_valid() and blockchain.size() >= self.size():
			self.genesis = blockchain.genesis
			self.last_block = blockchain.last_block

	def get_block(self, index):
		block = self.genesis
		while block:
			if block.index == index: return block
			block = block.next_block 
		return None