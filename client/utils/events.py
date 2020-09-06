''' Event functions '''
from .network import Network

class Event():

	def __init__(self, chat_box, chat_input, users_list, channels_list):

		self.chat_box = chat_box
		self.chat_input = chat_input
		self.users_list = users_list
		self.channels_list = channels_list

		self.selected_channel = ''
		print('Event class has been initiliazed')

	def get_input_text(self):
		text = self.chat_input.text()
		self.chat_input.setText('')
		return text

	def set_selected_channel(self, item):
		if type(item) == str:
			self.selected_channel = item
			self.chat_box.setText('\n'.join([channel for channel in Network.server_channels if channel['channel_name'] == self.selected_channel][0].get('messages')))
		else:
			self.selected_channel = item.text()
			self.chat_box.setText('\n'.join([channel for channel in Network.server_channels if channel['channel_name'] == self.selected_channel][0].get('messages')))