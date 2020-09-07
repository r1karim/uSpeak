from .network import Network

class Event():

	def __init__(self, chat_box, chat_input, users_list, channels_list):

		self.chat_box = chat_box
		self.chat_input = chat_input
		self.users_list = users_list
		self.channels_list = channels_list
		self.selected_channel = ''

	def get_input_text(self):
		result_text = self.chat_input.text()
		self.chat_input.setText('')
		return result_text

	def set_selected_channel(self, item):
		
		self.selected_channel = item
		
		if type(item) != str:
			self.selected_channel = item.text()
		
		self.chat_box.setText('\n'.join([channel for channel in Network.server_channels if channel['channel_name'] == self.selected_channel][0].get('messages')))

	def __str__(self):
		return "event instance"