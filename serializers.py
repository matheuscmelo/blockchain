from blockchain import Blockchain, Block, Transaction
def blockchain_serializer(data):
	blockchain = Blockchain()
	blockchain.genesis = block_serializer(data[0])
	block = blockchain.genesis
	i = 1
	while block and i < len(data):
		next_block = block_serializer(data[i])
		block.next_block = next_block
		block = next_block
		i += 1
	blockchain.last_block = block
	return blockchain
		

def block_serializer(data):
	block =  Block(index=data['index'])
	for transaction in data['transactions']:
		block.add_transaction(sender=transaction['sender'], receiver=transaction['receiver'], amount=transaction['amount'], timestamp=transaction['timestamp'], thash=transaction['hash'])
	block.hash = data['hash']
	return block