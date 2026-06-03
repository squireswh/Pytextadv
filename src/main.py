# (c) 2026
# ClicKill Microbits

from room import Room, RoomIdx

def main():
	start_room = Room("Start", "This is the beginning of your puny adventure", [1, 0, 2, 0, 0, 0, 0, 0, 0, 0])
	end_room = Room("End", "You've reached the end of your journey. :(", [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
	rooms = [None, start_room, end_room]

	# Index into rooms[] of the spawn point.
	starting_room = 1
	ending_room = 2

	# The room index of the room the character is currently in.
	curr_room = starting_room

	# Print the game intro text.
	print(f"{game_start_text()}")

	# Keep going until the user quits or reaches the last room.
	while True:
		curr_room = game_loop(curr_room, rooms)

		# If we get back 0, or the value of 'ending_room', we're done!
		if curr_room == 0 or curr_room == ending_room:
			if curr_room == 0:
				print("Game Over!")
			else:
				print("You've reached the end of your journey!")
			return

def game_start_text() -> str:
	return "Hello from pytextadv!\n"

def game_loop(current_room: int, rooms_list: list[Room]) -> int:
	# List of single-word commands the game engine understands.
	single_word_commands = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'UP', 'DOWN', 'QUIT']

	# Direction commands only.
	direction_commands = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'UP', 'DOWN']

	# Get the Room object we need.
	the_room = rooms_list[current_room]

	# Show the room name.
	print(f"You are in: {the_room.room_name}\n")

	# Show the room description.
	print(f"{the_room.room_description()}\n")

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

	# Debugging
	# print(f"{components=}\n\n")

	# 'lc': # elements in the list 'components'.
	lc = len(components)
	if lc == 1:
		# Single-word command.
		command = components[0]

		# In case the user hit <Enter> without typing anything, or they only typed a period.
		if command == '':
			print("I don't understand. :( \n")
			return current_room

		# Is 'command' a command the game engine understands?
		if command in single_word_commands:			
			# Handle 'Quit' separately.
			if command == "QUIT":
				print("Exiting the game.\n")
			else:
				# Is this a direction the player can go in?
				if command in direction_commands:
					print(f"Going {command}...\n")

					# Turn the command into the RoomIdx enum (for now, just use an int).
					room_idx = cmd_to_room_index(command)

					# Debugging
					# print(f"{room_idx=}")

					# Now, look at the value of the room's exit list @ that index.
					new_room = the_room.room_exit(room_idx)

					# Debugging
					# print(f"{new_room=}")
					if new_room == 0:
						print("You can't go that way.\n")
						return current_room
					else:
						return new_room
				else:
					print(f"I don't understand the command: {command}\n")
					return current_room
		else:
			print(f"I don't understand the command: {command}\n")
			return current_room
	else:
		# Multi-word commands.
		print(f"I don't understand {user_input}. :(\n")
		return current_room
	return 0

def cmd_to_room_index(the_cmd: str) -> int:
	direction_commands = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'UP', 'DOWN']
	return direction_commands.index(the_cmd)

if __name__ == "__main__":
	main()
