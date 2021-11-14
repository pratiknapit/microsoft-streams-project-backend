'''
This file contains auth_login, auth_register
'''
###########
#Functions#
###########
from src.data_store import data_store, add_user, login_email, create_token, hash_password

##########################
# Helper Check Functions #
##########################
from src.data_store import email_check, email_repeat_check, password_check, is_valid_token, token_to_user_id, save_data
from src.helper import token_logout, generate_reset_code, change_password
###################
# Error Functions #
###################
from src.error import InputError
import random
import string
import uuid
import json

class uuidencode(json.JSONEncoder):
    def default(self, uuid_id):
        if isinstance(uuid_id, uuid.UUID):
            return str(uuid_id)
        return json.JSONEncoder.default(self, uuid_id)


def create_session(user):
    unique_id = uuid.uuid4()
    unique_id_json = json.dumps(unique_id, cls=uuidencode)
    user['session_list'].append(unique_id_json)
    return unique_id_json

def auth_register_v1(email, password, name_first, name_last):                     # Add_user
    '''
    Registers an authorised user given its arguments (email, password, name_first, name_last)

    Arguments:
        <email> (str) - <A string which holds the email>
        <password> (str) - <A string of set password>
        <name_first> (str) - <A string of the first name of the user>
        <name_last> (str) - <A string of the last name of the user>

    Exceptions:
        InputError  - Occurs when the email is not a valid format for an email
        InputError  - Occurs when the email does not belong to the user
        InputError  - Occurs when length of password is less than 6
        InputError  - Occurs when length of name_first is less than 1 or greater than 50
        InputError  - Occurs when length of name_last is less than 1 or greater than 50

    Return Value:
        Returns auth_user_id and token on condition that the user is valid.
    '''

    data = data_store.get()

    if not email_check(email):
        raise InputError('Email Invalid')
    if email_repeat_check(email) is True:
        raise InputError('Email already exists')
    if len(password) < 6:
        raise InputError('Password too short')
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError('Invalid Length')
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError('Invalid Length')

    added_user = add_user(email, password, name_first, name_last)
    session_id = create_session(added_user)
    token = create_token(added_user, session_id)                                                     # authorisation hash
    
    store = data_store.get()
    for user in store['users']:
        if user['u_id'] == added_user['u_id']:
            user['token'] = token

    save_data(data)

    return {
        'auth_user_id': added_user['u_id'],
        'token': token,
    }

def auth_login_v1(email, password):
    '''
    Logs in an Authorised user with correct password and email

    Arguments:
        <email> (str)       - <A string which holds the email>
        <password> (str)    - <A string of set password>

    Exceptions:
        InputError  - Occurs when the email is not a valid format for an email
        InputError  - Occurs when the email does not belong to the user
        InputError  - Occurs when password is not correctly entered

    Return Value:
        Returns auth_user_id and token on condition that the user is valid
    '''

    data = data_store.get()

    if not email_check(email):
        raise InputError('Email invalid')
    if email_repeat_check(email) is False:
        raise InputError
    if not password_check(password):
        raise InputError('Incorrect Password Entered')

    cur_user = login_email(email)

    store = data_store.get()
    for user in store['users']:
        hashed_password = hash_password(password)
        if user['u_id'] == cur_user['u_id'] and user['password'] == hashed_password:
                session_id = create_session(user)
                save_data(store)                                                        # Everytime made something
                token = create_token(cur_user, session_id) 
                user['token'] = token

    save_data(data)
            
    return {
        'auth_user_id': cur_user['u_id'],
        'token': token
    }

def auth_logout(token):
    '''
    Logs out user based on token

    Arguments:
        <token> (str)       - <A string which holds the token>

    Exceptions: None

    Return Value:
        Returns empty dictionary and boolean success statement
    '''
    store = data_store.get() 
    is_loggedout = token_logout(token)

    save_data(store)
    return is_loggedout
def auth_passwordreset_request(email):
    '''
    Given authorised email returns a reset code to change password

    Arguments:
        <email> (str)       - <A string which holds the email of user>

    Exceptions: Input error raised for emails only for sanity check

    Return Value:
        Returns reset code
    '''
    data = data_store.get()
    if not email_repeat_check(email):
        raise InputError('Invalid Email')

    reset_code = generate_reset_code(email)
    
    save_data(data)
    return reset_code

def auth_passwordreset_reset(reset_code, new_password):
    '''
    Given a reset code for a user, set that user's new password to the password provided.

    Arguments:
        <reset_code>    (str)           - Unique codes used to authorise password change
        <new_password>  (new_password)  - New password to replace old password.

    Exceptions: Input error raised for invalid reset codes
                Input error raised for length of password less than 6 characters

    Return Value:
        None
    '''
    data = data_store.get()
    if len(new_password) < 6:
        raise InputError("Invalid password length")

    is_found = change_password(reset_code, new_password)
    save_data(data)

    if is_found == False:
        raise InputError("Invalid reset_code")
    return {}