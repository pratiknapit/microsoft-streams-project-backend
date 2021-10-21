'''
from src.error import AccessError, InputError
from src.data_store import (is_valid_token, is_valid_user_id, save_data, find_dm, find_user, invite_notification_message, is_user_in_dm, is_valid_dm_id)
from src.data_store import data_store
from datetime import datetime
'''
def dm_create_v1(token, u_ids):
    '''
    Function to create a channel that is either a public or private with a given name
    Arguments:
        token (string)       - an authorisation hash of the user
        u_ids (int [])       - user id of the users that this DM is directed to (excluding the creator)
    Exceptions:
        AccessError  - Occurs when the token invalid
        InputError   - Occurs when u_id does not refer to a valid user
    Return Value:
        a dictionary {dm_id, dm_name}
    Assumption:
        - a new dm is created everytime a creator creates one even there is already
         a dm with the same creator and dm members
        - a user who is removed from Dreams can not be added to a dm
    '''
    '''
    data = data_store.get()
    dms = data['dms']
    dm_id = len(dms) + 1

    if not is_valid_token(token):
        raise AccessError("Token is invalid.")

    user_id = is_valid_token(token)['u_id']
    handles = []

    for u_id in u_ids:
        if not is_valid_user_id(u_id):
            raise InputError(f"u_id: {u_id} is not a valid user.")

        user_handle = find_user(u_id, data)['account_handle']
        handles.append(user_handle)

    handles.append(find_user(user_id, data)['account_handle'])
    dm_name = ','.join(sorted(handles))

    dm_dict = {
        'creator': user_id,
        'dm_id': dm_id,
        'name': dm_name,
        'members': [user_id] + u_ids,
        'messages': []
    }

    dms.append(dm_dict)
    all_ids = u_ids.copy()
    all_ids.append(user_id)
    # now increase dms joined stat by one for all users in the dm
    for u_id in all_ids:
        user = find_user(u_id, data)
        
        if len(user['user_stats']['dms_joined']) == 0:
            dms_joined = 1
        else:
            dms_joined = user['user_stats']['dms_joined'][-1]['num_dms_joined'] + 1
        user['user_stats']['dms_joined'].append({'num_dms_joined':dms_joined, 'time_stamp':int(datetime.now().timestamp())})
    
    if len(data['dreams_stats']['dms_exist']) == 0:
        dms_exist = 1
    else:
        dms_exist = data['dreams_stats']['dms_exist'][-1]['num_dms_exist'] + 1

    data['dreams_stats']['dms_exist'].append({'num_dms_exist':dms_exist, 'time_stamp':int(datetime.now().timestamp())})
    
    #save_data(data)

    return {'dm_id': dm_id}
    '''


def dm_list_v1(token):
    """Returns the list of DMs that the user is a member of
    Args:
        token (string): jwt encode dict with keys session_id and user_id
    Raises:
        AccessError: raises if the token is invalid
    Returns:
        {dms}: a list of dms the user is a member of
    """
    '''
    decoded_token = is_valid_token(token)
    if decoded_token is False:
        raise AccessError("Invalid Token.")

    data = data_store.get()
    dm_list = []

    for dm in data['dms']:
        for member in dm['members']:
            if member == decoded_token['user_id']:
                dm_list.append({'dm_id': dm['dm_id'],
                                'name': dm['name']})
                break

    return {'dms': dm_list}
    '''


def dm_remove_v1(token, dm_id):
    '''
    Function to delete a dm
    Arguments:
        token (string)       - an authorisation hash of the user
        dm_id (int)          - dm id of the dm the user is deleting
    Exceptions:
        AccessError  - Occurs when the token invalid or when the user is not the dm creator
        InputError   - Occurs when dm_id does not refer to a valid dm
    Return Value:
        {} on successful removal of a dm
    '''
    '''
    data = data_store.get()
    token_data = is_valid_token(token)

    if token_data == False:
        raise AccessError(description=f"Token invalid")

    auth_user_id = token_data['user_id']
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
    
    dms_exist = data['dreams_stats']['dms_exist'][-1]['num_dms_exist'] - 1

    data['dreams_stats']['dms_exist'].append({'num_dms_exist':dms_exist, 'time_stamp':int(datetime.now().timestamp())})
    
    #save_data(data)
    return {}
    '''


