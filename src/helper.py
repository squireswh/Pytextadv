# helper.py
#
# (c) 2026
# ClicKill Microbits
#
# This module just implements some helper functions.

special_cases = ['historic']

# This function returns the correct article ('a' | 'an') given the word that will
# follow the article.
#
# Ex:
# * aan('tree') -> 'a'
# * aan('eyeball') -> 'an'
def aan(word: str) -> str:
	if len(word) > 0:
		vowels = "aeiouyAEIOUY"
		first_ltr = word[0]
		if first_ltr in vowels:
			return "an "
		else:
			if word.lower() in special_cases:
				return "an "
			else:
				return "a "
	else:
		return ""


# This function takes a string of the form, '<adjective> <noun>'
# and returns the adjective as the 1st element of a 2-tuple, and
# the noun as the 2nd element.
def split_noun_adj(s: str) -> (str, str):
	args = s.split(' ')
	return (args[0], args[1])

# This function simply encloses a string with double-quote marks.
def quote_it(s: str) -> str:
	return f'"{s}"'

# This function simply encloses a string with single-quote marks.
def single_quote_it(s: str) -> str:
	return f"'{s}'"

# This function provides the Python equivalent to the BASIC LEFT$ keyword.
def left_str(s: str, num_chars: int) -> str:
	return s[:num_chars]

# This function provides the Python equivalent to the BASIC RIGHT$ keyword.
def right_str(s: str, num_chars: int) -> str:
	minus_n = -1 * num_chars
	return s[minus_n:]

# This function provides the Python equivalent to the BASIC INSTR keyword when
# the first argument is an integer.
def instr_str_explicit(start_idx: int, s: str, substr: str) -> int:
	if start_idx < 1:
		return 0
	test_str = s
	if start_idx > len(s):
		return 0
	if start_idx > 1:
		test_str = s[start_idx - 1:]
	result = test_str.find(substr) + 1
	return result

# This function provides the Python equivalent to the BASIC INSTR keyword when
# the first argument is a string.
def instr_str(s: str, substr: str) -> int:
	return instr_str_explicit(1, s, substr)

# This function provides the Python equivalent to the BASIC MID$ keyword.
def mid_str(s: str, idx: int, num_chars=1) -> str:
	return s[idx-1:(idx+num_chars)-1]
