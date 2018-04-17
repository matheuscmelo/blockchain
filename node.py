import requests

class Notifier:

	def __init__(self, neighbours=[]):
		self.neighbours = neighbours

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
			if not self.send(method, neighbour, data):
				failed_neighbours.append(neighbour)
		return results
