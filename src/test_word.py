# test_word.py

import unittest
from words import WordType, Word, Words
from helper import quote_it

class TestCommands(unittest.TestCase):
	def test_wordtype(self):
		word_type = WordType.WORDTYPE_Noun
		self.assertEqual(repr(word_type), "(noun)")
		word_type = WordType.WORDTYPE_Adjective
		self.assertEqual(repr(word_type), "(adjective)")
		word_type = WordType.WORDTYPE_Verb
		self.assertEqual(repr(word_type), "(verb)")
		word_type = WordType.WORDTYPE_Preposition
		self.assertEqual(repr(word_type), "(preposition)")
		word_type = WordType.WORDTYPE_Article
		self.assertEqual(repr(word_type), "(article)")

	def test_word(self):
		word = Word("apple", WordType.WORDTYPE_Noun)
		self.assertEqual(word.theWord, "apple")
		self.assertEqual(word.wordType, WordType.WORDTYPE_Noun)
		word = Word("shiny", WordType.WORDTYPE_Adjective)
		self.assertEqual(word.theWord, "shiny")
		self.assertEqual(word.wordType, WordType.WORDTYPE_Adjective)
		word = Word("go", WordType.WORDTYPE_Verb)
		self.assertEqual(word.theWord, "go")
		self.assertEqual(word.wordType, WordType.WORDTYPE_Verb)
		word = Word("on", WordType.WORDTYPE_Preposition)
		self.assertEqual(word.theWord, "on")
		self.assertEqual(word.wordType, WordType.WORDTYPE_Preposition)
		word = Word("an", WordType.WORDTYPE_Article)
		self.assertEqual(word.theWord, "an")
		self.assertEqual(word.wordType, WordType.WORDTYPE_Article)
		self.assertEqual(word.the_word(), 'an')
		self.assertEqual(word.the_word_type(), WordType.WORDTYPE_Article)

	def test_words_init(self):
		words = Words()
		self.assertEqual(words.wordList, [])

	def test_words_clear(self):
		words = Words()
		a_word = Word("apple", WordType.WORDTYPE_Noun)
		words.add_word(a_word)
		self.assertNotEqual(words, [])
		words.clear()
		self.assertEqual(words.wordList, [])

	def test_add_word(self):
		words = Words()
		words.clear()
		self.assertEqual(words.wordList, [])
		a_word = Word("apple", WordType.WORDTYPE_Noun)
		words.add_word(a_word)
		self.assertNotEqual(words, [])
		self.assertEqual(len(words.wordList), 1)
		a_word = Word("shiny", WordType.WORDTYPE_Adjective)
		words.add_word(a_word)
		self.assertNotEqual(words, [])
		self.assertEqual(len(words.wordList), 2)
		words.clear()

	def test_dump_words(self):
		words = Words()
		words.clear()
		the_words = words.dump_words()
		self.assertEqual(the_words, [])
		a_word = Word("apple", WordType.WORDTYPE_Noun)
		words.add_word(a_word)
		a_word = Word("shiny", WordType.WORDTYPE_Adjective)
		words.add_word(a_word)
		the_words = words.dump_words()
		self.assertEqual(the_words, ['word=apple: WordType.WORDTYPE_Noun', 'word=shiny: WordType.WORDTYPE_Adjective'])
		words.clear()
		the_words = words.dump_words()
		self.assertEqual(the_words, [])
