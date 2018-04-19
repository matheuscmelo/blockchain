# coding: utf-8
import hashlib
from flask_restful import fields
from datetime import datetime
from node import Notifier
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
		else: self.timestamp = datetime.now()
		
		if not thash: self.hash = self.calculate_hash()
		else: self.hash=thash 

	def calculate_hash(self):
		bhash = hashlib.sha256()
		bhash.update(self.sender.encode('utf-8'))
		bhash.update(self.receiver.encode('utf-8'))
		bhash.update(str(self.amount).encode('utf-8'))
		bhash.update(str(self.timestamp).encode('utf-8'))
		return bhash.hexdigest()

	def __hash__(self):
		return self.hash

class Block:

	notifier = Notifier()

	api_fields = {
		'hash': fields.String,
		'index': fields.Integer,
		'transactions': fields.Nested(Transaction.api_fields)
	}

	def __init__(self, block_before=None, next_block=None, index=0):
		self.index = index
		self.transactions = []
		self.block_before = block_before
		self.next_block = next_block
		self.hash = ''
		self.is_closed = False

	def add_transaction(self, sender, receiver, amount):
		transaction = Transaction(sender, receiver, amount)
		if transaction not in self.transactions:
			self.transactions.append(transaction)
			# self.notifier.notify_transaction(transaction)
		return transaction

	def close(self):
		self.hash = self.calculate_hash()
		self.is_closed = True

	def calculate_hash(self):
		bhash = hashlib.sha256()
		bhash.update(str(self.index).encode('utf-8'))
		for transaction in self.transactions:
			bhash.update(transaction.hash.encode('utf-8'))

		if self.block_before: bhash.update(block_before.hash)

		return bhash.hexdigest()

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
			if bhash != block.hash: return False
			block = block.next_block

		return True

	def close_last_block(self):
		block = self.last_block
		self.add_block(Block())
		block.close()

	def add_transaction(self, sender, receiver, amount):
		return self.last_block.add_transaction(sender, receiver, amount)

	def new_blockchain(self, blockchain):
		if blockchain.is_valid() and blockchain.size() > self.size():
			self.genesis = blockchain.genesis
			self.last_block = blockchain.last_block