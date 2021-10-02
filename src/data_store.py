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
import random

## YOU SHOULD MODIFY THIS OBJECT BELOW


initial_object = {
    'users': [    
    ],
    'channels': [
    ],
    'Messages': [
    ], 
}


#Channels functions - made by Pratik 

# def function to make channel dictionary

def make_channel(auth_user_id, channel_id, name, is_public):

    return {
        'channel_id': channel_id, #need to make this in another function
        'name': name,
        'is_public': is_public,
        'owner_members': [auth_user_id],
        'all_members': [auth_user_id]
    }


# def function to add channel to list 

def add_channel(auth_user_id, name, is_public):
    store = data_store.get() #retrieve our initial object data
    channel_id = len(store['channels']) + 1 #use this function above to get channel id, we might not even need the function 
    channel = make_channel(auth_user_id, channel_id, name, is_public)
    store['channels'].append(channel)

    data_store.set(store) #believe that this should just make sure that the data is still a dictionary
    #need to make a new list which only returns { channel_id }
    return channel

# def function to return list of channels that user is part of 


def add_user(email, password, name_first, name_last):
    
    store = data_store.get()                                                    # gets user data from initial_object
    u_id = len(name_first) + len(name_last) + len(email) + random.randrange(1, 1000)
    user = make_user(email, password, name_first, name_last, u_id)   
    store['users'].append(user)
    data_store.set(store)
    return user

def make_user(email, password, name_first, name_last, u_id):                    # Remember to Add more fields

    return {
            'u_id': u_id,
            'email': email,  
            'password': password, 
            'name_first': name_first,
            'name_last': name_last, 
            'handle_str': create_handle(name_first, name_last),

    }
    
'''
def add_message(message, channel_id, u_id, time_created):
    store = data_store.get()  
    user = user_id_check(u_id)
    message_id = len(message) + random.randrange(1, 1000)
     if time_created == 0: 
        time_created = datetime.utcnow()        
    make_msg = make_message(message, message_id, channel_id, u_id, time_created) 
    user['messages_created'].append(message)

    store['Messages'].append(make_msg)
    data_store.set(store)
    return message_id

def make_message(message, message_id, channel_id, u_id, time_created): 
    
    return {
            'channel_id': channel_id, 
            'message_id': message_id,  
            'u_id': u_id, 
            'message': message,
            'time_created': time_created,
    }
'''






def create_handle(first_name, last_name):
    
    prototype_handle = first_name + last_name                                   # Concatenation of first and last name
    prototype_handle = prototype_handle.lower()                                 # lowercased string

    if handle_check(prototype_handle):                                          # If same handle
        prototype_handle = prototype_handle + str(random.randrange(1, 1000))             # Generate unique handle based on random generator (security)

    if len(prototype_handle) > 20:                                              # Ensure handle size less than 20 chars
        prototype_handle = prototype_handle[0:20]

def user_channels(auth_user_id):
    store = data_store.get()
    user_list_channel = {
        'channels': [

        ],
    } #this is empty list that we will append to
    for channel in store['channels']: 
        for member in channel['all_members']:
            if member == auth_user_id:
                user_list_channel['channels'].append(channel)
        
    return user_list_channel

# def function to return list of channels that user is part of  including priv channels

def user_all_channels(auth_user_id):
    store = data_store.get()    

    user_list_channel = { 'channels': store['channels'] }
         
    return user_list_channel

# def functions to help with Channel create, channels list and channels list all 

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

# Function Checks - Yuchao
def handle_check(handle_str):                                                   # Function to check handle uniqueness
    data = data_store.get()
    for user in data['users']:
        if user['handle_str'] == handle_str:
            return True
    return False

def auth_user_id_check(auth_user_id):
    data = data_store.get()
    for user in data['users']:
        if int(user['auth_user_id']) == int(auth_user_id):
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
#####################
def check_if_user_is_channel_member(auth_user_id, channel_id):
    store = data_store.get()
    user = auth_user_id_check(auth_user_id) 
    value = False 
    for Dict in store['channels']:
        if int(Dict['channel_id']) == int(channel_id):
            for member in Dict['all_members']:
               #if member["auth_user_id"] == user["auth_user_id"]:
                if member == user['auth_user_id']:
                    value = True 
    return value




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

