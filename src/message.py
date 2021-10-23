from _pytest.compat import is_async_function
from src.data_store import data_store, make_message
from src.data_store import token_check, channel_id_check, message_id_check, save_data
from src.data_store import dm_id_check, is_valid_token, check_if_user_is_channel_member, token_to_user_id, auth_user_id_check, user_id_check 
from src.error import InputError, AccessError

from src.auth import auth_register_v1
from src.channels import channels_create_v1


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

    channel = channel_id_check(channel_id)
    store = channel['Messages']
    auth_user_id = token_to_user_id(token)
    user = auth_user_id_check(auth_user_id) 
    if check_if_user_is_channel_member(token, channel_id) == True:
        message_id = make_message(message, channel_id, user['u_id'])
        
    for i in store:
        if i['message_id'] == message_id:
            user['messages_created'].remove(message_id)

    return {
        'message_id': message_id,
    }
    
def message_edit(token, message_id, new_message):
    """Edits a current message  
    Parameters:
        token (string)
        message_id(int)
        new_message(string)
    
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

    if len(new_message) == 0:
        user['messages_created'].remove(message_id)
    else :
        message['message'].replace(message['message'], new_message)
    return {}

def message_remove(token, message_id):
    """Removes a message  
    Parameters:
        token (string)
        message_id(int)
    
    """
    data = data_store.get()
    in_channel = False
    in_dm = False
    is_authorised = False

    if is_valid_token(token) == False:
        raise AccessError(description="Not an authorised user invalid")

    user_id = is_valid_token(token)['auth_user_id']

    for channel in data['channels']:
        for message in channel['Messages']:
            if message['message_id'] == message_id:
                in_channel = True
                if message['u_id'] == user_id:
                    is_authorised = True
                if user_id in channel['owner']:
                    is_authorised = True

    if in_channel and not is_authorised:
        raise AccessError(
            description="Not the sender nor an owner of the channel the message was sent in")
    if in_channel and is_authorised:
        for channel in data['channels']:
            for message in channel['Messages']:
                if message['message_id'] == message_id:
                    channel['Messages'].remove(message)
                    save_data(data)
                    return {}

    for dm in data['dms']:
        for message in dm['messages']:
            if message['message_id'] == message_id:
                in_dm = True
                if message['u_id'] == user_id:
                    is_authorised = True

    if in_dm and not is_authorised:
        raise AccessError(description="Not the sender nor an owner of Dreams")
    if in_dm and is_authorised:
        for dm in data['dms']:
            for message in dm['messages']:
                if message['message_id'] == message_id:
                    dm['messages'].remove(message)                    
                    save_data(data)
                    return {}

    if not in_channel and not in_dm:
        raise InputError(description="Message no longer exists.")

def owner_channel_check(token, channel_id):
    u_id = token_to_user_id(token)   #checks if it's a valid user
    channel = channel_id_check(channel_id)
    if channel == None:
        raise InputError

    for member in channel['owner_members']:     
        if member == u_id:
            return True
    return False
