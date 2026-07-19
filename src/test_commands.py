# test_commands.py

import unittest
from commands import Command
from helper import quote_it

class TestCommands(unittest.TestCase):
	def test_init(self):
		new_command = Command('test', 't', 0)
		self.assertEqual(new_command.required_args(), 0)

	def test_is_good_cmd(self):
		new_command = Command('test', 't', 0)
		self.assertEqual(new_command.is_good_command('test'), True)
		self.assertEqual(new_command.is_good_command('t'), True)
		self.assertEqual(new_command.is_good_command('text'), False)
		self.assertEqual(new_command.is_good_command('x'), False)

