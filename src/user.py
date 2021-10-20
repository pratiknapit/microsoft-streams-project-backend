from src.data_store import data_store, user_id_check, token_check
from src.error import InputError, AccessError
from src.data_store import handle_search, email_check, is_valid_token



def users_all_v1(token):
    if not is_valid_token(token):
            raise AccessError("Token not valid")
    
    user_list = []
    data = data_store.get()
    for user in data['users']:
        #users.append(user)
        # return custom user data
        myuser = {
            'auth_user_id': user['auth_user_id'],
            'email': user['email'],
            'name_first': user['name_first'],
            'name_last': user['name_last'],
            'handle_str': user['handle_str']
        }

    pass

def users_profile_v1(token, u_id):

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
        if user['auth_user_id'] == id:
            user['name_first'] = name_first
            user['name_last'] = name_last
            break
    return {}

def user_profile_setemail_v1(token, email):
    if not token_check(token):
            raise AccessError("Token provided is not valid")

    if not email_check(email):
            raise InputError("Email is incorrect")

    
    id = is_valid_token(token) # Also validates the token, raises AccessError when token is invalid
    # Change the name associated with the user
    data = data_store.get()
    for user in data['users']:
        if user['auth_user_id'] == id:
            user['email'] = email
            break
    
    # Save the data persistently (the jason stuff)
    # save_data(data)
    return {}


def user_profile_sethandle_v1(token, handle_str):

    if (len(handle_str) < 3 or len(handle_str) > 20):
        raise InputError("Invalid handle_str")

    if handle_search(handle_str) is not None:
        raise InputError("Handle_str is taken")
    
    data = data_store.get()
    for user in data['users']:
        if user['auth_user_id'] == id:
            user['handle_str'] = handle_str
            break
    # Save the data persistently (the jason stuff)
    # save_data(data)

    return {}


