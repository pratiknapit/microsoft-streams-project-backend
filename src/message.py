
from src.data_store import data_store, make_message
from src.data_store import token_check, channel_id_check, message_id_check, dm_id_check, is_valid_token, check_if_user_is_channel_member, token_to_user_id, auth_user_id_check 
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

    auth_user_id = token_to_user_id(token)
    user = auth_user_id_check(auth_user_id) 
    if check_if_user_is_channel_member(token, channel_id) == True:
        # if message_id_check(message) is False:
        #   raise AccessError
        message_id = make_message(message, channel_id, user['u_id'])

    return {
        'message_id': message_id,
    }
    
def message_edit(token, message_id, message):
    """Edits a current message  
    Parameters:
        token (string)
        message_id(int)
        edit_message(string)
    
    """
    '''
    if message_id_check(message_id) is None:
        raise InputError
    

    is_owner = owner_channel_check(token, edit_message['channel_id'])

    is_sender = False

    if user['u_id'] == edit_message['u_id']:
        is_sender = True

    if (is_owner or is_sender) == False:
        raise AccessError

    edit_message['message'] = edit_message
    '''
###
    if len(message) > 1000:
        raise InputError(description='Message over 1000 characters.')

    decoded_token = is_valid_token(token)
    if decoded_token is False:
        raise AccessError(description='Invalid Token.')

    data = data_store.get()

  #  token_user = find_user(decoded_token['user_id'], data)

    source = None
    found_message = None
    for dm in data['dms']:
        for dm_message in dm['messages']:
            if dm_message['message_id'] == message_id:
                if dm['creator'] == decoded_token['user_id'] or dm_message['u_id'] == decoded_token['user_id']:
                    found_message = dm_message
                    source = dm
                    break
                else:
                    raise AccessError(
                        description='Not authorised to edit message.')
        if found_message is not None:
            break

    if found_message is None:
        for channel in data['channels']:
            for channel_message in channel['messages']:
                if channel_message['message_id'] == message_id:
                    if decoded_token['user_id'] in channel['owner'] or channel_message['u_id'] == decoded_token['user_id']:
                        found_message = channel_message
                        source = channel
                        break
                    else:
                        raise AccessError(
                            description='Not authorised to edit message.')
            if found_message is not None:
                break

    if found_message is not None:
        if len(message) == 0:
            source['messages'].remove(found_message)
        else:
            found_message['message'] = message
    else:
        raise InputError(description='No message found.')

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

    
#def message_senddm(token, dm_id, message):


def owner_channel_check(token, channel_id):
    user = token_check(token)   #checks if it's a valid user
    if user == False:
        raise InputError
    channel = channel_id_check(channel_id)
    if channel == None:
        raise InputError

    for member in channel['owner_members']:     
        if int(member['u_id']) == int(user['u_id']):
            return True
    return False