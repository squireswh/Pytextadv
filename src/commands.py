# commands.py
#
# (c) 2026
# ClicKill Microbits

class Command:
	def __init__(self, cmd: str, cmd_alias: str, req_args: int, built_in: bool = True):
		self.__command = cmd
		self.__alias = cmd_alias
		self.__required_args = req_args
		self.__closure = None
		self.__built_in = built_in

	def __repr__(self) -> str:
		return f"{self.__command} ({self.__alias}): req: {self.__required_args}, built_in: {self.__built_in}"

	def is_good_command(self, other: str) -> bool:
		if other.lower() == self.__command.lower():
			return True
		elif other.lower() == self.__alias.lower():
			return True
		return False

	def required_args(self) -> int:
		return self.__required_args

	def cmd_alias(self) -> str:
		return self.__alias

	def cmd_command(self) -> str:
		return self.__command

	def built_in(self) -> bool:
		return self.__built_in
