import sys
from utils.network import Network
from utils import settings as globalsettings
from utils import config


def main():
	server_settings = config.load_config(globalsettings.CONFIG_FILE_LOCATION)
	server = Network(server_settings['hostname'], server_settings['port'], server_settings['max_users'], server_settings['rcon'], server_settings['channels'])
	
	server.start()

if __name__ == '__main__':
	main()