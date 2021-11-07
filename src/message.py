'''
This file contains message_send, message_edit, message_remove
'''
from src.data_store import data_store, make_message
from src.data_store import token_check, channel_id_check, message_id_check, save_data
from src.data_store import is_valid_token, check_if_user_is_channel_member, token_to_user_id
from src.data_store import auth_user_id_check, user_id_check, owner_channel_check, find_dm, is_valid_dm_id
from src.error import InputError, AccessError

def message_send(token, channel_id, message):
    ''' 
    Sends a message to the designated channel 

    Arguments:
        token      (str) - A string which holds the token
        channel_id (int) - The channel id of channel we need details from.
        message    (str) - The message string to send

    Exceptions:
        InputError      - Occurs when the inputted channel_id is not valid.
        InputError      - When message is longer than 1000 characters or less than 1 character.
        AccessError     - When token is invalid
        AccessError     - Occurs when user is not authorised and user not member of channel.

    Return Value:
        A dictionary containing the message_id of the message that was sent.
    '''
    
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

    message_id = make_message(message, channel_id, user['u_id'])
        
    for msg in store:
        if msg['message_id'] == message_id:
            user['messages_created'].remove(message_id)

    return {
        'message_id': message_id,
    }
    
def message_edit(token, message_id, new_message):
    '''
    Edits a current message  

    Arguments:
        token       (str) - A string which holds the token
        message_id  (int) - The message id of current message
        new_message (str) - The message to replace current message

    Exceptions:
        InputError      - Message length is over 1000 characters
        InputError      - When message id is invalid
        AccessError     - When token is invalid
        AccessError     - When u_id is invalid
        AccessError     - When user is not owner or sender

    Return Value:
        Empty dictionary
    '''
    if len(new_message) > 1000:
        raise InputError(description='Message over 1000 characters.')
    if message_id_check(message_id) == None:
        raise InputError
    decoded_token = is_valid_token(token)
    if decoded_token is False:
        raise AccessError(description='Invalid Token.')

    message = message_id_check(message_id)

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
        message['message'] = new_message
    return {}

def message_remove(token, message_id):
    '''
    Removes a message 

    Arguments:
        token      (str) - A string which holds the token
        message_id (int) - The message id of current message
        
    Exceptions:
        InputError      - Message length is over 1000 characters
        InputError      - When message does not exist
        AccessError     - When token is invalid
        AccessError     - When authorised user is invalid
        AccessError     - When user is not owner or sender

    Return Value:
        Empty dictionary
    '''
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
                if user_id in channel['owner_members']:
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
        raise AccessError(description="Not the sender nor an owner")
    if in_dm and is_authorised:
        for dm in data['dms']:
            for message in dm['messages']:
                if message['message_id'] == message_id:
                    dm['messages'].remove(message)                    
                    return {}

    if not in_channel and not in_dm:
        raise InputError(description="Message no longer exists.")

def message_share_v1(token, og_message_id, message, channel_id, dm_id): 

    data = data_store.get()

    #valid token check
    if not is_valid_token(token):
        raise AccessError(description="Not an authorised user invalid")

    #valid channel id check 

    if not channel_id_check(channel_id):
        raise InputError(description='Channel does not exist')

    #valid dm id check 

    if not is_valid_dm_id(dm_id):
        raise InputError(description='Not a valid dm')
    
    #check length of message is not more than 1000 characters
    if (len(message) > 1000):
        raise InputError('Message is longer than 1000 characters.')

    if channel_id == -1:
        #share the message to a dm 

        #check if message is in dm datastore - use helper func

        dm = find_dm(dm_id, data)
        #send a dm msg

        return 
    else: 
        #share message to a channel 

        #check if message is in channel datastore - use helper func 


        channel = channel_id_check(channel_id)
        message_send(token, channel_id, f", {message}: {og_message_id}")

def message_react_v1(token, message_id, react_id): 
    """
    Given a message within a channel or DM the authorised user is part of, 
    add a "react" to that particular message.

    """

    data = data_store.get()

    #token check 
    if not is_valid_token(token):
        raise AccessError(description="Not an authorised user invalid")

    #check if react id is a valid react id - current the only valid react ID the frontend has 
    # is 1

    if react_id != 1:
        raise InputError("React id must be 1.")


    #check if message id is valid id (exists in the datastore channel or dm) 

    message = message_id_check(message_id) #this will only check for messages in channels 
    if message == None:
        raise InputError("Message_id does not exist within a channel.")

    react_user = token_to_user_id(token) 

     #check if message already has a react with id react_id from the auth user
    if not message['reacts']:
        pass
    else:
        for react in message['reacts']:
            for user in react['u_ids']:
                if user == react_user:
                    raise InputError("User has already reacted to this message.")
            
    if message['reacts'] != []:
        for react in message['reacts']:
            react['u_ids'].append(react_user)
    
    else:
        u_ids = []
        u_ids.append(react_user)
        message['reacts'].append({'react_id': react_id, 'u_ids': u_ids, 'is_this_user_reacted': True})

def message_unreact_v1(token, message_id, react_id): 

    data = data_store.get()

    #token check 
    if not is_valid_token(token):
        raise AccessError(description="Not an authorised user invalid")
    
    user = token_to_user_id(token)
    
    message = message_id_check(message_id) #this will only check for messages in channels 
    
    if message == None:
        raise InputError("Message_id does not exist within a channel.")
    
    for react in message['reacts']:
        for user_id in react['u_ids']:
            if user_id == user:
                react['u_ids'].remove(user)






    




 


    









def notifications_get(token):

    df = -1; 

    return { 'notifications': [
            {
            'channel_id': df,
            'dm_id': df,
            'notification_message': "This is just a dummy message."
        }]
    }