def dm_details_v1(token, dm_id):
    '''
    Given a valid token from a user that is part of the given dm, returns the details of the given dm
    Args:
        token (string): jwt encode dict with keys session_id and user_id
        dm_id (int): id of the given dm
    Raises:
        AccessError: raises if the token is invalid
        InputError: if the dm_id is not a valid dm
        AccessError: raises if the authorised user is not a part of the dm
    Returns:
        {name, members}: name is str of the name of the dm, 
        members is a list of dicts with values, u_id, email, name_first, name_last and handle_str
    '''
    '''
    if not is_valid_token(token):
        raise AccessError("Invalid token")
    token = is_valid_token(token)

    data = data_store.get()
    
    try:
        dm_id = int(dm_id)
    except Exception as e:
        raise InputError(description='dm_id must be an integer') from e
    

    dm = next((dm for dm in data['dms'] if dm['dm_id'] == dm_id), False)
    #dm = list(filter(lambda dm: dm['dm_id'] == dm_id, data['dm']))[0]
    if not dm:
        raise InputError("dm_id is invalid")

    if dm['members'].count(token['user_id']) == 0:
        raise AccessError("User is not in this DM")

    return_dict = {'name': dm['name'], 'members': []}
    for member_id in dm['members']:
        user = next(user for user in data['users']
                    if user['user_id'] == member_id)
        return_dict['members'].append({'user_id': user['user_id'],
                                       'email': user['email_address'],
                                       'name_first': user['first_name'],
                                       'name_last': user['last_name'],
                                       'handle_str': user['account_handle'],
                                       })
    return return_dict
    '''


def dm_leave_v1(token, dm_id):
    '''
    Given a DM ID, the user is removed as a member of this DM
    Arguments:
        token (string)      - an authorisation hash of the user
        dm_id (int)         - dm_id of the dm the user is part of
    Exceptions:
        AccessError - Occurs when the token is invalid and authorised user is not a member of the dm
        InputError  - Occurs when dm_id is invalid
    Return Value:
        Returns {}
    '''
    '''
    decoded_token = is_valid_token(token)
    if decoded_token is False:
        raise AccessError("Invalid Token.")

    data = data_store.get()

    dm_id_found = False
    user_in_dm = False

    for dm in data['dms']:
        if dm['dm_id'] == dm_id:
            dm_id_found = True
            for member in dm['members']:
                if member == decoded_token['user_id']:
                    user_in_dm = True
            break

    if dm_id_found is False:
        raise InputError('Valid DM not found.')

    if user_in_dm is False:
        raise AccessError('User is not a member of this DM.')

    for dm in data['dms']:
        if dm['dm_id'] == dm_id:
            dm['members'].remove(decoded_token['user_id'])

    #save_data(data)

    return {}
    '''


def dm_messages_v1(token, dm_id, start):
    '''
    Function to return up to 50 messages between "start" and "start + 50"
    Arguments:
        token (string)      - an authorisation hash of the user
        dm_id (int)         - dm_id of the dm the user is part of
        start (int)         - show messages starting from start; start = 0 means the most recent message
    Exceptions:
        AccessError - Occurs when the token is invalid and authorised user is not a member of the dm
        InputError  - Occurs when dm_id is invalid and "start" is greater than\
        the total number of messages in the dm
    Return Value:
        Returns {messages, start, end} where messages is a dictionary
    '''
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
    

    if not is_valid_token(token):
        raise AccessError(description="Token is invalid")

    user_id = is_valid_token(token)['user_id']

    if not is_valid_dm_id(dm_id):
        raise InputError(description="DM ID is invalid.")

    dm_info = find_dm(dm_id, data)
    dm_messages = dm_info['messages']

    if not is_user_in_dm(dm_id, user_id, data):
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

    save_data(data)
    return messages_dict
    '''