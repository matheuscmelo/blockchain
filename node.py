import requests
from threading import Thread
import json
from blockchain import Blockchain
from urllib.parse import urlparse
from time import sleep

class Node:

	def __init__(self, neighbours=set(), blockchain = Blockchain()):
		self.neighbours = neighbours
		self.neighbours.add('http://206.189.174.49:81/')
		self.neighbours.add('http://206.189.174.459:81/')
		self.blockchain = blockchain
		if len(self.neighbours) < 8:
			self.ask_new_neighbours(8-len(self.neighbours))

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

	def close_last_block(self, index=None):
		index = self.blockchain.close_last_block(index)
		if index != -1:
			self.notify_close_block(index)

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
		print (neighbour_to_remove) 
		self.neighbours.remove(neighbour_to_remove)



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

	def notify(notifier, url, node, data, *args, **kwargs):
		try:
			notifier.send(url, data)
		except:
			node.remove_neighbour(url)
