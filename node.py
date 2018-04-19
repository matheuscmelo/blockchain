import requests
class Notifier:

	def __init__(self, neighbours=set()):
		self.neighbours = neighbours
		self.neighbours.add('http://localhost/')

	def send(self, method, url, data=None):
		try:
			method(url, data=data).json()
			return True
		except:
			return False

	def receive(self, url, data=None):
		return requests.get(url, data=data).json()

	def notify_neighbours(self, method, url, data=None):
		failed_neighbours = []
		for neighbour in self.neighbours:
			if not self.send(method, neighbour+url, data):
				failed_neighbours.add(neighbour)
		return failed_neighbours

	def notify(self, method, url, data=None):
		failed_neighbours = self.notify_neighbours(method, url, data)
		for failed in failed_neighbours:
			self.neighbours.remove(failed)
		self.ask_new_neighbours(len(failed_neighbours))

	def ask_new_neighbours(self, quantity):
		for neighbour in self.neighbours:
			new_neighbours = self.receive(neighbour+"neighbours", data={'quantity': quantity})
			for new_neighbour in new_neighbours:
				self.neighbours.add(new_neighbour)

	def notify_transaction(self, transaction):
		self.notify(requests.post, "blockchain")