'''
data_store.py

This contains a definition for a Datastore class which you should use to store your data.
You don't need to understand how it works at this point, just how to use it :)

The data_store variable is global, meaning that so long as you import it into any
python file in src, you can access its contents.

Example usage:

    from data_store import data_store

    store = data_store.get()
    print(store) # Prints { 'names': ['Nick', 'Emily', 'Hayden', 'Rob'] }

    names = store['names']

    names.remove('Rob')
    names.append('Jake')
    names.sort()

    print(store) # Prints { 'names': ['Emily', 'Hayden', 'Jake', 'Nick'] }
    data_store.set(store)
'''
import re

initial_object = {
    'users': [    
    ],
    'channels': [
    ],
}
# Channels Helper Check Functions 

# Function to make_channel dictionary
def make_channel(u_id, channel_id, name, is_public):

    return {
        'channel_id': channel_id, 
        'name': name,
        'is_public': is_public,
        'owner_members': [u_id],
        'all_members': [u_id],
        'Messages': [],
    }


# Function to add_channel to list 
def add_channel(u_id, name, is_public):
    store = data_store.get()                                                    # retrieve data from initial_object data base
    channel_id = len(store['channels']) + 1                                   
    channel = make_channel(u_id, channel_id, name, is_public)
    store['channels'].append(channel)

    data_store.set(store) 
    return channel

# Function to add_user to list 
def add_user(email, password, name_first, name_last):

    store = data_store.get()                                                  
    u_id = len(store['users']) + 1
    user = make_user(email, password, name_first, name_last, u_id)   
    store['users'].append(user)
    data_store.set(store)
    return user

# Function to make user
def make_user(email, password, name_first, name_last, u_id):                    
    store = data_store.get() 
    is_global_owner = 2
    if len(store['users']) == 0:
        is_global_owner = 1

    return {
            'u_id': u_id,
            'email': email,  
            'password': password, 
            'name_first': name_first,
            'name_last': name_last, 
            'handle_str': create_handle(name_first, name_last),
            'channel_id_owners': [],
            'channel_id_members': [],
            'is_global_owner': is_global_owner
    }

# Function to create_handle
def create_handle(first_name, last_name):

    prototype_handle = first_name + last_name                                   # Concatenation of first and last name
    prototype_handle = prototype_handle.lower()                                 # lowercased string

    if len(prototype_handle) > 20:                                              # Ensure handle size less than 20 chars
            prototype_handle = prototype_handle[0:20]
    
    first_proto = prototype_handle
    count = 0
    while handle_check(prototype_handle) == True:
        prototype_handle = first_proto + str(count)
        count += 1   
    return prototype_handle
        

def user_channels(u_id):
    store = data_store.get()
    user_list_channel = {
        'channels': [
        ],
    }
    for channel in store['channels']: 
        for member in channel['all_members']:
            if member == u_id:
                user_list_channel['channels'].append(
                    {'channel_id': channel['channel_id'], 'name': channel['name']}
                )
        
    return user_list_channel

# def function to return list of channels that user is part of including private channels

def user_all_channels(u_id):
    store = data_store.get()    

    all_channels_list = {
        'channels': [

        ],
    }
    for channel in store['channels']:
        all_channels_list['channels'].append(
            {'channel_id': channel['channel_id'], 'name': channel['name']}
        )
  
    return all_channels_list

# def functions to help with Channel create, channels_list and channels_listall 

#check if channel is in our database and returns it. 
def channel_check(channel_id):
    store = data_store.get()

    for channel in store['channels']:
        if int(channel['channel_id']) == int(channel_id):
            return channel 
    
    return False

def is_public_check(is_public):
    if is_public == True or is_public == False:
        return True
    return False 

def handle_check(handle_str):                                                   # Function to check handle uniqueness
    data = data_store.get()
    for user in data['users']:
        if user['handle_str'] == handle_str:
            return True
    return False

def auth_user_id_check(auth_user_id):
    data = data_store.get()
    for user in data['users']:
        if int(user['u_id']) == int(auth_user_id):
            return user
    return False

def email_check(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if (re.fullmatch(regex, email)):
        return True
    else:
        return False

def email_repeat_check(email):
    data = data_store.get()
    for user in data['users']:
        if user['email'] == email:
            return True
    return False

def login_email(email):
    data = data_store.get()
    for user in data['users']:
        if user['email'] == email:
            return user
    return False

def password_check(password):
    data = data_store.get()
    for user in data['users']:
        if user['password'] == password:
            return user
    return False

def message_check(message_id):
    data = data_store.get()
    for message in data['Messages']:
        if int(message['message_id']) == int(message_id):
            return message
    return None

def channel_id_check(channel_id):
	store = data_store.get()
	for channel in store['channels']:
		if int(channel['channel_id']) == int(channel_id):
			return channel
	
	return False

def check_if_user_is_channel_member(auth_user_id, channel_id):
    store = data_store.get()
    user = auth_user_id_check(auth_user_id) 
    if user == False:
        return False
    value = False 
    for Dict in store['channels']:
        if int(Dict['channel_id']) == int(channel_id):
            for member in Dict['all_members']:
                if member == user['u_id']:
                    value = True 
    return value

def check_if_channel_is_public_or_private(channel_id):
    store = data_store.get()
    channel_storage = channel_id_check(channel_id)
    for channel in store['channels']:
        if channel['channel_id'] == channel_storage['channel_id']:
            return channel['is_public']
            
def user_id_check(u_id):
    data = data_store.get()
    for user in data['users']:
        if int(user['u_id']) == int(u_id):
            return user
    return False

def msg_channel_check(channel_id):
    data = data_store.get()
    for msg in data['Messages']:
        if msg['channel_id'] == channel_id:
            return True
    return False


###################################################################
class Datastore:
    def __init__(self):
        self.__store = initial_object

    def get(self):
        return self.__store

    def set(self, store):
        if not isinstance(store, dict):
            raise TypeError('store must be of type dictionary')
        self.__store = store

print('Loading Datastore...')

global data_store
data_store = Datastore()

