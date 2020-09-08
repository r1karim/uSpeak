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
	while text.find('  ') != -1:
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
		try:
			target_user = [target_user for target_user in network.Network.online_users if target_user.get_user_name() == param1][0]
			target_user.send_message(globalsettings.SERVER_MESSAGE, {'channel_name': channel_name, 'message': 'You have been kicked from the chat.'})
			target_user.kick_user()
			[spec_user.send_message(globalsettings.SERVER_MESSAGE, {'channel_name': channel_name, 'message': target_user.get_user_name() + ' has been kicked from the chat by server administrator ' + user.get_user_name()}) for spec_user in network.Network.online_users]
			[spec_user.send_message(globalsettings.SERVER_DETAILS, {'users': network.Network.online_users}) for spec_user in network.Network.online_users]
		except IndexError:
			user.send_message(globalsettings.SERVER_MESSAGE, {'channel_name': channel_name, 'message': 'Invalid username'})

	else:
		user.send_message(globalsettings.SERVER_MESSAGE, {'channel_name': channel_name, 'message': 'You do not have permission to use this command.'})

