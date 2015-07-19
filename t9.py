import curses
from curses import wrapper

# ------------------------------------------------------------------------------
# Auxiliary class to be used within the Trie
class Node:
	def __init__(self):
		self.value = []
		self.char = None
		self.left = None
		self.mid = None
		self.right = None
	
	def __str__(self):
		string = self.char + '[' + ' '.join(self.value) + '], ' 
		if self.left != None:
			string = string + self.left.char
		string = string + ', '
		if self.mid != None:
			string = string + self.mid.char
		string = string + ', '
		if self.right != None:
			string = string + self.right.char
		string = string + '\n'
		return string
		
	
# ------------------------------------------------------------------------------
# Class that controls the creation and basic Trie API
class Trie:
	def __init__(self):
		self.root = None

	def __str__(self):
		return self.print_node(self.root, '')

	def print_node(self, node, string):
		if node == None:
			return string
		string = string + str(node)
		if node.left != None:
			string = self.print_node(node.left, string)
		if node.mid != None:
			string = self.print_node(node.mid, string)
		if node.right != None:
			string = self.print_node(node.right, string)
		return string

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

	def get_subtrie(self, key, N):
		node = self.get_inner(self.root, key, 0)
		if node == None:
			return None
		else:
			# copy the contents to avoid modifying the value of the node
			children = list(node.value)
			if node.mid != None:
				children = self.get_children(node.mid, N, children) 
			return children

	def get_children(self, node, N, children):
		children.extend(node.value)
		if len(children) >= N:
			return children
		if node.left != None:
			children = self.get_children(node.left, N, children)
			if len(children) >= N:
				return children
		if node.mid != None:
			children = self.get_children(node.mid, N, children)
			if len(children) >= N:
				return children
		if node.right != None:
			children = self.get_children(node.right, N, children)
		return children

# ------------------------------------------------------------------------------
# Dictionary to map letters to numbers, in order to create the Trie using the
# combinations of numbers as key, and the words as values
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

# Trie where the dictionary is stored
words_trie = Trie()

# Use the default English dictionary included in all *nix distributions
with open('/usr/share/dict/words', 'r') as dictionary:
# with open('./words', 'r') as dictionary:
	for line in dictionary:
		word = line.strip()

		key_list = []
		for char in word.lower():
			key_list.append(map_letters_to_numbers[char])
		key = ''.join(key_list)

		words_trie.put(key, word)

# Just a couple of examples:
# hello -> 43556
# fore  -> 3673

# ------------------------------------------------------------------------------
# Using curses to control the display on the screen
stdscr = curses.initscr()

# Function to be used later with `wrapper` so that this helper function takes
# care of all the initialization, exceptions and clean up of the screen setup
def t9_interface(stdscr):
	curses.cbreak()
	stdscr.clear()

	input_text = ''
	matches = []
	while True:
		stdscr.addstr(0, 0, 'Type the numbers and the words should be appearing underneath...')
		stdscr.addstr(1, 0, 'It accepts only [0-9], or [q] to exit. Use DEL to delete a number')
		stdscr.addstr(2, 0, '>> ' + input_text)
		stdscr.addstr(3, 0, 'Matches:')
		if len(matches) > 0:
			stdscr.addstr(4, 0, ' '.join(matches[0:min(len(matches), 10)]))

		c = stdscr.getch()
		stdscr.clear()
		if c == ord('q'):
			if len(input_text) == 0:
				break
		if c >= ord('0') and c <= ord('9'):
			input_text = input_text + chr(c)
		else:
			if c == curses.KEY_DC and len(input_text) > 0:
				input_text = input_text[0:-1]
		if len(input_text) > 0:
			matches = words_trie.get_subtrie(input_text, 10)
			if matches == None:
				matches = [] 
		else:
			matches = []

# Actual call to the interface that will show the results to the user input
curses.wrapper(t9_interface)
