'''
This file contains auth_login, auth_register
'''

###########
#Functions#
###########
from src.data_store import data_store, add_user, login_email, login_token

##########################
# Helper Check Functions #
##########################
from src.data_store import email_check, email_repeat_check, password_check

###################
# Error Functions #
###################
from src.error import InputError

def auth_register_v1(email, password, name_first, name_last):                     # Add_user
    '''
    <Registers an authorised user given its arguments (email, password, name_first, name_last)>

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
        Returns auth_user_id on condition that the user is valid and passes the check tests
    '''
    if not email_check(email):
        raise InputError
    if email_repeat_check(email) is True:
        raise InputError
    if len(password) < 6:
        raise InputError
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError

    added_user = add_user(email, password, name_first, name_last)
    token = login_token(added_user)                                                     # authorisation hash

    store = data_store.get()
    for user in store['users']:
        if user['u_id'] == user['u_id']:
            user['token'] = token
            
    return {
        'auth_user_id': added_user['u_id'],
        'token': token,
    }

def auth_login_v1(email, password):
    '''
    <Logs in an Authorised user with correct password and email.>

    Arguments:
        <email> (str)       - <A string which holds the email>
        <password> (str)    - <A string of set password>

    Exceptions:
        InputError  - Occurs when the email is not a valid format for an email
        InputError  - Occurs when the email does not belong to the user
        InputError  - Occurs when password is not correctly entered

    Return Value:
        Returns auth_user_id on condition that the user is valid and passes the check tests
    '''
    if not email_check(email):
        raise InputError
    if email_repeat_check(email) is False:
        raise InputError
    if not password_check(password):
        raise InputError

    cur_user = login_email(email)
    token = login_token(cur_user)                                                     # authorisation hash

    store = data_store.get()
    for user in store['users']:
        if user['u_id'] == user['u_id']:
            user['token'] = token
            
    return {
        'auth_user_id': cur_user['u_id'],
        'token': token
    }

def auth_logout(token):
    '''
    <Logs out user based on token>

    Arguments:
        <token> (str)       - <A string which holds the token>

    Exceptions:

    Return Value:
        Returns empty dictionary
    '''
    store = data_store.get() 
    for user in store['users']:
        if user['token'] == token:
            user.pop('token')
            return {}