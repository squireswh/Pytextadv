# test_item.py

import unittest
from helper import quote_it
from item import Item

class TestItem(unittest.TestCase):
	def test_init(self):
		new_item = Item('sword', 'heavy', 1)
		self.assertEqual(new_item.item_location, 1)
		self.assertEqual(new_item.item_name(), 'sword')
		self.assertEqual(new_item.item_adjective(), 'heavy')

	def test_item_desc(self):
		new_item = Item('sword', 'heavy', 1)
		self.assertEqual(new_item.item_desc(), 'a heavy sword')
		new_item = Item('sword', '', 1)
		self.assertEqual(new_item.item_desc(), 'a sword')
		new_item = Item('document', 'historic', 1)
		self.assertEqual(new_item.item_desc(), 'an historic document')
		new_item = Item('document', '', 1)
		self.assertEqual(new_item.item_desc(), 'a document')
		new_item = Item('igloo', 'interesting', 1)
		self.assertEqual(new_item.item_desc(), 'an interesting igloo')
		new_item = Item('igloo', '', 1)
		self.assertEqual(new_item.item_desc(), 'an igloo')

	def test_inv_desc(self):
		new_item = Item('sword', 'heavy', 1)
		self.assertEqual(new_item.inv_desc(), 'heavy sword')
		new_item = Item('sword', '', 1)
		self.assertEqual(new_item.inv_desc(), 'sword')
		new_item = Item('document', 'historic', 1)
		self.assertEqual(new_item.inv_desc(), 'historic document')
		new_item = Item('document', '', 1)
		self.assertEqual(new_item.inv_desc(), 'document')
		new_item = Item('igloo', 'interesting', 1)
		self.assertEqual(new_item.inv_desc(), 'interesting igloo')
		new_item = Item('igloo', '', 1)
		self.assertEqual(new_item.inv_desc(), 'igloo')

	def test_repr(self):
		new_item = Item('sword', 'heavy', 1)
		self.assertEqual(repr(new_item), f'{quote_it('heavy sword')} @ {new_item.item_location}')
		new_item = Item('sword', '', 1)
		self.assertEqual(repr(new_item), f'{quote_it('sword')} @ {new_item.item_location}')
		new_item = Item('document', 'historic', 1)
		self.assertEqual(repr(new_item), f'{quote_it('historic document')} @ {new_item.item_location}')
		new_item = Item('document', '', 1)
		self.assertEqual(repr(new_item), f'{quote_it('document')} @ {new_item.item_location}')
		new_item = Item('igloo', 'interesting', 1)
		self.assertEqual(repr(new_item), f'{quote_it('interesting igloo')} @ {new_item.item_location}')
		new_item = Item('igloo', '', 1)
		self.assertEqual(repr(new_item), f'{quote_it('igloo')} @ {new_item.item_location}')
