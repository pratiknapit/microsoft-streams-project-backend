import re

from src.data_store import data_store
from src.error import InputError


#def get_user_store():
 #   global data_store.get()
 #   return data_store.get()


regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def auth_login_v1(email, password):
    return {
        'auth_user_id': 1,
    }



def auth_register_v1(email, password, name_first, name_last):                     # Add_user

 #   store = get_user_store()
 #   store = data_store.get()
 #   user = make_user(email, password, name_first, name_last)
 #   store['users'].append(user)
 #   return user
    store = data_store.get()
    store['email'] = email
    store['password'] = password
    store['name_first'] = name_first
    store['name_last'] = name_last
    return user

def make_user(email, password, name_first, name_last):

    return {
            'email': email,  
            'password': password, 
            'name_first': name_first,
            'name_last': name_last, 
            'handle_str': create_handle(name_first, name_last),
    }

def create_handle(first_name, last_name):
    
    sample_handle = first_name + last_name                       # Concatenation of first and last name
    sample_handle = sample_handle.lower()

    if handle_check(sample_handle):                              # If passes handle_check 
        sample_handle = sample_handle + str(randrange(25000))    # Generate unique handle based on random generator

    if len(sample_handle) > 20:                                  # Ensure handle size less than 20 chars
        sample_handle = sample_handle[0:20]

    return sample_handle



 #   return {
 #       'auth_user_id': 1,
 #   }

def test_check(email):
		if (re.fullmatch(regex, email)) == None:            # If email is invalid



def handle_check(handle_str):                                   # Function to check handle
#    data = get_user_store()
    data = data_store.get()
    for user in data['users']:
        if user['handle_str'] == handle_str:
            return True
    return False