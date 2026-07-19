# (c) 2026
# ClicKill Microbits

from room import Room, RoomIdx
from commands import Command
from item import Item, items
from inventory import global_inventory
from helper import aan

def main():
	# Room setups.
	player = Room("Player", "the player", 0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

	# Our starting location.
	start_room = Room("Start", "This is the beginning of your puny adventure", 1, [1, 0, 2, 0, 0, 0, 0, 0, 0, 0])

	# Our ending location.
	end_room = Room("End", "You've reached the end of your journey.", 2, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
	rooms = [player, start_room, end_room]

	# Index into rooms[] of the spawn point.
	starting_room = 1
	ending_room = 2

	# The room index of the room the character is currently in.
	curr_room = starting_room

	# Item/inventory setups
	key_item = Item('Key', 'gold', 1)
	global_inventory.add_item(key_item)

	# Print the game intro text.
	print(f"{game_start_text()}")

	# Keep going until the user quits or 'game_over' == True.
	game_over = False
	while game_over == False:
		curr_room, game_over = game_loop(curr_room, rooms)

		# If we get back 0, or the value of 'ending_room', we're done!
		if curr_room == 0 or game_over:
			print("Game Over!")
			game_over = True

def game_start_text() -> str:
	return "Hello from pytextadv!\n"

def game_loop(current_room: int, rooms_list: list[Room]) -> (int, bool):
	# Command setups.
	quit_command = Command('QUIT', 'Q', 0)
	look_command = Command('LOOK', 'L', 0)
	north_command = Command('NORTH', 'N', 0)
	ne_command = Command('NORTHEAST', 'NE', 0)
	east_command = Command('EAST', 'E', 0)
	se_command = Command('SOUTHEAST', 'SE', 0)
	south_command = Command('SOUTH', 'S', 0)
	sw_command = Command('SOUTHWEST', 'SW', 0)
	west_command = Command('WEST', 'W', 0)
	nw_command = Command('NORTHWEST', 'NW', 0)
	up_command = Command('UP','U', 0)
	down_command = Command('DOWN', 'D', 0)
	take_command = Command('TAKE','', 1)
	inv_command = Command('INVENTORY', 'I', 0)
	drop_command = Command('DROP', '', 1)

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
	drop_command
	]

	# Initialize the singleton Inventory object
	global_inventory.clear()
	
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
	command = components[0]

	# Single-word command.
	if lc == 1:
		args = []
	else:
		args = components[1:]

	# In case the user hit <Enter> without typing anything, or they only typed a period.
	if command == '':
		print("I don't understand. \n")
		return (current_room, False)

	# Is 'command' a command the game engine understands?
	for idx, the_cmd in enumerate(commands):
		if the_cmd.is_good_command(command):
			# Yes, do something with the 'idx'th command.
			new_room = process_command(the_cmd.required_args(), current_room, command, idx, the_room, args)

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
		print(f"I don't understand '{command}'. \n")
		return (current_room, False)
	
def process_command(reqd_args: int, curr_room: int, cmd_str: str, idx: int, t_room: Room, args: list[str]) -> int:
	# Make sure commands that take arguments get them.
	num_args = len(args)
	if num_args < reqd_args:
		print("I need more information.")
		return curr_room

	# Now decide what to do.
	match idx:
		case 0:
			# Quit command
			print("Exiting the game.\n")
			return 0

		case 1:
			# Look command
			if num_args == 0:
				t_room.room_desc_always()

				# Show the room inventory
				t_room.room_inv()
			else:
				# Look <arg> (for now) just confirms the player has
				# - or does not have - the item indicated by <arg>.
				if num_args >= 2:
					item_adj = f"{args[0].upper()} "
					item_name = args[1].upper()
				else:
					item_name = args[0].upper()
					item_adj = ""
				item = item_adj + item_name
				if player_has_item(item):
					print(f"You have the {item}.")
				else:
					article = aan(item)
					print(f"You don't have {article}{item}.")
			return curr_room

		case 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11:
			# Direction commands.
			print(f"Going {cmd_str}...\n")
			room_idx = idx - 2

			# Debugging
			# print(f"{room_idx=}")

			# Now, look at the value of the room's exit list @ that index.
			new_room = t_room.room_exit(room_idx)

			# Debugging
			# print(f"{new_room=}")
			if new_room == 0:
				print("You can't go that way.\n")
				return curr_room
			else:
				return new_room

		case 12:
			# Take command.
			if num_args >= 2:
				item_adj = f"{args[0].upper()} "
				item_name = args[1].upper()
			else:
				item_name = args[0].upper()
				item_adj = ""
			item = item_adj + item_name
			if not player_has_item(item):
				# Move the item out of the current room
				# into the player's inventory (room 0).
				if global_inventory.move_item_room_to_room(item, curr_room, 0):
					print(f"You take the {item}.")
				else:
					print("I don't see it here.")
			else:
				print("You already have it.")
			return curr_room

		case 13:
			# Inventory command.
			inv_str = global_inventory.show_inv_for(0)
			print(inv_str)
			return curr_room

		case 14:
			# Drop command
			if num_args >= 2:
				item_adj = f"{args[0].upper()} "
				item_name = args[1].upper()
			else:
				item_name = args[0].upper()
				item_adj = ""
			item = item_adj + item_name
			if global_inventory.player_has_item(item):
				# poop
				if global_inventory.move_item_room_to_room(item, 0, curr_room):
					print(f"You drop the {item}.")
				else:
					raise Exception(f"Internal error: we shouldn't get here, the player should have had the item {item}.")
			else:
				print("You don't have it.")
			return curr_room

		case _:
			return curr_room

	def player_take(item: str, p_inv: list[str]) -> str:
		raise Exception("Not implemented yet.")

if __name__ == "__main__":
	main()
