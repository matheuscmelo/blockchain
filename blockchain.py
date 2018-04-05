class Transaction:
	def __init__(self, sender, receiver, amount):
		self.sender = sender
		self.receiver = receiver
		self.amount = amount

class Block:
	def __init__(self, block_before=None, next_block=None):
		self.transactions = []
		self.block_before = block_before
		self.next_block = next_block

	def add_transaction(self, transaction):
		self.transactions.append(transaction)

class Blockchain:
	def __init__(self, genesis=None):
		self.genesis = genesis
		self.last_block = genesis

	def size(self):
		block = self.genesis
		size = 0
		while(block):
			size += 1
			block = block.next_block
		return size

	def add_block(self, block):
		if(self.last_block):
			self.last_block.next_block = block
			self.last_block = block
		else:
			self.genesis = block
			self.last_block = block

	def is_valid(self):
		return True

	def new_blockchain(self, blockchain):
		if blockchain.is_valid and blockchain.size() > self.size():
			self.genesis = blockchain.genesis
			self.last_block = blockchain.last_block