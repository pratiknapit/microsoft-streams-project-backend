from src.data_store import auth_user_id_check, data_store, message_id_check, token_to_user_id, user_id_check, token_check
from src.error import InputError, AccessError
from src.data_store import handle_check, email_check, email_repeat_check, is_valid_token, token_to_user_id
import json
from src.data_store import save_data
from datetime import datetime
from src.auth import auth_register_v1 
from src.channels import channels_create_v1, channels_list_v1
from src.other import clear_v1
import time
from src.dm import dm_create, dm_remove
from src.message import message_remove, message_send, message_senddm
import os
import time
import requests
import urllib.request
# from PIL import Image
import io
import sys




def users_all_v1(token):

    '''
    When given a valid token, it returns a list of dictionaries of each user's details. 
    Each user's details is a dictionary and there is a list of them. Hence a list of dictionaries.

    Arguments:
        token (str)     - A jwt encoded dictionary with u_id key

    Exceptions:
        AccessError     - Occurs when the token is invalid

    Return Value:
        Returns {users}, a list of dictionaries of each user's details 
        (user id, email, first name, last name and handle)
    '''
    # token check (AccessError if invalid token)
    if is_valid_token(token) == False:
        raise AccessError("Token not valid")

    user_list = []
    data = data_store.get()
    for user in data['users']:
        if user['is_removed'] != True:
            user = {
                'u_id': user['u_id'],
                'email': user['email'],
                'name_first': user['name_first'],
                'name_last': user['name_last'],
                'handle_str': user['handle_str'],
            }
            user_list.append(user)
            #user = {}  

    return{"users": user_list}

def user_profile_v1(token, u_id):

    '''
    When given a valid u_id and valid token of the selected user,
    it returns a profile (the user details) of that user.

    Arguments:
        token (str)     - A jwt encoded dictionary with u_id key
        u_id (int)      - The user id of the selected user's details which is to be returned

    Exceptions:
        AccessError   - Occurs when the token is invalid
        InputError    - Entered user id is incorrect

    Return Value:
        Returns {user}, a dictionary of the selected user's details 
        (user id, email, first name, last name and handle)
    '''
    # Token check (AccessError if invalid token)
    if not is_valid_token(token):
            raise AccessError ("Token provided is not valid")

    # u_id check (InputError if invalid/incorrect u_id)
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
                    'handle_str' : user['handle_str'],
                    'profile_img_url': user['profile_img_url']
                    
                },
            }
    
def user_profile_setname_v1(token, name_first, name_last):

    '''
    When provided with a valid token, the user can change their current first and last name to newer ones. 
    This is on the condition that they are valid names.

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

    # Token check (AccessError if invalid token)
    if not is_valid_token(token):
            raise AccessError("Token provided is not valid")

    # If first name isnt in correct range of length, it raises an InputError
    if (len(name_first) < 1 or len(name_first) > 50):
        raise InputError(
            "First name has to be between 1 and 50 characters inclusively")

    # If last name isnt in correct range of length, it raises an InputError
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
    When provided with a valid token, the user can change their current email to a newer one. 
    This is on the condition that the email is valid and not already taken by another user.

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

    # Token check (AccessError if invalid token)
    if is_valid_token(token) == False:
        raise AccessError("Token provided is not valid")

    # Raises an InputError if the new given email is not in a valid format
    if not email_check(email):
            raise InputError("Email is invalid")

    # Raises an InputError if the new given email is already taken by someone else
    if email_repeat_check(email) == True:
            raise InputError("Email is already taken")

    id = is_valid_token(token) 
    data = data_store.get()
    for user in data['users']:
        if user['u_id'] == id:
            user['email'] = email
    
    save_data(data)
    return {}

def user_profile_sethandle_v1(token, handle_str):

    '''
    When provided with a valid token, the user can change their current handle_str to a newer one. 
    This is on the condition that the handle_str is valid and not already taken by another user.

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

    # Token check (AccessError if invalid token)
    if is_valid_token(token) == False:
        raise AccessError("Token provided is not valid")
    
    # If handle string is not in correct range of length (between 3 and 20 characters inclusively)
    if (len(handle_str) < 3 or len(handle_str) > 20):
        raise InputError("Invalid handle_str")

    # If handle string is already taken by another user, it raises an InputError
    if handle_check(handle_str) == True:
        raise InputError("Handle_str is already taken")
    
    data = data_store.get()
    for user in data['users']:
        if user['u_id'] == id:
            user['handle_str'] = handle_str

    save_data(data)        
    return {}


