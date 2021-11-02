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
import jwt
import json
import hashlib
from src.error import InputError

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
            'password': hash_password(password), 
            'name_first': name_first,
            'name_last': name_last, 
            'handle_str': create_handle(name_first, name_last),
            'channel_id_owners': [],
            'channel_id_members': [],
            'is_global_owner': is_global_owner,
            'messages_created':[],
            'session_list': [],
            'notifications': [],
            'sent_messages': [],
    }

# Function to make message dictionary and returns message_id
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
def create_token(user, session_id):
    SECRET = 'abcdedweidjwijdokfwkfwoqkqfw'
    token = jwt.encode({'auth_user_id': user['u_id'], 'session_id': session_id}, SECRET, algorithm='HS256')
    logged_in_users.append(token)
    return token

# Decoding function for encoded jwt
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
            if user['session_list'].count(payload['session_id']) != 0:
                return payload
        return False

# Token checker for logged_in_users
def token_check(token):
    store = logged_in_users
    if token in store: 
        return token
    return False

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_valid_user_id(auth_user_id):
    store = data_store.get()
    for user in store['users']:
        if user['u_id'] == auth_user_id:
            return True
    return False

# Checks for existence of dm_id in dms
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

# Function used to list all channels that a user is part of.

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

# Function to list all channels in the database.

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

# Function to leave a channel given the token and channel_id. It returns if a member 
# was found or not.

def leave_channel(token, channel_id):
    data = data_store.get()
    user_id = token_to_user_id(token)
    for channel in data['channels']:
        if channel_id == channel['channel_id']:
            #Remove the user from the owner members if they are an owner 
            for owner in channel['owner_members']:
                if owner == user_id:
                    channel['owner_members'].remove(user_id)
                    break
            #Remove the user for the member list
            valid_member = False
            for member in channel['all_members']:  
                if user_id == member: 
                    channel['all_members'].remove(user_id)
                    valid_member = True
                    break
    return valid_member

# Function to add a new owner to the channel.

def add_owner_channel(channel_id, u_id):
    data = data_store.get()
    new_owner_id = u_id  
    for channel in data['channels']:	
        if channel["channel_id"] == channel_id:
            channel['owner_members'].append(new_owner_id)
            break
    return {}

# Function to remove an owner from a channel.

def remove_owner_channel(channel_id, u_id):
    data = data_store.get()
    new_owner_id = u_id  
    for channel in data['channels']:	
        if channel["channel_id"] == channel_id:
            channel['owner_members'].remove(new_owner_id)
            break
    return {}

# def functions to help with Channel create, channels_list and channels_listall 

def is_public_check(is_public):
    if is_public == True or is_public == False:
        return True
    return False 

# Function to check handle uniqueness
def handle_check(handle_str):
    data = data_store.get()
    for user in data['users']:
        if user['handle_str'] == handle_str:
            return True
    return False

# Check for auth_user_id 
def auth_user_id_check(auth_user_id):
    data = data_store.get()
    for user in data['users']:
        if int(user['u_id']) == int(auth_user_id):
            return user
    return False

# Function check email validity
def email_check(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if (re.fullmatch(regex, email)):
        return True
    else:
        return False

# Function check repeated emails
def email_repeat_check(email):
    data = data_store.get()
    for user in data['users']:
        if user['email'] == email:
            return True
    return False

# Function to return user based on email
def login_email(email):
    data = data_store.get()
    for user in data['users']:
        if user['email'] == email:
            return user
    return False

# Function to return user with correct password
def password_check(password):
    data = data_store.get()
    for user in data['users']:
        if user['password'] == hash_password(password):
            return user
    return False

# Function to check message_id in respective channel and message
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


################################
#Helper Function for message.py#
################################
def owner_channel_check(token, channel_id):
    u_id = token_to_user_id(token)                  #checks if it's a valid user
    channel = channel_id_check(channel_id)
    if channel == None:
        raise InputError

    for member in channel['owner_members']:     
        if member == u_id:
            return True
    return False
#############################
# Helper Functions for dm.py#
#############################
def find_user(u_id):
    store = data_store.get()
    for user in store['users']:
        if user['u_id'] == u_id:
            return user

def find_dm(dm_id, store):
    for dm in store['dms']:
        if dm['dm_id'] == dm_id:
            return dm

def find_channel(channel_id, data):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            return channel

# Checks if dm_id exists within dm
def is_valid_dm_id(dm_id):
    store = data_store.get()
    for dm in store['dms']:
        if dm['dm_id'] == dm_id:
            return True
    return False

# Checks if user member is in channel
def is_user_in_channel(channel_id, user_id):
    store = data_store.get()
    channel = find_channel(channel_id, store)
    for member in channel['members']:
        if member['user_id'] == user_id:
            return True
    return False

# Checks if user member is in dm
def is_user_in_dm(dm_id, user_id):
    store = data_store.get()
    dm = find_dm(dm_id, store)
    for member in dm['members']:
        if member == user_id:
            return True
    if dm['creator'] == user_id:
        return True
    return False

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

