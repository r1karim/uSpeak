from . import settings as globalsettings
from . import functions, command
import socket, pickle, datetime, errno, select
from threading import Thread


class User():

	def __init__(self, socket, ip, username=''):
		self.socket = socket
		self.ip = ip
		self.username = username
		self.admin = False

	def get_user_ip(self):
		return self.ip

	def set_user_name(self, new_name):
		self.username = new_name

	def get_user_name(self):
		return self.username

	def close_connection(self):
		self.socket.close()

	def send_message(self, msgtype, message):
		try:
			self.socket.send(pickle.dumps({'type': msgtype, 'message': message}))

		except ConnectionResetError:
			print('user %s has probably disconnected.' % (self.get_user_name()))
			del self

		except Exception as exception:
			print(f'Could not send message to user {self.get_user_name()} error code: {exception}')


class Network():

	online_users = []

	def __init__(self, hostname, port, max_users, rcon_pass, channels):

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 10000, 3000))

		self.hostname = hostname
		self.max_users = max_users
		self.rcon_pass = rcon_pass
		self.channels = []

		[self.channels.append({'channel_name': channel, 'messages': []}) for channel in channels]

		self.sock.bind((socket.gethostname(), port))
		self.sock.listen(5)
		self.sock.settimeout(1)

		print(f"{hostname} has been setup with the following settings: ")
		print(f"port: {port}")
		print(f"Max user count: {max_users}")
		print(f"Rcon password: {rcon_pass}")
		print(f"Channels: {channels}")

		self.connection_thread = Thread(target=self.listen_to_connection)
		self.packets_thread = Thread(target=self.listen_to_packets)

	def start(self):

		print("Server is starting...")
		self.connection_thread.start()
		self.packets_thread.start()

	def listen_to_connection(self):
		while True:
			try:
				if len(Network.online_users) > self.max_users:
					continue
	
				socket, address = self.sock.accept()
				socket.setblocking(0)

				new_user = User(socket, address)
				new_user.set_user_name(socket.recv(globalsettings.USERNAME_BUFFER).decode('UTF-8'))

				try:

					if len([user for user in Network.online_users if user.get_user_name() == new_user.get_user_name()]):
						new_user.close_connection()
						print("closing connection for this user...")
						
					else:

						print("Adding user %s" % (new_user.get_user_name()))
						Network.online_users.append(new_user)

						temp = self.channels
						temp_users = Network.online_users
						temp_users = [{'username': user.get_user_name(), 'id': i} for i, user in  enumerate(Network.online_users)]
						[channel.update(messages=channel['messages'][len(channel['messages'])-globalsettings.MAX_LOAD_MESSAGES_COUNT:]) for channel in temp if len(channel['messages']) > globalsettings.MAX_LOAD_MESSAGES_COUNT]

						time = datetime.datetime.now()
						join_message = f"<{time.hour}:{time.minute}:{time.second}> {new_user.get_user_name()} has joined the chat."
					
						self.channels[0]['messages'].append(join_message)
						
						new_user.send_message(globalsettings.SERVER_DETAILS, {'channels': temp, 'users': temp_users})	
						[user.send_message(globalsettings.SERVER_DETAILS, {'users': temp_users}) for user in Network.online_users if user != new_user]
						[user.send_message(globalsettings.SERVER_MESSAGE, {'channel_name': self.channels[0]['channel_name'], 'message': join_message}) for user in Network.online_users if user != new_user]


				except Exception as exception:
					print(exception)
		
			except:
				pass

	def listen_to_packets(self):
		while True:
			try:
				messages = []
				for user in Network.online_users:

					try:
						messages.append(functions.update_dict(pickle.loads(user.socket.recv(globalsettings.MAX_BUFFER)), 'user', user))

					except ConnectionResetError:

						time = datetime.datetime.now()

						[user_ex.send_message(globalsettings.USER_LEFT,{'channel_name': self.channels[0]['channel_name'], 'username': user.get_user_name(), 'time': time}) for user_ex in Network.online_users if user_ex != user]
						
						self.channels[0]['messages'].append(f"<{time.hour}:{time.minute}:{time.second}> {user.get_user_name()} has left the chat.")

						Network.online_users.remove(user)

					except:
						pass

				if len(messages):

					time_text = f'<{datetime.datetime.now().hour}:{datetime.datetime.now().minute}:{datetime.datetime.now().second}>'

					for user in Network.online_users: [user.send_message(globalsettings.SERVER_MESSAGE,{'channel_name': message['channel_name'], 'message': functions.append_return([channel for channel in self.channels if channel['channel_name'] == message['channel_name']][0]['messages'], time_text + ' ' + message['user'].get_user_name() + ': ' + message['message'])}) for message in messages if message['message'][0] != globalsettings.COMMAND_PREFIX]
					
					try:
						[[cmd for cmd in command.Command.server_commands if cmd.text == split(message)[0]][0].execute(message['user'], *split(message)[1:]) for message in messages if message['message'][0] == globalsettings.COMMAND_PREFIX]
					except:
						
						continue

			except Exception as exception:
				print(exception)