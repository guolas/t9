class Node:
	def __init__(self):
		self.value = []
		self.char = None
		self.left = None
		self.mid = None
		self.right = None
	
class Trie:
	def __init__(self):
		self.root = None

	def put(self, key, value):
		self.root = self.put_inner(self.root, key, value, 0)

	def put_inner(self, node, key, value, idx):
		char = key[idx]
		if node == None:
			node = Node()
			node.char = char
		if char < node.char:
			node.left = self.put_inner(node.left, key, value, idx)
		elif char > node.char:
			node.right = self.put_inner(node.right, key, value, idx)
		elif idx < len(key) - 1:
			node.mid = self.put_inner(node.mid, key, value, idx + 1)
		else:
			node.value.append(value)
		return node
	
	def contains(self, key):
		return self.get(key) != None

	def get(self, key):
		node = self.get_inner(self.root, key, 0)
		if node == None:
			return None
		else:
			return node.value

	def get_inner(self, node, key, idx):
		if node == None:
			return None
		char = key[idx]
		if char < node.char:
			return self.get_inner(node.left, key, idx)
		elif char > node.char:
			return self.get_inner(node.right, key, idx)
		elif idx < len(key) - 1:
			return self.get_inner(node.mid, key, idx + 1)
		else:
			return node

map_letters_to_numbers = {
  'a': '2',
  'b': '2',
  'c': '2',
  'd': '3',
  'e': '3',
  'f': '3',
  'g': '4',
  'h': '4',
  'i': '4',
  'j': '5',
  'k': '5',
  'l': '5',
  'm': '6',
  'n': '6',
  'o': '6',
  'p': '7',
  'q': '7',
  'r': '7',
  's': '7',
  't': '8',
  'u': '8',
  'v': '8',
  'w': '9',
  'x': '9',
  'y': '9',
  'z': '9',
  '-': '0'
}

dictionary_mapped = {}

words_trie = Trie()

with open('/usr/share/dict/words', 'r') as dictionary:
	for line in dictionary:
		word = line.strip()

		key_list = []
		for char in word.lower():
			key_list.append(map_letters_to_numbers[char])
		key = ''.join(key_list)
		
		words_trie.put(key, word)

print('The word is: {:}'.format(words_trie.get('43556')))
