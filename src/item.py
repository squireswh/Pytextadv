# item.py
#
# (c) 2026
# ClicKill Microbits
#
# This module implements the game items (those the player can see or interact with.)

import copy
from helper import aan, quote_it

class Item:
	# Duh.
	def __init__(self, new_name: str, new_adj: str, loc: int):
		self.name = new_name.lower()
		self.adjective = new_adj.lower()
		self.item_location = loc

	# Debugging
	def __repr__(self) -> str:
		first_word = self.adjective
		desc = f"{self.adjective} {self.name}"
		if len(first_word) == 0:
			first_word = self.name
			desc = f"{self.name}"
		article = aan(first_word)
		desc2 = f"{article}{desc}"
		return f"{quote_it(desc)} @ {self.item_location}"

	# Special
	def __eq__(self, other) -> bool:
		# print("testing for equality with '=='")
		if not isinstance(other, Item):
			return NotImplemented
		name_eq = self.name == other.item_name()
		adj_eq = self.adjective == other.item_adjective()
		location_eq = self.item_location == other.item_location
		return name_eq and adj_eq and location_eq

	def copy(self):
		return copy.copy(self)

	def __copy__(self):
		# Create a new instance without calling __init__
		new_instance = self.__class__.__new__(self.__class__)
		
		# Perform a shallow copy of the attributes
		new_instance.__dict__.update(self.__dict__)
		return new_instance

	def __deepcopy__(self, memo):
		new_instance = self.__class__.__new__(self.__class__)
		memo[id(new_instance)] = new_instance
		
		# Perform a deep copy of each attribute
		for key, value in self.__dict__.items():
			setattr(new_instance, key, copy.deepcopy(value, memo))
			
		return new_instance

	# Getter.
	def item_name(self) -> str:
		return self.name

	# Getter.
	def item_adjective(self) -> str:
		return self.adjective

	# Getter.
	def item_desc(self) -> str:
		first_word = self.adjective
		desc = f"{self.adjective} {self.name}"
		if len(first_word) == 0:
			first_word = self.name
			desc = f"{self.name}"
		article = aan(first_word)
		return f"{article}{desc}"

	# Getter.
	def inv_desc(self) -> str:
		first_word = self.adjective
		desc = f"{self.adjective} {self.name}"
		if len(first_word) == 0:
			desc = f"{self.name}"
		return f"{desc}"

items = []
