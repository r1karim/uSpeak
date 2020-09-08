import socket, pickle
from . import settings as globalsettings
from threading import Thread


class Network():

	server_channels = []
	server_users = []

	def __init__(self, srv_ip, srv_port, username, gui_event):
		self.sock = socket.socket()
		self.ip = srv_ip

		if self.ip == '127.0.0.1' or self.ip == 'localhost':
			self.ip = socket.gethostname()

		self.port = srv_port
		self.username = username
		self.listen_thread = Thread(target=self.listen)

		self.event = gui_event

		print(f"Connection created ip: {self.ip} port: {self.port} username {self.username}")

	def establish_connection(self):
		self.sock.connect((self.ip, self.port))
		self.sock.send(self.username.encode('UTF-8'))
		self.listen_thread.start()

	def listen(self):
		while True:
			try:
				try:
					data_in_bytes = self.sock.recv(globalsettings.BUFFER_SIZE)
				except:
					pass

				data = pickle.loads(data_in_bytes)

				if data['type'] == globalsettings.SERVER_DETAILS:

					try:
						if data['message']['channels']:
							Network.server_channels = data['message']['channels']
							self.event.channels_list.clear()
							self.event.channels_list.addItems([channel['channel_name'] for channel in Network.server_channels])
					except:
						pass

					try:
						if data['message']['users']:
							Network.server_users = data['message']['users']
							self.event.users_list.clear()
							self.event.users_list.addItems([user['username'] for user in Network.server_users])
					except:
						pass

				elif data['type'] == globalsettings.SERVER_MESSAGE or data['type'] == globalsettings.USER_LEFT:
					
					if data['type'] == globalsettings.USER_LEFT:

						data['message']['message'] = f"<{data['message']['time'].hour}:{data['message']['time'].minute}:{data['message']['time'].second}>" + ' ' + data['message']['username'] + ' has left the chat'
						Network.server_users = [user for user in Network.server_users if user['username'] != data['message']['username']]
						self.event.users_list.clear()
						self.event.users_list.addItems([user['username'] for user in Network.server_users])

					[channel for channel in Network.server_channels if channel['channel_name'] == data['message']['channel_name']][0]['messages'].append(data['message']['message'])
					
					if self.event.selected_channel == data['message']['channel_name']:
					
						self.event.chat_box.append(data['message']['message'])


			
			except Exception as exception:
				print(exception)


	def disconnect(self):
		self.sock.close()

	def send_message(self, msgtype, channel,message):
		if channel and message:
			self.sock.send(pickle.dumps({'type': msgtype, 'channel_name': channel,'message': message}))