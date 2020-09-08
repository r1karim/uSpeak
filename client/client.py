import sys, time, os
from PyQt5.QtWidgets import QApplication, QAction, QListWidget
from PyQt5.QtGui import QIcon
from utils.events import Event
from utils.gui import *
from utils.network import Network
from utils import settings as globalsettings
from threading import Thread
from win32api import GetSystemMetrics


client_app = QApplication(sys.argv)

def main(arguments):
	print("Loading client...")
	try:
		if len(arguments) != globalsettings.ARGUMENTS_LENGTH:
			raise Exception(f"required 3 arguments received {len(arguments)}.")

		client_frame = window_frame(client_app, "uSpeak - client", GetSystemMetrics(0) / 2 - globalsettings.CLIENT_SCREEN_WIDTH / 2, GetSystemMetrics(1) / 2 - globalsettings.CLIENT_SCREEN_HEIGHT / 2, globalsettings.CLIENT_SCREEN_WIDTH, globalsettings.CLIENT_SCREEN_HEIGHT , stylesheet='', resizable=False)

		chat_box = text_field(client_frame, 10, 32, '')
		chat_box.setReadOnly(True)
		chat_box.resize(470, 350)
		
		userlist = QListWidget(client_frame)
		userlist.move(520, 32)
		userlist.resize(100, 120)

		channellist = QListWidget(client_frame)
		channellist.itemClicked.connect(lambda item: event.set_selected_channel(item))

		channellist.move(520, 160)
		channellist.resize(100, 200)

		chat_input = input_field(client_frame, 10, 387, 'Message #selected channel')
		chat_input.resize(470, 30)


		message_button = button(client_frame, "Send message", 520, 387, lambda: client.send_message(globalsettings.USER_MESSAGE, event.selected_channel, event.get_input_text()))
		chat_input.returnPressed.connect(message_button.click)

		exitAct = QAction(QIcon(''), '&Disconnect', client_frame)
		exitAct.triggered.connect(os._exit)

		menubar = client_frame.menuBar()
		server_menu = menubar.addMenu('Server')
		action = server_menu.addAction(exitAct)

		event = Event(chat_box, chat_input, userlist, channellist)

		client = Network(arguments[0], int(arguments[1]), arguments[2], event)
		client.establish_connection()
		time.sleep(0.3)
		event.set_selected_channel(channellist.item(0))
		client_frame.gui_show()

	except Exception as exception:
		print(f"{exception}")
		print('test')
		exit()

	except IndexError:
		print(f"Required 3 arguments received {len(arguments)}.")
		exit()

	except:
		pass

if __name__ == '__main__':
	main(sys.argv[1:])