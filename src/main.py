# (c) 2026
# ClicKill Microbits

import builtins

builtins.DEBUGGING = True

from room import Room, RoomIdx
from commands import Command
from item import Item, items
from inventory import global_inventory
from helper import aan
from words import WordType, Word, Words, global_words

def main():
	# Room setups.
	#
	# Each room has:
	# * Room name
	# * Room description
	# * Room index (the index into the rooms[] list where it resides - used for internsl bookkeeping.)
	# * Room exit list (The list of indices into the rooms[] list of exits; 0 -> no exit from here, or an
	#   integer index indicating the room the player will end up in if they go in a specific direction from
	#   the current room. The direction order is always: N,Ne,E,SE,S,SW,W,NW,Up,Down).)
	player = Room("Player", "the player", 0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

	# Our starting location.
	start_room = Room("Start", "This is the beginning of your puny adventure", 1, [1, 0, 2, 0, 0, 0, 0, 0, 0, 0])

	# Our ending location.
	end_room = Room("End", "You've reached the end of your journey.", 2, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
	rooms = [player, start_room, end_room]

	# Index of the spawn point in the rooms[] list.
	starting_room = 1
	ending_room = 2

	# The room index of the room the character is currently in.
	curr_room = starting_room

	# Item/inventory setups
	key_item = Item('Key', 'gold', 1)
	global_inventory.add_item(key_item)

	# Command setups.
	commands = setup_words()

	# Debugging
	# print(f"{global_words.dump_words()=}")

	# Print the game intro text.
	print(f"{game_start_text()}")

	# Keep going until the user quits or 'game_over' == True.
	game_over = False
	# game_over = True
	while game_over == False:
		curr_room, game_over = game_loop(curr_room, rooms, commands)

		# If we get back 0, or the value of 'ending_room', we're done!
		if curr_room == 0 or game_over:
			print("Game Over!")
			game_over = True

def game_start_text() -> str:
	return "Hello from pytextadv!\n"

def setup_words() -> list[Command]:
	quit_command = init_command('Quit', 'Q', 0)
	look_command = init_command('LOOK', 'L', 0)
	north_command = init_command('NORTH', 'N', 0)
	ne_command = init_command('NORTHEAST', 'NE', 0)
	east_command = init_command('EAST', 'E', 0)
	se_command = init_command('SOUTHEAST', 'SE', 0)
	south_command = init_command('SOUTH', 'S', 0)
	sw_command = init_command('SOUTHWEST', 'SW', 0)
	west_command = init_command('WEST', 'W', 0)
	nw_command = init_command('NORTHWEST', 'NW', 0)
	up_command = init_command('UP','U', 0)
	down_command = init_command('DOWN', 'D', 0)
	take_command = init_command('TAKE','', 1, False)
	inv_command = init_command('INVENTORY', 'I', 0)
	drop_command = init_command('DROP', '', 1, False)
	go_command = init_command('GO', '', 1)

	# add the commands to the list of comands.
	commands = [quit_command,
	look_command,
	north_command,
	ne_command,
	east_command,
	se_command,
	south_command,
	sw_command,
	west_command,
	nw_command,
	up_command,
	down_command,
	take_command,
	inv_command,
	drop_command,
	go_command
	]

	# add the prepositions to the list
	prep_word = Word("on", WordType.WORDTYPE_Preposition)
	global_words.add_word(prep_word)
	prep_word = Word("to", WordType.WORDTYPE_Preposition)
	global_words.add_word(prep_word)

	# add the articles ('a', 'an', 'the') to the list
	article_word = Word('a', WordType.WORDTYPE_Article)
	global_words.add_word(article_word)
	article_word = Word('an', WordType.WORDTYPE_Article)
	global_words.add_word(article_word)
	article_word = Word('the', WordType.WORDTYPE_Article)
	global_words.add_word(article_word)

	# Initialize the singleton Inventory object
	global_inventory.clear()
	return commands

def init_command(the_cmd: str, cmd_alias: str, num_args: int, built_in: bool = True) -> Command:
	cmd_str = Command(the_cmd.upper(), cmd_alias, num_args, built_in)

	# Add the command and its alias to the global word list.
	verb_word = Word(the_cmd.lower(), WordType.WORDTYPE_Verb)
	global_words.add_word(verb_word)
	verb_word = Word(cmd_alias.lower(), WordType.WORDTYPE_Verb)
	global_words.add_word(verb_word)

	# Return the constructed Command object.
	return cmd_str

def game_loop(current_room: int, rooms_list: list[Room], commands: list[Command]) -> (int, bool):
	# Get the Room object we need.
	the_room = rooms_list[current_room]

	# Show the room name.
	print(f"You are in: {the_room.room_name}\n")

	# Show the room description.
	print(f"{the_room.room_description()}")

	# Show the room inventory
	the_room.room_inv()

	# Input prompt
	user_input = input(">")

	# Get rid of any '.' at the end.
	the_suffix = user_input[-1:]
	if the_suffix == ".":
		user_input = user_input[:-1]

	# All uppercase.
	user_input_upper = user_input.upper()

	# Separate out the word(s) in the sentence.
	components = user_input_upper.split(" ")

	# 'lc': # elements in the list 'components'.
	lc = len(components)
	if lc == 0:
		command = ''
		args = []
	else:
		command = components[0].lower()
		args = components[1:]

	# In case the user hit <Enter> without typing anything, or they only typed a period.
	if command == '':
		print("Time passes.\n")
		return (current_room, False)

	# See if the command is 'go', or it's alias, 'g' (because we haven't resolved command aliases, yet.)
	if (command == 'go') or (command == 'g'):
		# Replace the verb 'go' with it's direct object.
		if lc > 1:
			command = components[1]
			components = [command]
			lc = 1
		else:
			# do nothing - the problem will be taken care of in procress_command().
			pass

	# Parse user input into Word instances (for now, this assumes only one word of any WordType.)
	# An adjective, if present, is assumed to modify the direct object (contained in 'sentence_dict["NOUN]'.)
	sentence_dict = dict()
	for the_word in components:
		# Debugging
		if DEBUGGING:
			print(f"{the_word=}")

		the_word_type = global_words.word_type(the_word)
		# Debugging
		if DEBUGGING:
			print(f"{the_word_type=}")
		if not (the_word_type is None):
			# Valid word
			match the_word_type:
				case WordType.WORDTYPE_Noun:
					if the_preposition == "":
						# No preposition yet, so no indirect object
						sentence_dict["NOUN"] = the_word
					else:
						# the_ido = the_word
						sentence_dict["INDIRECT_OBJECT"] = the_word
				case WordType.WORDTYPE_Adjective:
					sentence_dict["ADJECTIVE"] = the_word
				case WordType.WORDTYPE_Verb:
					sentence_dict["VERB"] = the_word
					command = the_word
				case WordType.WORDTYPE_Preposition:
					sentence_dict["PREPOSITION"] = the_word
				case WordType.WORDTYPE_Article:
					sentence_dict["ARTICLE"] = the_word
				case _:
					# internal error!!
					raise Exception("Internal error!")
		else:
			print(f"I don't understand '{the_word}'\n")
			return

	# Debugging
	# print(f"{sentence_dict=}")

	# Is 'command' a command the game engine understands?
	for idx, the_cmd in enumerate(commands):
		# Debugging
		if DEBUGGING:
			print(f"{idx=}, {the_cmd=}")
		if the_cmd.is_good_command(command):
			# Debugging
			if DEBUGGING:
				print("good command")

			# Yes, do something with the 'idx'th command.
			new_room = process_command(the_cmd.required_args(), current_room, command, idx, the_room, args, sentence_dict, commands)

			# check the game over condition
			g_over = (new_room == 2)
			if g_over:
				# Reprint the room name and description.
				# Fetch the new room so we can get an up-to-date name/description.
				the_room = rooms_list[new_room]
				print(f"You are in: {the_room.room_name()}\n")
				print(f"{the_room.room_description()}")				
			return (new_room, g_over)
		else:
			# Debugging
			if DEBUGGING:
				print("command not recognized.")
			g_over = True
			new_room = 0

def process_command(reqd_args: int, curr_room: int, cmd_str: str, idx: int, t_room: Room, args: list[str], sentence: dict, commands: list[Command]) -> int:
	# Make sure commands that take arguments get them.
	num_args = len(args)
	if num_args < reqd_args:
		print("I need more information.")
		return curr_room

	# Resolve command aliases.
	aliases = [x.cmd_alias() for x in commands]
	corr_commands = [x.cmd_command() for x in commands]
	if cmd_str in aliases:
		# 'cmd_str' is in the list of aliases for all commands; replace it with the real
		# command.
		idx2 = aliases.index(cmd_str)

		# Debugging
		if DEBUGGING:
			print(f"Alias '{cmd_str}' found: replacing with '{corr_commands[idx2]}' @ {idx2}")
		cmd_str = corr_commands[idx2]

	# get the index of the command in 'commands'.
	idx = corr_commands.index(cmd_str)

	# Debugging
	if DEBUGGING:
		print(f"{idx=}")

	# Now decide what to do.
	if num_args == 0:
		# Debugging
		if DEBUGGING:
			print("command has no argument.")

		# handle commandsthat don't take any extra information.
		match idx:
			case 0:
				# Quit command
				print("Exiting the game.\n")
				return 0

			case 1:
				# Look command.
				print(t_room.room_desc_always())

				# Show the room inventory
				t_room.room_inv()				
				return curr_room

			case 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11:
				# Direction commands.
				print(f"Going {cmd_str}...\n")
				room_idx = idx - 2

				# Now, look at the value of the room's exit list @ that index.
				new_room = t_room.room_exit(room_idx)
				if new_room == 0:
					print("You can't go that way.\n")
					return curr_room
				else:
					return new_room

			case 13:
				# Inventory command.
				inv_str = global_inventory.show_inv_for(0)
				print(inv_str)
				return curr_room

			case _:
				return curr_room
	else:
		# Debugging
		if DEBUGGING:
			print('Poodoo!')
		return curr_room

	def player_take(item: str, p_inv: list[str]) -> str:
		raise Exception("Not implemented yet.")

if __name__ == "__main__":
	main()
