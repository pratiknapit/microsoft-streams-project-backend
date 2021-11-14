'''
This file contains channels_list, channels_listall, channels_create.
'''
from src.data_store import save_data, token_check, user_channels, add_channel, user_all_channels
from src.error import AccessError, InputError
from src.data_store import data_store, token_to_user_id
from datetime import datetime



def channels_list_v1(token):
    """
    <Provide a list of all channels that the authorised user is part of.>

    Arguments:
        token (str)            - Token of a user after registration from auth_register

    Exceptions:
        AccessError     - Occurs when auth_user_id passed in is not a valid id.

    Return Value:
        Returns dictionary with key 'channels' and required details on
        condition that auth_user_id is member of a channel.
        Returns an empty dictionary on condition that auth_user_id is not a member of any channel.
    """
    data = data_store.get()
    if token_check(token) == False:
        raise AccessError(description="token not found")

    ret = user_channels(token)
    save_data(data)
    
    return ret


def channels_listall_v1(token):
    """
    <Provide a list of all channels, including private channels, (and their associated details).>

    Arguments:
        token (str)            - Token of a user after registration from auth_register

    Exceptions:
        AccessError       - Occurs when auth_user_id passed in is not a valid id.

    Return Value:
        Returns dictionary with key 'channels' and required details on
        every channel in the data store.
        Returns an empty dictionary on condition that there are no channels in the data store.
    """
    data = data_store.get() 
    if token_check(token) == False:
        raise AccessError(description="token not found")

    ret = user_all_channels(token)

    save_data(data)

    return ret


def channels_create_v1(token, name, is_public):
    """
    <Creates a new channel with the given name that is either a public or private channel.>

    Arguments:
        token (str)            - Token of a user after registration from auth_register
        <is_public> (Bool)    - Public or private channel.

    Exceptions:
        AccessError         - Occurs when auth_user_id passed in is not a valid id.
        InputError          - When the name is less than 1 or more than 20 characters.

    Return Value:
        Returns AccessError on if the auth_user_id does not belong to a valid user id.
        Returns InputError on if the name is less than 1 or more than 20 characters.
        Returns Dictionary with 'channel_id' and 'name'  on valid user id and name.
        Returns an empty dictionary on condition that there are no channels in the data store.
    """

    data = data_store.get()

    if len(name) < 1 or len(name) > 20:
        raise InputError
    
    if token_check(token) == False:
        raise AccessError(description="token not found")

    #The function below will add the new channel that is created to the database.
    added_channel = add_channel(token, name, is_public)

    #User stats implementation
    u_id = token_to_user_id(token)
    for user in data['users']:
        if user['u_id'] == u_id:
            channels_joined = len(user['user_stats']['channels_joined']) #Dont need to check prev because channels cannot be deleted
            user['user_stats']['channels_joined'].append({
                'num_channels_joined': channels_joined, 
                'time_stamp':int(datetime.now().timestamp())
            })
    
    if len(data['workspace_stats']['channels_exist']) == 1:
        channel_exist = 1
    else:
        channel_exist = data['workspace_stats']['channels_exist'][-1]['num_channels_exist'] + 1
    
    data['workspace_stats']['channels_exist'].append({
        'num_channels_exist': channel_exist,
        'time_stamp':int(datetime.now().timestamp())
    })

    save_data(data)


    #Our return value is a dictionary with these keys, as per the spec requirements.
    return {
        'channel_id': added_channel['channel_id']
    }