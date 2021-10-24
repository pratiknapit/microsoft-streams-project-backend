'''
This file contains dm_create, dm_details, dm_leave, dm_list, dm_remove, dm_messages
'''
from src.error import AccessError, InputError
from src.data_store import dm_id_check, is_user_in_channel, is_user_in_dm, is_valid_token, is_valid_user_id, is_user_in_dm
from src.data_store import find_user, find_dm, find_channel, is_valid_dm_id, is_user_in_channel
from src.data_store import data_store

def dm_create(token, u_ids):
    '''
    Creates dms given users and token

    Arguments:
        token (str)       - an authorisation hash of the user
        u_ids (int [])    - user ids of the users that this DM is directed to (excluding the creator)
    Exceptions:
        AccessError  - Occurs when the token invalid
        InputError   - Occurs when u_id does not refer to a valid user
    Return Value:
        A dictionary containing dm_id
    '''
    
    store = data_store.get()
    dms = store['dms']
    dm_id = len(dms) + 1

    if not is_valid_token(token):
        raise AccessError("Token is invalid.")

    user_id = is_valid_token(token)['auth_user_id']
    handles = []

    for u_id in u_ids:
        if not is_valid_user_id(u_id):
            raise InputError(f"u_id: {u_id} is not a valid user.")

        user_handle = find_user(u_id)['handle_str']
        handles.append(user_handle)

    handles.append(find_user(user_id)['handle_str'])
    dm_name = ','.join(sorted(handles))

    dm_dict = {
        'creator': user_id,
        'dm_id': dm_id,
        'name': dm_name,
        'members': [user_id] + u_ids,
        'messages': []
    }

    dms.append(dm_dict)

    return {'dm_id': dm_id}

def dm_list(token):
    '''
    Returns the list of DMs that the user is a member of

    Arguments:
        token (str) - an authorisation hash of the user
    Exceptions:
        AccessError - When the token is invalid
    Returns:
        A list of dms the user is a member of
    '''

    decoded_token = is_valid_token(token)
    if decoded_token == False:
        raise AccessError("Invalid Token.")

    data = data_store.get()
    dm_list = []

    for dm in data['dms']:
        for member in dm['members']:
            if member == decoded_token['auth_user_id']:
                dm_list.append({'dm_id': dm['dm_id'],
                                'name': dm['name']})
                break

    return {'dms': dm_list}

def dm_remove(token, dm_id):
    '''
    Function to delete a dm
    Arguments:
        token (string)       - an authorisation hash of the user
        dm_id (int)          - dm id of the dm the user is deleting
    Exceptions:
        AccessError  - Occurs when the token invalid or when the user is not the dm creator
        InputError   - Occurs when dm_id does not refer to a valid dm
    Return Value:
        Empty dictionary
    '''
    data = data_store.get()

    if dm_id_check(dm_id) == False:
        raise InputError("Invalid dm_id")
    
    decoded_token = is_valid_token(token)
    if decoded_token == False:
        raise AccessError("Invalid token.")

    auth_user_id = decoded_token['auth_user_id']
    if is_valid_user_id(auth_user_id) == False:
        raise AccessError(
            description=f"Auth_user_id: {auth_user_id} is invalid")

    found_dm = False
    for dm in data['dms']:
        if dm['dm_id'] == dm_id:
            found_dm = True
            if dm['creator'] != auth_user_id:
                raise AccessError(description=f"user is not dm creator")
            del dm
            break

    if found_dm == False:
        raise InputError(description=f"Dm id was invalid")

    return {}
    

