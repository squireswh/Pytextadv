# test_room.py

import unittest
from helper import quote_it
from room import Room, RoomIdx

class TestRoom(unittest.TestCase):
	def test_init(self):
		new_room = Room('Test', 'Test room', 0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
		self.assertEqual(new_room.room_description(), 'Test room')
		self.assertEqual(new_room.room_description(), '\n')
		self.assertEqual(new_room.room_desc_always(), 'Test room')
		self.assertEqual(new_room.room_index(), 0)
		for i in range(0, 10):
			self.assertEqual(new_room.room_exit(i), 0)

	def test_can_go_in_dir(self):
		new_room = Room('Test', 'Test room', 0, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
		self.assertEqual(new_room.can_go_in_direction(RoomIdx.ROOMIDX_North), False)
		self.assertEqual(new_room.can_go_in_direction(RoomIdx.ROOMIDX_Northeast), True)
		self.assertEqual(new_room.can_go_in_direction(RoomIdx.ROOMIDX_East), True)
		self.assertEqual(new_room.can_go_in_direction(RoomIdx.ROOMIDX_Southeast), True)
		self.assertEqual(new_room.can_go_in_direction(RoomIdx.ROOMIDX_South), True)
		self.assertEqual(new_room.can_go_in_direction(RoomIdx.ROOMIDX_Southwest), True)
		self.assertEqual(new_room.can_go_in_direction(RoomIdx.ROOMIDX_West), True)
		self.assertEqual(new_room.can_go_in_direction(RoomIdx.ROOMIDX_Northwest), True)
		self.assertEqual(new_room.can_go_in_direction(RoomIdx.ROOMIDX_Up), True)
		self.assertEqual(new_room.can_go_in_direction(RoomIdx.ROOMIDX_Down), True)

