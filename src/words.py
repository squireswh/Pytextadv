# words.py
#
# (c) 2026
# ClicKill Microbits
#
# This module keeps track of all the words in the game, and their type: (noun, verb, adjective, preposition, article)

from enum import Enum

class WordType(Enum):
	WORDTYPE_Noun = 0
	WORDTYPE_Adjective = 1
	WORDTYPE_Verb = 2
	WORDTYPE_Preposition = 3
	WORDTYPE_Article = 4

	def __repr__(self) -> str:
		if self == WordType.WORDTYPE_Noun:
			return "(noun)"
		elif self == WordType.WORDTYPE_Adjective:
			return "(adjective)"
		elif self == WordType.WORDTYPE_Verb:
			return "(verb)"
		elif self == WordType.WORDTYPE_Article:
			return "(article)"
		else:
			return "(preposition)"

class Word:
	def __init__(self, theWord:str, wordType: WordType):
		self.theWord = theWord
		self.wordType = wordType

	def __repr__(self) -> str:
		return f"{self.theWord}: {self.wordType}"

	def the_word(self) -> str:
		return self.theWord

	def the_word_type(self) -> str:
		return self.wordType

class Words:
	def __init__(self):
		self.wordList = []

	def clear(self) -> None:
		self.wordList = []
		
	def add_word(self, theWord: Word) -> None:
		self.wordList.append(theWord)

	def word_type(self, a_word: str) -> WordType | None:
		a_word = a_word.lower()
		word_list = [x.the_word() for x in self.wordList]
		word_list_types = [x.wordType for x in self.wordList]
		if a_word in word_list:
			the_word_idx = word_list.index(a_word)
			the_word_type = word_list_types[the_word_idx]
			return the_word_type
		else:
			return None

	def dump_words(self) -> list[str]:
		result = []
		for word in self.wordList:
			# result.append(word.theWord)
			result.append(f"{word=}")
		return result

global_words = Words()
