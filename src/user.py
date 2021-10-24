from src.data_store import data_store, user_id_check, token_check
from src.error import InputError, AccessError
from src.data_store import handle_check, email_check, email_repeat_check, is_valid_token
import json
from src.data_store import save_data


def users_all_v1(token):

    '''
    Arguments:
        token (str)     - A jwt encoded dictionary with u_id key

    Exceptions:
        AccessError     - Occurs when the token is invalid

    Return Value:
        Returns {users}, a list of dictionaries of each user's details (user id, email, first name, last name and handle)
    '''

    if is_valid_token(token) == False:
        raise AccessError("Token not valid")

    user_list = []
    data = data_store.get()
    for user in data['users']:
        user = {
            'u_id': user['u_id'],
            'email': user['email'],
            'name_first': user['name_first'],
            'name_last': user['name_last'],
            'handle_str': user['handle_str'],
        }
        user_list.append(user)
        user = {}  
    return{"users": user_list}

def user_profile_v1(token, u_id):

    '''
    Arguments:
        token (str)     - A jwt encoded dictionary with u_id key
        u_id (int)      - The user id of the selected user's details which is to be returned

    Exceptions:
        AccessError   - Occurs when the token is invalid
        InputError    - Entered user id is incorrect

    Return Value:
        Returns {user}, a dictionary of the selected user's details (user id, email, first name, last name and handle)
    '''

    if not token_check(token):
            raise AccessError ("Token provided is not valid")

    if not user_id_check(u_id):
            raise InputError("Incorrect user id")

    data = data_store.get()
    for user in data['users']:
        if u_id == user['u_id']:
            return {
                'user': {
                    'u_id': user['u_id'],
                    'email': user['email'],
                    'name_first' : user['name_first'], 
	                'name_last' : user['name_last'], 
                    'handle_str' : user['handle_str']
                },
            }
    
def user_profile_setname_v1(token, name_first, name_last):

    '''
    Arguments:
        token (str)     - A jwt encoded dictionary with u_id key
        name_first (str)        - The new first name of the user
        name_last (str)     -The new last name of the user

    Exceptions:
        AccessError     - Occurs when the token is invalid
        InputError      - Occurs when the length of name_first is not between 1 and 50 characters inclusively 
        InputError      - Occurs when the length of name_last is not between 1 and 50 characters inclusively 

    Return Value:
        Returns {}, an empty dictionary on the condition that everything is correct
    '''

    if not token_check(token):
            raise AccessError("Token provided is not valid")

    if (len(name_first) < 1 or len(name_first) > 50):
        raise InputError(
            "First name has to be between 1 and 50 characters inclusively")

    if (len(name_last) < 1 or len(name_last) > 50):
        raise InputError(
            "Last name has to be between 1 and 50 characters inclusively")

    data = data_store.get()
    for user in data['users']:
        if user['u_id'] == id:
            user['name_first'] = name_first
            user['name_last'] = name_last
            break

    save_data(data)
    return {}

def user_profile_setemail_v1(token, email):

    '''
    Arguments:
        token (str)     - A jwt encoded dictionary with u_id key
        email (str)     - The new email of the user

    Exceptions:
        AccessError     - Occurs when the token is invalid
        InputError      - New email being entered is an invalid email
        InputError      - New email being entered is already taken by a different user

    Return Value:
        Returns {}, an empty dictionary on the condition that everything is correct 
    '''

    if token_check(token) == False:
        raise AccessError("Token provided is not valid")

    if not email_check(email):
            raise InputError("Email is invalid")

    if email_repeat_check(email) == True:
            raise InputError("Email is already taken")

    # Also validates the token, raises AccessError when token is invalid
    # Change the name associated with the user
    id = is_valid_token(token) 
    data = data_store.get()
    for user in data['users']:
        if user['u_id'] == id:
            user['email'] = email
    
    save_data(data)
    return {}

def user_profile_sethandle_v1(token, handle_str):

    '''
    Arguments:
        token (str)     - A jwt encoded dictionary with u_id key
        handle_str (str)        - The new handle of the user

    Exceptions:
        AccessError     - Occurs when the token is invalid
        InputError      - New handle_str entered is an invalid handle
        InputError      - New handle_str enetered is already being used by another user


    Return Value:
        Returns {}, an empty dictionary on the condition that everything is correct
    '''

    if token_check(token) == False:
        raise AccessError("Token provided is not valid")
    
    if (len(handle_str) < 3 or len(handle_str) > 20):
        raise InputError("Invalid handle_str")

    if handle_check(handle_str) == True:
        raise InputError("Handle_str is already taken")
    
    data = data_store.get()
    for user in data['users']:
        if user['u_id'] == id:
            user['handle_str'] = handle_str

    save_data(data)        
    return {}
