from . import settings as globalsettings
import configparser

config = configparser.ConfigParser()

def load(file_loc):
	config.read(file_loc)
	return {'hostname': config.get("main", "hostname"), 'port': int(config.get("main", "port")), 'max_users': int(config.get("main", "max_users")), 'rcon': config.get("main", "rcon_pass"), 'channels': config.get("main", "channels").split(',')}

def load_config(file_loc):
	if file_loc:
		try:
			server_settings = load(file_loc)

		except configparser.Error:
			config['main'] = {
				'hostname': globalsettings.DEFAULT_HOST_NAME,
				'port': str(globalsettings.DEFAULT_SERVER_PORT),
				'max_users': str(globalsettings.DEFAULT_MAX_USERS),
				'rcon_pass': str(globalsettings.DEFAULT_SERVER_RCON),
				'channels': str(globalsettings.DEFAULT_CHANNELS)
			}
			with open(file_loc, 'w') as config_file:
				config.write(config_file)

			server_settings = load(file_loc)
		return server_settings

	else:
		raise Exception("Config file have not been specified.")