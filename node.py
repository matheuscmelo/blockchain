import requests
from threading import Thread
import json
from blockchain import Blockchain
class Node:

	def __init__(self, neighbours=set(), blockchain = Blockchain()):
		self.neighbours = neighbours
		self.neighbours.add('http://206.189.174.49:5000/')
		self.blockchain = blockchain
		if len(self.neighbours) < 8:
			self.ask_new_neighbours(8-len(self.neighbours))

	def notify_neighbours(self, method, url, data={}): 
		for neighbour in self.neighbours:
			Notifier(node=self, url=neighbour + url, method=method, data=data).start()

	def ask_new_neighbours(self, quantity):
		Notifier(node=self, function=NotifierFunctions.get_neighbours).start()
		
	def notify_transaction(self, transaction): 
		self.notify_neighbours(method=requests.post, url="blockchain", data=transaction.__dict__)

	def notify_close_block(self):
		self.notify_neighbours(method=requests.put, url="blockchain/closeblock")

	def to_list(self):
		return self.blockchain.to_list

	def size(self):
		return self.blockchain.size()

	def is_valid(self):
		return self.blockchain.is_valid()

	def close_last_block(self):
		self.blockchain.close_last_block()

	def add_transaction(self, sender, receiver, amount, timestamp=None, thash=None):
		transaction, result = self.blockchain.add_transaction(sender, receiver, amount, timestamp, thash)

		if result:
			self.notify_transaction(transaction)
		return transaction

	def new_blockchain(self, blockchain):
		self.blockchain.new_blockchain(blockchain)


class Notifier(Thread): 

	def __init__(self, node=None, url=None, method=None, data=None, function=None):
		self.node = node
		self.url = url
		self.method = method
		self.data = data
		self.function = function
		Thread.__init__(self)

	def run(self):
		try:
			if self.function:
				self.function(notifier=self, node=self.node, url=self.url, method=self.method, data=self.data, function=self.function)
			else:
				self.method(self.url, json=self.data)
			return True
		except:
			return False
 
	def send(self, method, url, data={}): 
		method(url, json=data)

	def receive(self, url, data=None):
		return requests.get(url, data=data).json()

class NotifierFunctions:

	def get_neighbours(notifier, node, *args, **kwargs):
		new_neighbours = []
		for neighbour in node.neighbours:
			new_neighbours = new_neighbours + notifier.receive(neighbour+"neighbours")
		for neighbour in new_neighbours:
			node.neighbours.add(neighbour)