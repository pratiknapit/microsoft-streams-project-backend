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
    'user': [    
    ]
}

def add_user(email, password, name_first, name_last):
    
    store = data_store.get()                                                    # gets user data from initial_object
    auth_user_id = len(name_first) +len(name_last) +len(email) + random.randrange(1, 1000)
    user = make_user(email, password, name_first, name_last, auth_user_id)   
    store['user'].append(user)
    return user

def make_user(email, password, name_first, name_last, auth_user_id):                    # Remember to Add more fields

    return {
            'auth_user_id': auth_user_id,
            'email': email,  
            'password': password, 
            'name_first': name_first,
            'name_last': name_last, 
            'handle': create_handle(name_first, name_last),
    }

def create_handle(first_name, last_name):
    
    prototype_handle = first_name + last_name                                   # Concatenation of first and last name
    prototype_handle = prototype_handle.lower()                                 # lowercased string

    if handle_check(prototype_handle):                                          # If same handle
        prototype_handle = prototype_handle + str(random.randrange(1, 1000))             # Generate unique handle based on random generator (security)

    if len(prototype_handle) > 20:                                              # Ensure handle size less than 20 chars
        prototype_handle = prototype_handle[0:20]

    return prototype_handle

def handle_check(handle):                                                   # Function to check handle uniqueness
    data = data_store.get()
    for user in data['user']:
        if user['handle'] == handle:
            return True
    return False

def auth_user_id_check(auth_user_id):
    data = data_store.get()
    for user in data['user']:
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
    for user in data['user']:
        if user['email'] == email:
            return True
    return False

def login_email(email):
    data = data_store.get()
    for user in data['user']:
        if user['email'] == email:
            return user
    return False

def password_check(password):
    data = data_store.get()
    for user in data['user']:
        if user['password'] == password:
            return user
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