def user_stat(token): 
    '''
    When provided a valid token, it returns all of the selected user's statistics for their usage of UNSW Streams.

    Each of the stats are time-series data types for:
        - The number of channels which the selected user is a part of
        - The number of DMs which the selected user is a part of
        - The number of messages which the selected user has sent

    Arguments:
        token (str)   - A jwt encoded dictionary with u_id key

    Exceptions:
        AccessError     - Occurs when the token is invalid

    Return Value:
        Returns {user_stats}, on the condition that everything is correct. Where user_stats is a dictionary which contains 
        {
            channels_joined: [{num_channels_joined, time_stamp}],
            dms_joined: [{num_dms_joined, time_stamp}], 
            messages_sent: [{num_messages_sent, time_stamp}], 
            involvement_rate 
        }
    '''

    data = data_store.get()

    if not is_valid_token(token):
        raise AccessError("Token Invalid")

    user_id = token_to_user_id(token)

    user = auth_user_id_check(user_id)

    user_data = user['user_stats']
    involvement_rate_nom = len(user_data['channels_joined']) + len(user_data['dms_joined']) 
    + len(user_data['messages_sent'])

    streams_data = data['workspace_stats']

    involvement_rate_dem = len(streams_data['channels_exist']) + len(streams_data['dms_exist'])
    + len(streams_data['messages_exist'])

    involvement = involvement_rate_nom / involvement_rate_dem

    save_data(data)
    
    return {
        'user_stats': {
                'channels_joined': user_data['channels_joined'],
                'dms_joined': user_data['dms_joined'],
                'messages_sent': user_data['messages_sent'],
                'involvement_rate': involvement,
            }
    }

    
def users_stat():
    '''
    When provided a valid token, it returns all the statistics for all users' usage on the UNSW Streams platform.

    Each of the stats are time-series data types for:
        - The number of channels which currently exist
        - The number of DMs which currently exist
        - The number of messages which currently exist

    Arguments:
        token (str)   - A jwt encoded dictionary with u_id key

    Exceptions:
        AccessError     - Occurs when the token is invalid

    Return Value:
        Returns {workspace_stats}, on the condition that everything is correct. Where workspace_stats is a dictionary which contains 
        {
            channels_exist: [{num_channels_exist, time_stamp}], 
            dms_exist: [{num_dms_exist, time_stamp}], 
            messages_exist: [{num_messages_exist, time_stamp}], 
            utilization_rate 
        }
    '''

    data = data_store.get() 

    workspace = data['workspace_stats']

    count = 0
    for user in data['users']:
        if len(user['user_stats']['channels_joined']) > 1 or len(user['user_stats']['dms_joined']) > 1:
            count += 1
    
    total_users = len(data['users'])

    utilization = count/total_users

    return {
        'workspace_stats': {
            'channels_exist': workspace['channels_exist'],
            'dms_exist': workspace['dms_exist'],
            'messages_exist': workspace['messages_exist'],
            'utilization_rate': utilization    
        }
    }

"""
def user_profile_uploadphoto_v1(token, img_url, x_start, y_start, x_end, y_end):

    '''
    When provided a valid token, it uploads a photo for the user's profile.

    Arguments:
        token (str)   - A jwt encoded dictionary with u_id key 
        img_url (str) - the url of the image from the internet which the user wishes to upload
        x_start (int)    - the start x coordinate of the image to be cropped
        y_start (int)    - the start y coordinate of the image to be cropped
        x_end (int)      - the end x coordinate of the image to be cropped
        y_end (int)      - the end y coordinate of the image to be cropped

    Exceptions:
        AccessError     - Occurs when the token is invalid
        InputError       - img_url returns an HTTP status other than 200
        InputError       - any of x_start, y_start, x_end, y_end are not 
                           within the dimensions of the image at the URL
        InputError       - Image uploaded is not a JPG

    Return Value:
        Returns {}, an empty dictionary on the condition that everything is correct
    '''
    if is_valid_token(token) == False:
        raise AccessError("Token provided is not valid")

    id = token_to_user_id(token)

    path = 'src/static/'
    if not os.path.exists(path):
        os.mkdir(path)

    path = path + str(id) + '.jpg'

    try:
        urllib.request.urlretrieve(img_url, path)
    except Exception as ex:
        raise InputError("Invalid URL") from ex
    try:
        imageObject = Image.open(path)
    except Exception as ex:
        raise InputError("Invalid URL") from ex
    

    width, height = imageObject.size
    if (x_start < 0) or (x_end > width) or (y_start < 0) or (y_end > height):
        raise InputError("Cropping is outside image dimensions")
    if (x_start > x_end) or (y_start > y_end):
        raise InputError("Cropping is outside image dimensions")


    # crop the image
    # give the file a unique name for the user using their auth_user_id 
    # and save the image save the image

    imageObject = Image.open(path)
    cropped = imageObject.crop((x_start, y_start, x_end, y_end))
    cropped.save(path)


    # update the user data
    data = data_store.get()
    for user in data['users']:
        if id == user['u_id']:
            user['profile_img_url'] = 'http://127.0.0.1:8237/static/' + str(id) + '.jpg'
            break
    save_data(data)
    
    return {}
"""




