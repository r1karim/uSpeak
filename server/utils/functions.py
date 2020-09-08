''' Functions that does not belong to a class goes here '''

from . import network, settings as globalsettings

def update_dict(spec_dict, newkey, newvalue):
	spec_dict.update({newkey: newvalue})
	return spec_dict

def append_return(list, item):
	if item not in list:
		list.append(item)
	return item

def split(text):
	text.replace('  ', ' ')
	return text.split(' ')


def rcon(user, channel_name, param, param1=''):

	if param == 'login' and not user.is_admin():
		if network.Network.rcon_password == param1:
			user.set_admin(True)
			user.send_message(globalsettings.SERVER_MESSAGE, {'channel_name': channel_name, "message": "You have successfuly logged in as a server administrator."})

		else:
			user.send_message(globalsettings.SERVER_MESSAGE, {'channel_name': channel_name, 'message': 'the given password is incorrect.'})
	
	elif user.admin and param == 'help':
		
		user.send_message(globalsettings.SERVER_MESSAGE, {'channel_name': channel_name, 'message': "\n________uSpeak711 RCON - Help________\n/rcon kick [username] -> To kick a user\n\
/rcon say [text] -> To send a message as a server administrator"})

	elif user.admin and param == 'kick':
		pass


	else:
		user.send_message(globalsettings.SERVER_MESSAGE, {'channel_name': channel_name, 'message': 'You do not have permission to use this command.'})

