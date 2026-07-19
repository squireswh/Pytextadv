# room.py
#
# (c) 2026
# ClicKill Microbits
#
# This module implements the rooms in the game.
#
# The room is a class that holds the room's name, the descriptive
# text, a boolean flag to indicate f this room has been visited,
# and a list[int] of exits from the room. The indices into this list
# are the RoomIdx enumerated values.
#
# Room #0 is the 'player', an no exits exist from it, and no entrances should exist to it
# from other rooms.
#
# All the other rooms are actual rooms that can - but might not - have any items in them.

from enum import Enum
from inventory import global_inventory

class RoomIdx(Enum):
	ROOMIDX_North = 0
	ROOMIDX_Northeast = 1
	ROOMIDX_East = 2
	ROOMIDX_Southeast = 3
	ROOMIDX_South = 4
	ROOMIDX_Southwest = 5
	ROOMIDX_West = 6
	ROOMIDX_Northwest = 7
	ROOMIDX_Up = 8
	ROOMIDX_Down = 9

	def __repr__(self) -> str:
		if self == RoomIdx.ROOMIDX_North:
			return "RoomIdx.ROOMIDX_North"
		elif self == RoomIdx.ROOMIDX_Northeast:
			return "RoomIdx.ROOMIDX_Northeast"
		elif self == RoomIdx.ROOMIDX_East:
			return "RoomIdx.ROOMIDX_East"
		elif self == RoomIdx.ROOMIDX_Southeast:
			return "RoomIdx.ROOMIDX_Southeast"
		elif self == RoomIdx.ROOMIDX_South:
			return "RoomIdx.ROOMIDX_South"
		elif self == RoomIdx.ROOMIDX_Southwest:
			return "RoomIdx.ROOMIDX_Southwest"
		elif self == RoomIdx.ROOMIDX_West:
			return "RoomIdx.ROOMIDX_West"
		elif self == RoomIdx.ROOMIDX_Northwest:
			return "RoomIdx.ROOMIDX_Northwest"
		elif self == RoomIdx.ROOMIDX_Up:
			return "RoomIdx.ROOMIDX_Up"
		else:
			return "RoomIdx.ROOMIDX_Down"

class Room:
	# Duh.
	def __init__(self, room_name: str, room_desc: str, room_idx: int, room_exits: list[int]):
		# Room's name (ex: 'damp cave')
		self.room_name = room_name

		# Room's description (ex: 'This is a damp cave, treacherous and slick with condensation.')
		self.__room_desc = room_desc

		# Set to True once this roo visited for the 1st time.
		self.__visited = False

		# The index of this room in the list of rooms in main().
		self.__index = room_idx

		# Room's exits. This is a a list[int] where the position in this list is:
		# 0 - north
		# 1 - northeast
		# 2 - east
		# 3 - southeast
		# 4 - south
		# 5 - southwest
		# 6 - west
		# 7 - northwest
		# 8 - up
		# 9 - down
		# and each element's value is an index into a global list[Room] that the exit links to.
		self.__room_exits = room_exits

	# Debugging
	def __repr__(self) -> str:
		return f"{self.room_name=}, {self.room_desc=}, {self.room_exits=}"

	# Getter.
	#   Supply an integer index (see above) to get the index into the list of rooms (held in main.py)
	#   that the exit from this room takes the player to.
	def room_exit(self, idx: int) -> int:
		return self.__room_exits[idx]

	# Getter.
	#   Returns the description for this room if it hasn't been visited yet, or an empty string.
	def room_description(self) -> str:
		if self.__visited == False:
			self.__visited = True
			return f"{self.__room_desc}"
		return '\n'

	# Getter.
	#  Similar to the above, but always returns the description for the room.
	def room_desc_always(self) -> str:
		return f"{self.__room_desc}"

	# Getter.
	#   Return's the room's own index into the global list of rooms in main.py
	def room_index(self) -> int:
		return self.__index

	# Print the room's inventory (if any) to stdout.
	def room_inv(self) -> None:
		global_inventory.show_inv_for(self.__index)

	# Function that returns True if the player can exit the room in the direction
	# indicated by 'dir'.
	def can_go_in_direction(self, dir: RoomIdx) -> bool:
		idx = dir.value
		return (self.__room_exits[idx] != 0)
