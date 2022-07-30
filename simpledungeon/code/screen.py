import os
from code import util, terminal



def build_padded_string(string):
	"""Return a string built to the correct length"""
	padding = int((60-len(string))/2)
	_str = "| " + (" "*padding) + string + (" "*padding)
	if len(_str) == 62:
		_str += "  |"
	elif len(_str) == 61:
		_str += "   |"
	else:
		_str += " |"

	return _str


def balance_strings(strings):
	"""Return a list of strings with equal length"""

	longest = ""

	for string in strings:
		if len(string) > len(longest):
			longest = string

	balanced_strings = []

	for string in strings:
		while len(string) != len(longest):
			string += " "
		balanced_strings.append(string)

	return balanced_strings



class Screen():
	def __init__(self):
		"""Initiate the screen Object"""
		self.width = 0
		self.height = 0

	def update_size(self):
		"""Update the screen size"""
		size = os.get_terminal_size()

		if size.columns != self.width or size.lines != self.height:
			terminal.clear()

  
		self.width = size.columns
		self.height = size.lines


	def display_out(self, string_list):
		"""Display a multiline string in the center of the screen"""

		self.update_size()

		length_of_string = len(string_list[0])
		height_of_string = len(string_list)

		padding_width = int((self.width - length_of_string) / 2)
		padding_height = int((self.height - height_of_string) / 2)

		print("\n"*padding_height)

		for string in string_list:
			print((" "*padding_width)+string)


	def center(self, string):
		"""Return a centered string"""

		length_of_string = len(string)

		padding = int((61-length_of_string)/2)

		return (" "*padding)+string+(" "*padding)

	def build_out_string(self, m_string):
		self.update_size()

		old_strings = m_string.split("\n")

		length_of_string = 56
		height_of_string = len(old_strings)

		padding_width = int((self.width - length_of_string) / 2)
		padding_height = int((self.height - height_of_string) / 2)

		new_string = "\n"*padding_height
		
		for string in old_strings:
			new_string += (" "*padding_width) + string + "\n"

		return new_string


	def display_card(self, player, content):
		"""Show a card from a line of content"""

		content = balance_strings(content)

		terminal.clear()

		length_of_content = len(content)

		if length_of_content > 60:
			asdfadfadf; # Throw error for now

		else:
			spacing = int((60-length_of_content) /  2)

			out = []

			out.append("---"*21+"--") # it works, don't question it.
			for stat in [player.get_stats()]:
				out.append(build_padded_string(stat))

			out.append("---"*21+"--")

			for line in content:
				out.append(build_padded_string(line))


			for i in range(23-len(out)):
				out.append("|"+(" "*63)+"|")


			out.append("-"*65)
			out.append("\n")
			out.append("\n")

		self.display_out(out)



	def ask_question(self, player, question, raw_prompts=[]):
		"""Display a question with multiple options to choose from, return result"""

		prompts = balance_strings(raw_prompts)

		terminal.clear()

		length_of_question = len(question)

		if length_of_question > 60:
			aldkjf;alkdjf; # throw an error for now

		else:
			spacing = int((60-length_of_question) / 2)

			out = []

			out.append("---"*21+"--") # it works, don't question it.
			for stat in [player.get_stats()]:
				out.append(build_padded_string(stat))

			out.append("---"*21+"--")

			for i in range(3):
				out.append("|"+(" "*63)+"|")

			out.append(build_padded_string(question))

			for i in range(2):
				out.append("|"+(" "*63)+"|")


			for prompt in prompts:
				p = "["+str(prompts.index(prompt))+"] "+prompt
				out.append(build_padded_string(p))

			for i in range(23-len(out)):
				out.append("|"+(" "*63)+"|")


			out.append("-"*65)
			out.append("\n")
			out.append("\n")


			self.display_out(out)

			val = util.get_int(_max=len(raw_prompts)-1)

			return raw_prompts[val].lower()

