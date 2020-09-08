class Command():
	server_commands = set()

	def __init__(self, command_text, command_func):
		self.text = command_text
		self.func = command_func
		Command.server_commands.add(self)

	def execute(self, *args):
		self.func(*args)


	def __str__(self):
		return self.text