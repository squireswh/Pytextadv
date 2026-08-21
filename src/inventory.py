# inventory.py
#
# (c) 2026
# ClicKill Microbits
#
# This module implements the inventory for the player, and for the rooms
# in the game (monsters don't have inventory.)
#
# The inventory consists of two data structures; a list[Item] and a dictionary of [str, int].
# the list holds the list of all game items regardless of which 'room' they belong to, and
# the dictionary provides a lookup from the item-descriptive string to an integer index
# into the list.
#
# Room #0 is the 'player', an no exits exist from it, and no entrances should exist to it
# from other rooms.
#
# All the other rooms are actual rooms that can - but might not - have any items in them.

from item import Item
from helper import split_noun_adj
from words import WordType, Word, global_words

class Inventory:
	def __init__(self):
		# This list contains the actual Item instances.
		self.inventory = []

		# This dictionary maps the item descriptions to the indices into 'global_inventory'.
		self.inv_dict: dict[str, int] = {}

	def clear(self):
		self.inventory = []
		self.inv_dict: dict[str, int] = {}

	# This function adds an Item to the global inventory; DON'T use it to add a specific item
	# to the player's inventory - that's NOT what this function is for!!
	#
	# The Item should be preloaded with it's .item_location set to the index of the room it starts in.
	# If you want the player to start out with an item, set it's .item_location to 0.
	# Do this BEFORE calling this function!
	def add_item(self, the_item: Item) -> None:
		# This function presumes the caller has already set the item's location!
		#
		# This is the key into the dictionary. The item's description may or may not have an adjective.
		# If it does, then the description will have the form, "<adjective> <noun>", else it will
		# just be the noun (the item's name.) Python dictionaries are cas sensitive, so our comparisons
		# (later) must be case insensitive.
		u_desc = the_item.inv_desc().upper()

		# This is the index where 'the_item' will reside. This works because we always append to the end
		# of the list, ant Python lists start with index 0.
		new_idx = len(self.inventory)

		# Insert the item.
		self.inventory.append(the_item)

		# Make a Word for this item.
		noun_word = Word(the_item.name, WordType.WORDTYPE_Noun)
		global_words.add_word(noun_word)
		if len(the_item.adjective) > 0:
			adj_word = Word(the_item.adjective, WordType.WORDTYPE_Adjective)
			global_words.add_word(adj_word)

		# Make sure the item is not already in the dictionary
		if u_desc not in self.inv_dict:
			# No dups, okay to insert.
			self.inv_dict[u_desc] = new_idx
		else:
			# huge booboo!
			raise Exception(f"Item {u_desc} already in dictionary!")

	# This function returns a 2-tuple consisting of: the # of ambiguous entries if you leave off the adjective,
	# and the unambiguous description for that item.
	#
	# If it returns (0, _), then there are no items in the lookup dictionary whose name matches the noun part
	# of 'str'.
	# If it returns (1, _), then tuple[1] has the full item description.
	# If it returns a value > 1, then there's more than one item with the same name, but different adjectives.
	# This indicates the caller needs to handle this case by telling the player to disambiguate their input.
	def ambiguate(self, item: str) -> (int, str):
		# The # of ambiguous entries if you leave off the adjective.
		num_amb = 0

		# The dictionary key which will be returned as the 2nd item in the tuple.
		t_key = ""

		# Make case-insensitive.
		u_desc = item.upper()

		# Loop over all the key-value pairs in the dictionary.
		for index, (k, v) in enumerate(self.inv_dict.items()):
			# For each one, make sure it's uppercased, then disassemble it into the adjective and noun.
			# print(f"{k=}, {v=}")
			k_upper = k.upper()
			adj, noun = split_noun_adj(k_upper)

			# Could this be the one we're looking for?
			if noun == u_desc:
				num_amb += 1
				t_key = k_upper
		return (num_amb, t_key)

	# This function is used to move an item between rooms. This generally isused to take an item (move it
	# from room N to room 0), or drop an item (move it from room 0 to whatever room the player is currently
	# in.)
	def move_item_room_to_room(self, item: str, old_room: int, new_room: int) -> bool:
		# This is the key into the dictionary.
		u_desc = item.upper()

		# See if the player is actually referring to an item in the game.
		if u_desc in global_inv_dict:
			# Yep.
			idx = self.inv_dict[u_desc]
		else:
			# We didn't find 'item' in the global inventory;
			# try disambiguating it.
			n_amb, t_key = ambiguate(u_desc)
			if n_amb != 1:
				# Either not found, or needs disambiguation.
				if n_amb > 1:
					print(f"Which {u_desc}?")
				return False
			else:
				# There's only one item with the name; no dups. Look up the index from the dictionary.
				u_desc = t_key
				idx = self.inv_dict[u_desc]

		# Get the actual Item.
		the_item = self.inventory[idx]

		# Make sure it's actually @ 'old_room'.
		if the_item.item_location == old_room:
			# It is. All we need to do is set it's .item_location to that of the new room, 'new_room'.
			the_item.item_location  = new_room
			return True
		else:
			# Something went wrong.
			return False

	# This function returns True if the item 'item' is in room 0 (the player's inventory.)
	def player_has_item(self, item: str) -> bool:
		# Just in case...
		# This is the key into the dictionary.
		if room_no > 0:
			return room_has_item(item)
		u_desc = item.upper()
		if u_desc in self.inv_dict:
			idx = self.inv_dict[u_desc]
		else:
			# we didn't find 'item' in the player's inventory;
			# try disambiguating it.
			n_amb, t_key = ambiguate(u_desc)
			if n_amb != 1:
				if n_amb > 1:
					print(f"Which {u_desc}?")
				return False
			else:
				u_desc = t_key
				idx = self.inv_dict[u_desc]

		# Get the actual Item.
		the_item = self.inventory[idx]

		# Is it where we expect?
		if the_item.item_location == 0:
			return True
		return False	

	# This function returns True if the item 'item' is in room 'room_no'
	def room_has_item(self, room_no: int, item: str) -> bool:
		# Just in case...
		if room_no == 0:
			return player_has_item(item)
		# This is the key into the dictionary.
		u_desc = item.upper()
		if u_desc in self.inv_dict:
			idx = self.inv_dict[u_desc]
		else:
			# we didn't find 'item' in the inventory;
			# try disambiguating it.
			n_amb, t_key = ambiguate(u_desc)
			if n_amb != 1:
				if n_amb > 1:
					print(f"Which {u_desc}?")
				return False
			else:
				u_desc = t_key
				idx = self.inv_dict[u_desc]

		# Get the actual Item.
		the_item = self.inventory[idx]

		# Is it where we expect?
		if the_item.item_location == room_no:
			return True
		return False	

	# This function prints the inventory (if any) of room 'room_no' to stdout.
	def show_inv_for(self, room_no: int) -> str:
		# Holds the list of items. we need this so we can defer the printing
		# until after we've verified there are items in the inventory.
		item_list = []

		# This count will reveal if we have any items in room 'room_no'.
		printed = 0

		# Customize this based on the room #.
		greeting = "You see:"
		if room_no == 0:
			# Room 0 is the player's inventory.
			greeting = "You have:"

		# Add the items to 'item_list' (if any).
		for item in self.inventory:
			if item.item_location == room_no:
				# This item belongs to room #'room_no'; put the item in the list
				# and count it.
				item_list.append(f"* {item.item_desc()}")
				printed += 1

		# Do we have any items to print?
		if printed == 0:
			# No items in the inventory.
			if room_no == 0:
				# Do this, but only if we're printing the player's inventory.
				item_list.append("You have no items")
			return "\n".join(item_list)

		# Print the greeting, followed by the list of items.
		item_list.insert(0, greeting)
		return "\n".join(item_list)

global_inventory = Inventory()
