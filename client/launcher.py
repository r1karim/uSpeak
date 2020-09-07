import sys, subprocess
from PyQt5.QtWidgets import QApplication
from utils.gui import *
from win32api import GetSystemMetrics
from utils import settings as globalsettings

def get_data_from_user():
	global frame

	try:
		username = frame.username_input.text()
		server_ip = frame.ip_input.text()
		server_port = frame.port_input.text()

		if not username or not server_ip:
			raise Exception("You need to fill both the username and the server ip.")
	
		server_port = int(server_port)
	
	except ValueError:
		frame.log.setText(frame.log.toPlainText()  + f"ERROR: Could not connect because the following port is not valid: {server_port}" + "\n")
	
	except Exception as exception:
		frame.log.setText(frame.log.toPlainText()  + f"ERROR: Could not connect because: {exception}" + "\n")
	
	else:
		frame.log.setText(frame.log.toPlainText()  + f"Connecting to {server_ip}:{server_port} as {username}..." + "\n")
		subprocess.Popen(f"python client.py {server_ip} {server_port} {username}", shell=True)
		sys.exit()

	return None

application = QApplication(sys.argv)

X, Y = GetSystemMetrics(0) / 2 - globalsettings.LAUNCHER_SCREEN_WIDTH / 2, GetSystemMetrics(1) / 2 - globalsettings.LAUNCHER_SCREEN_HEIGHT / 2 - 72

frame = window_frame(application, 'uSpeak - Launcher', X, Y, globalsettings.LAUNCHER_SCREEN_WIDTH, globalsettings.LAUNCHER_SCREEN_HEIGHT, stylesheet="background-color: rgb(42,42,42); color: white;", resizable=False)
frame.username_input = input_field(frame, 10, 10, 'username', stylesheet='background-color: grey;')
frame.ip_input = input_field(frame, 120, 10, 'server ip', stylesheet='background-color: grey;')
frame.port_input = input_field(frame, 230, 10, 'port', stylesheet='background-color: grey;')

if globalsettings.DEBUG_MODE:
	frame.username_input.setText("user711")
	frame.ip_input.setText("127.0.0.1")
	frame.port_input.setText("7777")

frame.log = text_field(frame, 120, 54, '', stylesheet='background-color: black;')
frame.log.setReadOnly(True)
frame.log.resize(210, 60)
frame.button = button(frame, 'Connect', 10, 54, get_data_from_user, 'background-color: rgb(47, 121, 181)')

frame.gui_show()