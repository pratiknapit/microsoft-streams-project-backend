
from src.data_store import data_store, make_message
from src.data_store import token_check, channel_id_check, message_id_check, dm_id_check, is_valid_token
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
        raise InputError
    if not channel_id_check(channel_id):
        raise InputError
    if (len(message) > 1000 or len(message) < 1): 
        raise InputError
    if not member_channel_check(token, channel_id):
        raise AccessError

    store = data_store.get()
    for member in store['all_members']: 
 #       if message_id_check(message) is False:
 #           raise AccessError
        if store['u_id'] == member['u_id']: 
            message_id = make_message(message, channel_id, store['u_id'])
        
    return {
        'message_id': message_id,
    }

def message_edit(token, message_id, edit_message):
    """Edits a current message  
    Parameters:
        token (string)
        message_id(int)
        edit_message(string)
    
    """
    if len(edit_message) > 1000:
        raise InputError
    if message_id_check(message_id) is None:
        raise InputError
    
    user = token_check(token)
    if user is False:
        raise AccessError

    is_owner = owner_channel_check(token, edit_message['channel_id'])

    is_sender = False

    if user['u_id'] == edit_message['u_id']:
        is_sender = True

    if (is_owner or is_sender) == False:
        raise AccessError

    edit_message['message'] = edit_message
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

def member_channel_check(token, channel_id): 
    if token_check(token) is False:
        raise InputError

    if channel_id_check(channel_id) is None:
        raise InputError
    store = data_store.get()
    for member in store['all_members']:
        if int(member['u_id']) == int(store['u_id']):
            return True
    return False

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
