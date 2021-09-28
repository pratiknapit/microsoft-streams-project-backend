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

## YOU SHOULD MODIFY THIS OBJECT BELOW
initial_object = {
    'user': [    
    ]
}

def add_user(email, password, name_first, name_last):
    
    store = data_store.get()                                   # gets user data from initial object
    u_id = len(name_first) +len(name_last) +len(email) + randrange(100000)
    user = make_user(email, password, name_first, name_last, u_id)   # Remember to Add more fields
#    data_store.set(store)
    store['user'].append(user)
    return user

def make_user(email, password, name_first, name_last, u_id):

    return {
            'u_id': u_id,
            'email': email,  
            'password': password, 
            'name_first': name_first,
            'name_last': name_last, 
            'handle_str': create_handle(name_first, name_last),
    }

def create_handle(first_name, last_name):
    
    sample_handle = first_name + last_name                       # Concatenation of first and last name
    sample_handle = sample_handle.lower()                        # lowercased string

    if handle_check(sample_handle):                              # If passes handle_check 
        sample_handle = sample_handle + str(randrange(25000))    # Generate unique handle based on random generator

    if len(sample_handle) > 20:                                  # Ensure handle size less than 20 chars
        sample_handle = sample_handle[0:20]

    return sample_handle

def handle_check(handle_str):                                   # Function to check handle
#    data = get_user_store()
    data = data_store.get()
    for user in data['users']:
        if user['handle_str'] == handle_str:
            return True
    return False

def email_check(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if (re.fullmatch(regex, email)):
        return True
    else:
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

