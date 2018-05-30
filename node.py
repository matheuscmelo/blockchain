import requests
from threading import Thread
from blockchain import Blockchain
from urllib.parse import urlparse
from time import sleep
from serializers import blockchain_serializer

class Node:

	def __init__(self, neighbours=set(), blockchain = Blockchain()):
		self.neighbours = neighbours
		self.neighbours.add('http://206.189.174.49:81/')
		self.blockchain = blockchain
		if len(self.neighbours) < 8:
			self.ask_new_neighbours(8-len(self.neighbours))
		self.start_blockchain_worker()

	def start_blockchain_worker(self):
		Notifier(node=self, function=NotifierFunctions.blockchain_worker).start()

	def get_blockchain_neighbours(self):
		for neighbour in list(self.neighbours):
			Notifier(node=self, url=neighbour, function=NotifierFunctions.get_blockchain).start()

	def notify_neighbours(self,url, method=None, function=None, data={}): 
		for neighbour in list(self.neighbours):
			Notifier(node=self, url=neighbour + url, method=method, function=function, data=data).start()

	def ask_new_neighbours(self, quantity):
		Notifier(node=self, function=NotifierFunctions.get_neighbours).start()
		
	def notify_transaction(self, transaction): 
		self.notify_neighbours(function=NotifierFunctions.notify, method=requests.post, url="blockchain", data=transaction.__dict__)

	def notify_close_block(self, index):
		self.notify_neighbours(function=NotifierFunctions.notify, method=requests.put, url="blockchain/closeblock", data={"index" : index})

	def to_list(self):
		return self.blockchain.to_list

	def size(self):
		return self.blockchain.size()

	def is_valid(self):
		return self.blockchain.is_valid()

	def close_last_block(self, index):
		block = self.blockchain.close_last_block(index)
		if block:
			self.notify_close_block(index)
			return block

	def add_transaction(self, sender, receiver, amount, timestamp=None, thash=None):
		transaction, result = self.blockchain.add_transaction(sender, receiver, amount, timestamp, thash)

		if result:
			self.notify_transaction(transaction)
		return transaction

	def new_blockchain(self, blockchain):
		self.blockchain.new_blockchain(blockchain)

	def add_neighbour(self, neighbour):
		self.neighbours.add("http://%s:81/" % neighbour)

	def remove_neighbour(self, url=None, neighbour=None):
		neighbour_to_remove = ""
		if neighbour: neighbour_to_remove = neighbour
		elif url:
			neighbour_to_remove = "http://%s/" % urlparse(url).netloc
		self.neighbours.remove(neighbour_to_remove)

	def get_block(self, index):
		return self.blockchain.get_block(index)


class Notifier(Thread): 

	def __init__(self, node=None, url=None, method=None, data=None, function=None):
		self.node = node
		self.url = url
		self.method = method
		self.data = data
		self.function = function
		Thread.__init__(self)

	def run(self):
		if self.function:
			self.function(notifier=self, node=self.node, url=self.url, method=self.method, data=self.data)
		else: 
			self.method(self.url, json=self.data)
 
	def send(self, url, data={}): 
		self.method(url, json=data)

	def receive(self, url, data=None):
		return requests.get(url, data=data).json()

class NotifierFunctions:
 
	def get_neighbours(notifier, node, *args, **kwargs):
		new_neighbours = []
		for neighbour in list(node.neighbours):
			try:
				new_neighbours = new_neighbours + notifier.receive(neighbour+"neighbours")
			except:
				pass
		for neighbour in new_neighbours: 
			node.neighbours.add(neighbour)

	def get_blockchain(notifier, node, url, *args, **kwargs):
		data = None
		try:
			data = notifier.receive(url)
		except:
			node.remove_neighbour(url)
		if data:
			blockchain = blockchain_serializer(data)
			node.new_blockchain(blockchain)

	def blockchain_worker(node, *args, **kwargs):
		while True:
			node.get_blockchain_neighbours()
			sleep(600)

	def notify(notifier, url, node, data, *args, **kwargs):
		try:
			notifier.send(url, data)
		except:
			node.remove_neighbour(url)
