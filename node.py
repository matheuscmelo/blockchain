import requests
from threading import Thread
import json
class Node:

	def __init__(self, neighbours=set()):
		self.neighbours = neighbours
		self.neighbours.add('http://127.0.0.1/')
 
	def receive(self, url, data=None):
		return requests.get(url, data=data).json()

	def notify_neighbours(self, method, url, data=None): 
		for neighbour in self.neighbours:
			Notifier(node=self,url=neighbour + url, method=method, data=data).start()

	def ask_new_neighbours(self, quantity):
		for neighbour in self.neighbours:
			new_neighbours = self.receive(neighbour+"neighbours", data={'quantity': quantity})
			for new_neighbour in new_neighbours:
				self.neighbours.add(new_neighbour)

	def notify_transaction(self, transaction): 
		self.notify_neighbours(method=requests.post, url="blockchain", data=transaction.__dict__)

class Notifier(Thread):

	def __init__(self, node, url, method, data):
		self.node = node
		self.url = url
		self.method = method
		self.data = data
		Thread.__init__(self)

	def run(self): 
		self.send(self.method, self.url, self.data)
 
	def send(self, method, url, data={}): 
		method(url, data=data)