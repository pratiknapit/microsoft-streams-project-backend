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
from json import dumps
import jwt
import json

initial_object = {
    'users': [    
    ],
    'channels': [
    ],
    'dms': [
    ],
}
# Channels Helper Check Functions 

# Function to give user id given token 
def token_to_user_id(token):
    store = data_store.get()
    for user in store['users']:
        if user['token'] == token:
            return user['u_id']
    return False

#Need to ask about if we add u_id or token to the members/owners list 
def make_channel(channel_id, name, is_public):

    #u_id = token_to_user_id(token)

    return {
        'channel_id': channel_id, 
        'name': name,
        'is_public': is_public,
        'owner_members': [],
        'all_members': [],
        'Messages': [],
    }
        
# Function to add_channel to list 
def add_channel(token, name, is_public):
    store = data_store.get()                                                    # retrieve data from initial_object data base
    channel_id = len(store['channels']) + 1                                   
    channel = make_channel(channel_id, name, is_public)
    u_id = token_to_user_id(token)
    channel['owner_members'].append(u_id)
    channel['all_members'].append(u_id)

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
            'is_global_owner': is_global_owner,
            'messages_created':[],
    }

def make_message(message, channel_id, u_id): 
    m_id = 0
    channels = data_store.get()['channels']
    for channel in channels:
        m_id += len(channel['Messages'])
    message_id = m_id + 1
    user = user_id_check(u_id)
    user['messages_created'].append(message_id)

    channel = channel_id_check(channel_id)
    channel['Messages'].append({
                            'channel_id': channel_id, 
                            'message_id': message_id, 
                            'u_id': u_id, 
                            'message': message, 
                            })
    return message_id

logged_in_users = []
def login_token(user):
    SECRET = 'abcdedweidjwijdokfwkfwoqkqfw'
    #token = str(jwt.encode({'handle_str': user['handle_str']}, SECRET, algorithm = 'HS256'))
    token = jwt.encode({'auth_user_id': user['u_id']}, SECRET, algorithm='HS256')
    logged_in_users.append(token)
    return token


def is_valid_token(token):
    data = data_store.get()
    SECRET = 'abcdedweidjwijdokfwkfwoqkqfw'
    try:
        payload = jwt.decode(token, SECRET, algorithms=['HS256'])
    except:
        jwt.exceptions.InvalidSignatureError()
        return False
    else:
        user = next(
            (user for user in data['users'] if user['u_id'] == payload['auth_user_id']), False)
        if user:
            return payload
        return False

def token_check(token):
    store = logged_in_users
    if token in store: 
        return token
    return False

def is_valid_user_id(auth_user_id):
    store = data_store.get()
    for user in store['users']:
        if user['u_id'] == auth_user_id:
            return True
    return False

def dm_id_check(dm_id):
    store = data_store.get()
    for dm in store['dms']:
        if dm['dm_id'] == dm_id:
            return True
    return False

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


def user_channels(token):
    u_id = token_to_user_id(token)
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

def user_all_channels(token):
    store = data_store.get()    
    all_channels_list = {
        'channels': [

        ]
    }
    for channel in store['channels']:
        all_channels_list['channels'].append(
            {'channel_id': channel['channel_id'], 'name': channel['name']}
        )
  
    return all_channels_list

# def functions to help with Channel create, channels_list and channels_listall 

def is_public_check(is_public):
    if is_public == True or is_public == False:
        return True
    return False 

def handle_check(handle_str):   # Function to check handle uniqueness
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

def message_id_check(message_id):
    channels = data_store.get()['channels']
    for channel in channels:
        for message in channel['Messages']:
            if message['message_id'] == message_id:
                return message
    return None

def channel_id_check(channel_id):
	store = data_store.get()
	for channel in store['channels']:
		if int(channel['channel_id']) == int(channel_id):
			return channel	
	return False

def check_existing_owner(u_id, channel_id):
    data = data_store.get()
    current_owner = False
    for channel in data['channels']:
        if channel["channel_id"] == channel_id:
            for owner in channel['owner_members']:
	            if u_id == owner:
		            current_owner = True 
    return current_owner

def check_existing_member(u_id, channel_id):
    data = data_store.get()
    result = False
    for channel in data['channels']:
        if int(channel['channel_id']) == int(channel_id):
            for mem in channel['all_members']:
	            if mem == u_id:
		            result = True 
    return result

def check_if_user_is_channel_member(token, channel_id):
    auth_user_id = token_to_user_id(token)
    store = data_store.get()
    user = auth_user_id_check(auth_user_id) 
    if user == False:
        return False
    result = False 
    for channel in store['channels']:
        if int(channel['channel_id']) == int(channel_id):
            for member in channel['all_members']:
                if member == auth_user_id:
                    result = True 
    return result


def check_if_channel_is_public_or_private(channel_id):
    store = data_store.get()
    for channel in store['channels']:
        if int(channel['channel_id']) == int(channel_id):
            return channel['is_public']
            
def user_id_check(u_id):
    data = data_store.get()
    for user in data['users']:
        if int(user['u_id']) == int(u_id):
            return user
    return False

def handle_search(handle):
    data = data_store.get()
    for user in data['users']:
        if user['handle_str'] == handle:
            return user


def save_data(data):
    with open('data.json', 'w') as FILE:
        json.dump(data, FILE)

## YOU SHOULD MODIFY THIS OBJECT ABOVE

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

