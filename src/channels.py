'''
This file contains channels_list, channels_listall, channels_create.
'''
from src.data_store import token_check, user_channels, add_channel, user_all_channels
from src.error import AccessError, InputError


def channels_list_v1(token):
    """
    <Provide a list of all channels that the authorised user is part of.>

    Arguments:
        <auth_user_id> (Int)    - <Authorised user id.>

    Exceptions:
        AccessError     - Occurs when auth_user_id passed in is not a valid id.

    Return Value:
        Returns dictionary with key 'channels' and required details on
        condition that auth_user_id is member of a channel.
        Returns an empty dictionary on condition that auth_user_id is not a member of any channel.
    """
    if token_check(token) == False:
        raise AccessError(description="token not found")

    return user_channels(token)


def channels_listall_v1(token):
    """
    <Provide a list of all channels, including private channels, (and their associated details).>

    Arguments:
        <auth_user_id> (Int)  - Authorised user id.

    Exceptions:
        AccessError       - Occurs when auth_user_id passed in is not a valid id.

    Return Value:
        Returns dictionary with key 'channels' and required details on
        every channel in the data store.
        Returns an empty dictionary on condition that there are no channels in the data store.
    """
    if token_check(token) == False:
        raise AccessError(description="token not found")

    return user_all_channels(token)


def channels_create_v1(token, name, is_public):
    """
    <Creates a new channel with the given name that is either a public or private channel.>

    Arguments:
        <auth_user_id> (Int)    - Authorised user id.
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

    if len(name) < 1 or len(name) > 20:
        raise InputError
    
    if token_check(token) == False:
        raise AccessError(description="token not found")

    #The function below will add the new channel that is created to the database.
    added_channel = add_channel(token, name, is_public)

    #Our return value is a dictionary with these keys, as per the spec requirements.
    return {
        'channel_id': added_channel['channel_id']
    }