def dm_details(token, dm_id):
    '''
    Given a valid token from a user that is part of the given dm, returns the details of the given dm
    Arguments:
        token (string): an authorisation hash of the user
        dm_id (int): id of the given dm
    Exceptions:
        AccessError: When the token is invalid
        InputError: When dm_id is not a valid dm
        AccessError: raises if the authorised user is not a part of the dm

    Return Value:
        String of the name of the dm, 
        list of dicts with u_id, email, name_first, name_last and handle_str
    '''
    if is_valid_token(token) == False:
        raise AccessError("Invalid token")
    decoded_token = is_valid_token(token)

    data = data_store.get()
    
    try:
        dm_id = int(dm_id)
    except Exception as e:
        raise InputError(description='dm_id must be an integer') from e
    

    dm = next((dm for dm in data['dms'] if dm['dm_id'] == dm_id), False)

    if not dm:
        raise InputError("dm_id is invalid")
    
    if dm['members'].count(decoded_token['auth_user_id']) == 0:
        raise AccessError("User is not in this DM")

    return_dict = {'name': dm['name'], 'members': []}
    for member_id in dm['members']:
        user = next(user for user in data['users']
                    if user['u_id'] == member_id)
        return_dict['members'].append({'u_id': user['u_id'],
                                       'email': user['email'],
                                       'name_first': user['name_first'],
                                       'name_last': user['name_last'],
                                       'handle_str': user['handle_str'],
                                       })
    return return_dict

def dm_leave(token, dm_id):
    '''
    Given a DM ID, the user is removed as a member of this DM
    Arguments:
        token (string)      - an authorisation hash of the user
        dm_id (int)         - dm_id of the dm the user is part of
    Exceptions:
        AccessError - Occurs when the token is invalid and authorised user is not a member of the dm
        InputError  - Occurs when dm_id is invalid
    Return Value:
        Empty dictionary
    '''
    decoded_token = is_valid_token(token)
    if decoded_token == False:
        raise AccessError("Invalid Token.")

    data = data_store.get()

    dm_id_found = False
    user_in_dm = False

    for dm in data['dms']:
        if dm['dm_id'] == dm_id:
            dm_id_found = True
            for member in dm['members']:
                if member == decoded_token['auth_user_id']:
                    user_in_dm = True
            break

    if dm_id_found is False:
        raise InputError('Valid DM not found.')

    if user_in_dm is False:
        raise AccessError('User is not a member of this DM.')

    for dm in data['dms']:
        if dm['dm_id'] == dm_id:
            dm['members'].remove(decoded_token['auth_user_id'])
    
    data_store.set(data)
    return {}

def dm_messages(token, dm_id, start):
    '''
    Function to return up to 50 messages between "start" and "start + 50"
    Arguments:
        token (str)         - an authorisation hash of the user
        dm_id (int)         - dm_id of the dm the user is part of
        start (int)         - show messages starting from start; start = 0 means the most recent message
    Exceptions:
        AccessError - Occurs when the token is invalid and authorised user is not a member of the dm
        InputError  - Occurs when dm_id is invalid and "start" is greater than
        the total number of messages in the dm
    Return Value:
        Returns {messages, start, end} where messages is a dictionary
    '''
    data = data_store.get()
    try:
        dm_id = int(dm_id)
    except Exception as e: 
        raise InputError(description='dm_id must be an integer') from e
    try:
        start = int(start)
    except Exception as e:
        raise InputError(description='start must be an integer') from e
    

    if is_valid_token(token) == False:
        raise AccessError(description="Token is invalid")

    decoded_token = is_valid_token(token)

    if not is_valid_dm_id(dm_id):
        raise InputError(description="DM ID is invalid.")

    dm_info = find_dm(dm_id, data)
    dm_messages = dm_info['messages']

    if not is_user_in_dm(dm_id, decoded_token['auth_user_id']):
        raise AccessError(
            description=f"User is not a member of the dm with dm id {dm_id}")

    # Check valid start number
    if start >= len(dm_messages) and start != 0:
        raise InputError(
            description="Start is greater than the total number of messages in the dm.")

    # calculate the ending return value
    end = start + 50 if (start + 50 < len(data['dms']) - 1) else -1
    messages_dict = {'messages': [],
                     'start': start,
                     'end': end
                     }

    if end == -1:
        for i in range(start, len(dm_messages)):
            messages_dict['messages'].append(dm_messages[i])
    else:
        for i in range(start, end):
            messages_dict['messages'].append(dm_messages[i])

    return messages_dict