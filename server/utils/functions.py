''' Functions that does not belong to a class goes here '''

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