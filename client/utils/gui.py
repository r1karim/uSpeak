import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction
from PyQt5 import QtWidgets


class window_frame(QMainWindow):
	def __init__(self, app, win_title, x, y, width, height, stylesheet='', resizable=True):
		QMainWindow.__init__(self)
		self.app = app
		self.setWindowTitle(win_title)
		self.setGeometry(x, y, width, height)

		if not resizable:
			self.setFixedSize(self.size())
		
		self.setStyleSheet(stylesheet)

	def gui_show(self):
		self.show()
		sys.exit(self.app.exec_())

class input_field(QtWidgets.QLineEdit):
	def __init__(self, frame, x, y, placeholder, stylesheet=''):
		QtWidgets.QLineEdit.__init__(self, frame)
		self.move(x,y)
		self.setPlaceholderText(placeholder)
		self.setStyleSheet(stylesheet)

class text_field(QtWidgets.QTextEdit):
	def __init__(self, frame, x, y, placeholder, stylesheet=''):
		QtWidgets.QTextEdit.__init__(self, frame)
		self.move(x,y)
		self.setPlaceholderText(placeholder)
		self.setStyleSheet(stylesheet)
	

class button(QtWidgets.QPushButton):
	def __init__(self, frame, text,x, y, click_func,stylesheet=''):
		QtWidgets.QPushButton.__init__(self, frame)
		self.move(x, y)
		self.setText(text)
		self.setStyleSheet(stylesheet)
		self.clicked.connect(click_func)