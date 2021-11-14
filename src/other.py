from src.data_store import data_store
from src.data_store import auth_user_id_check, token_to_user_id, is_valid_token
from src.error import InputError, AccessError

def clear_v1():
    store = data_store.get()
    store['users'] = []
    store['channels'] = []
    store['Messages'] = []
    store['dms'] = []
    data_store.set(store)

def notifications_get(token):

    if not is_valid_token(token):
        raise AccessError(description="Not an authorised user invalid")

    user_id = token_to_user_id(token)
    user = auth_user_id_check(user_id)
    
    return {'notifications': user['notifications'][:20]}

def search_v2(token, query_str):
    '''
    Given a query string, return a collection of messages in all of the channels/DMs that the user has joined that contain the query.
    Arguments:
        token     (str)    - an authorisation hash of the user who is adding the ownership of the user with u_id
        query_str (str)    - query string for collection of messages
        ...
    Exceptions:
        InputError  - query string is more than 1000 characters or less than 1 character
        AccessError - token is invalid
    Returns:
        Returns {messages}
    '''
    decoded_token = is_valid_token(token)
    if decoded_token is False:
        raise AccessError('Not authorised to search.')

    if len(query_str) > 1000 or len(query_str) < 1:
        raise InputError('Query string too long.')

    messages = []

    data = data_store.get()

    for channel in data['channels']:
        is_in_channel = False
        for member in channel['all_members']:
            if member == decoded_token['auth_user_id']:
                is_in_channel = True
                break
        if decoded_token['auth_user_id'] in channel['owner_members']:
            is_in_channel = True
        if is_in_channel:
            for channel_message in channel['Messages']:
                if query_str in channel_message['message']:
                    messages.append(channel_message)

    for dm in data['dms']:
        is_in_dm = False
        if decoded_token['auth_user_id'] in dm['members']:
            is_in_dm = True
        if dm['creator'] == decoded_token['auth_user_id']:
            is_in_dm = True
        if is_in_dm:
            for dm_message in dm['messages']:
                if query_str in dm_message['message']:
                    messages.append(dm_message)

    return {
        'messages': messages
    }
