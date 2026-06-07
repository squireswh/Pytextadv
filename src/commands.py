# commands.py
#
# (c) 2026
# ClicKill Microbits

class Command:
	def __init__(self, cmd: str, cmd_alias: str, req_args: int):
		self.__command = cmd
		self.__alias = cmd_alias
		self.__required_args = req_args
		self.__closure = None

	def __repr__(self) -> str:
		return f"{self.__command} ({self.__alias}): req: {self.__required_args}"

	def is_good_command(self, other: str) -> bool:
		if other.lower() == self.__command.lower():
			return True
		elif other.lower() == self.__alias.lower():
			return True
		return False

	def required_args(self) -> int:
		return self.__required_args
