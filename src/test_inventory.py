# test_inventory.py

import unittest
import copy
from item import Item
from helper import quote_it
from inventory import Inventory, global_inventory

class TestInventory(unittest.TestCase):
	def test_add_item(self):
		global_inventory.clear()
		test_item = Item("sword", "test", 0)
		self.assertEqual(len(global_inventory.inventory), 0)
		global_inventory.add_item(test_item)
		# print(f"{global_inventory=}")
		self.assertTrue(global_inventory.inventory)
		self.assertTrue(global_inventory.inv_dict)
		copy_test_item = global_inventory.inventory[0].copy()
		# print(f"{test_item=}, {copy_test_item=}")
		self.assertTrue(test_item == copy_test_item)
		for item, (k, v) in enumerate(global_inventory.inv_dict.items()):
			self.assertEqual(k.upper(), "TEST SWORD")
			self.assertEqual(v, 0)
			break

	def test_clear(self):
		global_inventory.clear()
		self.assertEqual(len(global_inventory.inventory), 0)
		self.assertFalse(global_inventory.inv_dict)

	def test_ambiguate_no_match(self):
		global_inventory.clear()
		test_item = Item("sword", "test", 0)
		global_inventory.add_item(test_item)
		result = global_inventory.ambiguate("maul")
		self.assertEqual(result[0], 0)

	def test_ambiguate_one_matching_item(self):
		global_inventory.clear()
		test_item = Item("sword", "test", 0)
		global_inventory.add_item(test_item)
		result = global_inventory.ambiguate("sword")
		self.assertEqual(result[0], 1)
		self.assertEqual(result[1], "TEST SWORD")

	def test_ambiguate_multiple_matching_items(self):
		global_inventory.clear()
		test_item1 = Item("sword", "test", 0)
		global_inventory.add_item(test_item1)
		test_item2 = Item("sword", "fire", 0)
		global_inventory.add_item(test_item2)
		result = global_inventory.ambiguate("sword")
		self.assertGreater(result[0], 1)
