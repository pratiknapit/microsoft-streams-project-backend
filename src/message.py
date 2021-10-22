from src.data_store import data_store, make_message
from src.data_store import token_check, channel_id_check, message_id_check
from src.data_store import dm_id_check, is_valid_token, check_if_user_is_channel_member, token_to_user_id, auth_user_id_check, user_id_check 
from src.error import InputError, AccessError


def message_send(token, channel_id, message):
    """ Sends a message to the designated channel 
    Parameters:
        token (string)
        channel_id(int)
        message(string)
    
    Returns:
        (dictionary): A dictionary containing the message_id
        of the message that was sent.
    """
    
    if not token_check(token):
        raise AccessError
    if not channel_id_check(channel_id):
        raise InputError(description='Channel does not exist')
    if (len(message) > 1000 or len(message) < 1): 
        raise InputError('Message is longer than 1000 characters or less than 1 character')
    if not check_if_user_is_channel_member(token, channel_id):
        raise AccessError

    store = data_store.get()['Messages']
    auth_user_id = token_to_user_id(token)
    user = auth_user_id_check(auth_user_id) 
    if check_if_user_is_channel_member(token, channel_id) == True:
        message_id = make_message(message, channel_id, user['u_id'])

    for i in store:
        if i['message_id'] == message_id:
            user['messages_created'].remove(message)

    '''
        if message_id_check(message_id) == message:
            user['messages_created'].remove(message)
            raise AccessError
    '''
    return {
        'message_id': message_id,
    }
    
def message_edit(token, message_id, new_message):
    """Edits a current message  
    Parameters:
        token (string)
        message_id(int)
        edit_message(string)
    
    """
    if len(new_message) > 1000:
        raise InputError(description='Message over 1000 characters.')
    if message_id_check(message_id) is None:
        raise InputError
    decoded_token = is_valid_token(token)
    if decoded_token is False:
        raise AccessError(description='Invalid Token.')

    
    message = message_id_check(message_id)
    if message == False:
        raise InputError

    is_owner = owner_channel_check(token, message['channel_id'])
    u_id = token_to_user_id(token)
    user = user_id_check(u_id)

    if user == False:
        raise AccessError

    is_sender = False
    if user['u_id'] == message['u_id']:
        is_sender = True

    if (is_owner or is_sender) == False:
        raise AccessError

    auth_user_id = token_to_user_id(token)
    user = auth_user_id_check(auth_user_id) 
    if len(new_message) == 0:
        user['messages_created'].remove(message)

    message['message'] = new_message
    return {}

def message_remove(token, message_id):
    """Removes a message  
    Parameters:
        token (string)
        message_id(int)
    
    """
    message = message_id_check(message_id)
    if message is None:
        raise InputError
    is_owner = owner_channel_check(token, message['channel_id'])

    user = token_check(token)
    if user is False:
        raise AccessError

    is_sender = False

    if user['u_id'] == message['u_id']:
        is_sender = True

    if (is_owner or is_sender) == False:
        raise AccessError

    store = data_store.get()['channels']
    store['Messages'].remove(message)
    return {}

'''    
def message_senddm(token, dm_id, message):

    data = data_store.get()
    token_data = is_valid_token(token)

    if token_data == False:
        raise AccessError(description=f"Token invalid")

    auth_user_id = token_data['user_id']
    auth_user = find_user(auth_user_id, data)

    if len(message) > 1000:
        raise InputError(description=f"message is too long")

    if is_valid_dm_id(dm_id) == False:
        raise InputError(description='dm is invalid')
    dm = find_dm(dm_id, data)

    if is_user_in_dm(dm_id, auth_user_id,  data) == False:
        raise AccessError(
            description='user is not in the dm they are sharing message to')

    message_id = data['msg_counter'] + 1
    new_message = {'message_id': message_id, 'u_id': auth_user_id,
                   'message': message, "time_created": datetime.now().replace(tzinfo=timezone.utc).timestamp(), 'is_pinned': False, 'reactions': []}

    dm['messages'].insert(0, new_message)

    # notify tagged users
    user_message = tag_users(message, auth_user['account_handle'], dm_id, -1)
    if user_message:
        user, message = user_message
        user = next(u for u in data['users'] if u['user_id'] == user)
        user['notifications'].insert(0, message)

    auth_user['sent_messages'].append(message_id)
    
    auth_user['user_stats']['messages_sent'].append({'num_messages_sent':len(auth_user['sent_messages']), 'time_stamp':int(datetime.now().timestamp())})
    
    data['msg_counter'] += 1
    
    if len(data['dreams_stats']['messages_exist']) == 0:
        messages_exist = 1
    else:
        messages_exist = data['dreams_stats']['messages_exist'][-1]['num_messages_exist'] + 1

    data['dreams_stats']['messages_exist'].append({'num_messages_exist':messages_exist, 'time_stamp':int(datetime.now().timestamp())})
    
    save_data(data)

    return {'message_id': message_id}
'''

def owner_channel_check(token, channel_id):
    u_id = token_to_user_id(token)   #checks if it's a valid user
    channel = channel_id_check(channel_id)
    if channel == None:
        raise InputError

    for member in channel['owner_members']:     
        if member == u_id:
            return True
    return False