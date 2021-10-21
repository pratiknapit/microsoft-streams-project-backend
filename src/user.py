from src.data_store import data_store, user_id_check, token_check
from src.error import InputError, AccessError
from src.data_store import handle_check, email_check, email_repeat_check, is_valid_token
import json
from src.data_store import save_data



def users_all_v1(token):
    if is_valid_token(token) == False:
        raise AccessError("Token not valid")
    
    user_list = []
    data = data_store.get()
    for user in range(len(data['users'])):
        user = {
            'u_id': data['user_list'][user]['u_id'],
            'email': data['user_list'][user]['email'],
            'name_first': data['user_list'][user]['name_first'],
            'name_last': data['user_list'][user]['name_last'],
            'handle_str': data['user_list'][user]['handle'],
        }
        user_list.append(user)

    return{"user_list": user_list}

def user_profile_v1(token, u_id):

    if not token_check(token):
            raise AccessError ("Token provided is not valid")

    if not user_id_check(u_id):
            raise AccessError("Incorrect user id")

    data = data_store.get()
    for user in data['users']:
        if u_id == user['auth_user_id']:
            return {
                'user': {
                    'u_id': user['auth_user_id'],
                    'email': user['email'],
                    'name_first' : user['name_first'], 
	                'name_last' : user['name_last'], 
                    'handle_str' : user['handle_str']
                },
            }
    


def user_profile_setname_v1(token, name_first, name_last):

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
    if token_check(token) == False:
        raise AccessError("Token provided is not valid")

    if not email_check(email):
            raise InputError("Email is incorrect")

    if email_repeat_check(email) == True:
            raise InputError("Email is already taken")

    # Also validates the token, raises AccessError when token is invalid
    # Change the name associated with the user
    id = is_valid_token(token) 
    data = data_store.get()
    for user in data['users']:
        if user['auth_user_id'] == id:
            user['email'] = email
    
    save_data(data)
    return {}


def user_profile_sethandle_v1(token, handle_str):

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


