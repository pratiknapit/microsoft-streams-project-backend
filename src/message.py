'''
This file contains message_send, message_edit, message_remove
'''
from src.data_store import data_store, is_valid_user_id, make_message, find_message_source
from src.data_store import token_check, channel_id_check, message_id_check, save_data
from src.data_store import is_valid_token, check_if_user_is_channel_member, token_to_user_id
from src.data_store import auth_user_id_check, user_id_check, owner_channel_check, find_dm, is_valid_dm_id
from src.data_store import find_user, find_dm, find_channel, is_valid_dm_id, is_user_in_dm, is_user_in_channel
from src.error import InputError, AccessError
from datetime import datetime, timezone
import time

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
    
    #check length of message is not more than 1000 characters
    if (len(message) > 1000):
        raise InputError('Message is longer than 1000 characters.')

    if channel_id == -1 and dm_id == -1:
        raise InputError("A channel if or dm if must be an input.")

    if channel_id != -1 and dm_id != -1:
        raise InputError("A channel if or dm if must be an input.")

    auth_user = token_to_user_id(token)
    user = auth_user_id_check(auth_user)
    user_handle = user['handle_str']

    if channel_id != -1:
        #share message to a channel 
        if not channel_id_check(channel_id):
            raise InputError(description='Channel does not exist')

        #check if message is in channel datastore - use helper func 
        og_message = message_id_check(og_message_id)
        new_message = message + '\n"""\n' + og_message['message'] + '\n"""\n'

        #channel = channel_id_check(channel_id)
        msg_send = message_send(token, channel_id, f"{user_handle} shared this {message}: {new_message}")
        save_data(data)
        return {'shared_message_id': msg_send['message_id']}
    
    if dm_id != -1: 
        #share the message to a dm 
        if not is_valid_dm_id(dm_id):
            raise InputError(description='Not a valid dm')
        og_message = find_dm(dm_id, data)
        new_message = message + '\n"""\n' + og_message + '\n"""\n'

        #check if message is in dm datastore - use helper func

        dm_send = message_senddm(token, dm_id, new_message)
        save_data(data)
        return {'shared_message_id': dm_send['message_id']}
        #send a dm msg
    
    
        

def message_react_v1(token, message_id, react_id): 
    """
    Given a message within a channel or DM the authorised user is part of, 
    add a "react" to that particular message.

    Need to add dm implementation. But first test with channel msgs.

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

    react_user_id = token_to_user_id(token) 

     #check if message already has a react with id react_id from the auth user
    if not message['reacts']:
        pass
    else:
        for react in message['reacts']:
            for user in react['u_ids']:
                if user == react_user_id:
                    raise InputError("User has already reacted to this message.")
            
    if message['reacts'] != []:
        for react in message['reacts']:
            react['u_ids'].append(react_user_id)
            if react_user_id == message['u_id']:
                react['is_this_user_reacted'] == True 
    
    else:
        u_ids = []
        u_ids.append(react_user_id)
        if react_user_id == message['u_id']:
            user_reacted = True
        else:
            user_reacted = False
        message['reacts'].append({'react_id': react_id, 'u_ids': u_ids, 'is_this_user_reacted': user_reacted})

    #Add notification to the user's notifications

    react_user = auth_user_id_check(react_user_id)
    react_user_str_handle = react_user['handle_str']

    user_og_msg_id = message['u_id'] 
    user_og = auth_user_id_check(user_og_msg_id)
    channel_name = channel_id_check(message['channel_id'])['name']
    notif_message = f"{react_user_str_handle} reacted to your message in {channel_name}"
    user_og['notifications'].append({'channel_id': message['channel_id'], 'dm_id': -1, 'notification_message': notif_message})
    
    save_data(data)

    return {}

def message_unreact_v1(token, message_id, react_id): 

    #Still need to implement for dm use.

    data = data_store.get()

    #token check 
    if not is_valid_token(token):
        raise AccessError(description="Not an authorised user invalid")
    
    user = token_to_user_id(token)
    
    message = message_id_check(message_id) #this will only check for messages in channels 
    
    if react_id != 1:
        raise InputError("React id must be 1.")
        
    if message == None:
        raise InputError("Message_id does not exist within a channel.")
    
    for react in message['reacts']:
        for user_id in react['u_ids']:
            if user_id == user:
                react['u_ids'].remove(user)

    save_data(data)

    return {}


def notifications_get(token):

    user_id = token_to_user_id(token)
    user = auth_user_id_check(user_id)
    return_list = [] 
    if len(user['notifications']) == 0:
        return {'notifications': return_list }
    
    elif len(user['notifications']) <= 20:
        for notifs in user['notifications']:
            return_list.append(notifs) 
        return {'notifications': return_list }

    else:
        i = 0
        while (i < 20):
            return_list.append(user['notifications'][i])
            i = i + 1

        return {'notifications': return_list 
        }

def message_senddm(token, dm_id, message):

    data = data_store.get()
    token_data = is_valid_token(token)

    if token_data == False:
        raise AccessError("Token invalid")

    auth_user_id = token_data['auth_user_id']
    auth_user = find_user(auth_user_id)

    if len(message) > 1000 or len(message) < 1:
        raise InputError("message length invalid")

    if is_valid_dm_id(dm_id) == False:
        raise InputError('dm is invalid')
    dm = find_dm(dm_id, data)

    if is_user_in_dm(dm_id, auth_user_id) == False:
        raise AccessError('user is not in the dm they are sharing message to')

    message_id = data['msg_counter'] + 1
    new_message = { 'message_id': message_id, 
                    'u_id': auth_user_id,
                    'message': message, 
                    'time_created': datetime.now().replace(tzinfo=timezone.utc).timestamp(), 
                    'is_pinned': False, 
                    'reactions': []
                    }

    dm['messages'].insert(0, new_message)

    # notify tagged users
    #user_message = tag_users(message, auth_user['account_handle'], dm_id, -1)
    #if user_message:
    #    user, message = user_message
    #    user = next(u for u in data['users'] if u['user_id'] == user)
    #    user['notifications'].insert(0, message)

    auth_user['sent_messages'].append(message_id)
    
    #auth_user['user_stats']['messages_sent'].append({'num_messages_sent':len(auth_user['sent_messages']), 'time_stamp':int(datetime.now().timestamp())})
    
    data['msg_counter'] += 1
    
    #if len(data['dreams_stats']['messages_exist']) == 0:
    #    messages_exist = 1
    #else:
    #    messages_exist = data['dreams_stats']['messages_exist'][-1]['num_messages_exist'] + 1

    #data['dreams_stats']['messages_exist'].append({'num_messages_exist':messages_exist, 'time_stamp':int(datetime.now().timestamp())})
    
    save_data(data)

    return {'message_id': message_id}


def message_sendlater(token, channel_id, message, time_sent):

    data = data_store.get()
    if not is_valid_token(token):
        raise AccessError("Invalid token id.")

    if not channel_id_check(channel_id):
        raise InputError("Invalid channel id.")

    user_id = is_valid_token(token)['auth_user_id']
    if not is_user_in_channel(channel_id, user_id):
        raise AccessError("user is not a member of the channel with channel id {channel_id}.")

    if len(message) > 1000:
        raise InputError("message is longer than 1000 characters")

    current_timestamp = datetime.now().replace(tzinfo=timezone.utc).timestamp()
    if time_sent < current_timestamp:
        raise InputError("the time for the message to send is in the past.")

    delay_time = time_sent - current_timestamp
    time.sleep(delay_time)
    messageID_dict = message_send(token, channel_id, message)
    save_data(data)
    return messageID_dict

def message_sendlaterdm(token, dm_id, message, time_sent):
    data = data_store.get()

    if not is_valid_token(token):
        raise AccessError("Invalid token id.")

    if not is_valid_dm_id(dm_id):
        raise InputError("Invalid dm id.")

    user_id = is_valid_token(token)['auth_user_id']
    if not is_user_in_dm(dm_id, user_id):
        raise AccessError("user is not a member of the DM with dm id {dm_id}.")

    if len(message) > 1000:
        raise InputError("message is longer than 1000 characters")

    current_timestamp = datetime.now().replace(tzinfo=timezone.utc).timestamp()
    if time_sent < current_timestamp:
        raise InputError("the time for the message to send is in the past.")

    delay_time = time_sent - current_timestamp
    time.sleep(delay_time)
    messageID_dict = message_senddm(token, dm_id, message)
    save_data(data)

    return messageID_dict

def message_pin(token, message_id):
    decoded_token = is_valid_token(token)
    if decoded_token is False:
        raise AccessError(description="Invalid Token.")

    data = data_store.get()

    message_found = find_message_source(message_id, data)

    if message_found is None:
        raise InputError("Message was not found.")

    for dm in data['dms']:
        for dm_msg in dm['messages']:
            if dm_msg['message_id'] == message_id:

                is_member = False
                for member in dm['members']:
                    if member == decoded_token['auth_user_id']:
                        is_member = True

                is_owner = False
                if dm['creator'] == decoded_token['auth_user_id']:
                    is_owner = True
                    is_member = True

                if is_member is False:
                    raise AccessError(description="Not a member of the DM")

                if is_owner is False:
                    raise AccessError(description="Not a owner of the DM")

                if dm_msg['is_pinned'] is True:
                    raise InputError(description="DM Message already pinned")

                dm_msg['is_pinned'] = True

    for channel in data['channels']:
        for channel_msg in channel['Messages']:
            if channel_msg['message_id'] == message_id:

                is_member = False
                for member in channel['all_members']:
                    if member == decoded_token['auth_user_id']:
                        is_member = True

                is_owner = False
                for owner in channel['owner_members']:
                    if owner == decoded_token['auth_user_id']:
                        is_owner = True
                        is_member = True

                if is_member is False:
                    raise AccessError(
                        description="Not a member of this channel")

                if is_owner is False:
                    raise AccessError(
                        description="Not an owner of this channel")

                if channel_msg['is_pinned'] is True:
                    raise InputError(
                        description="Channel Message already pinned")

                channel_msg['is_pinned'] = True

    save_data(data)

    return {}


def message_unpin(token, message_id):
    decoded_token = is_valid_token(token)
    if decoded_token is False:
        raise AccessError("Invalid Token.")

    data = data_store.get()

    message_found = find_message_source(message_id, data)

    if message_found is None:
        raise InputError("Message was not found.")

    for dm in data['dms']:
        for dm_msg in dm['messages']:
            if dm_msg['message_id'] == message_id:

                is_member = False
                for member in dm['members']:
                    if member == decoded_token['auth_user_id']:
                        is_member = True

                is_owner = False
                if dm['creator'] == decoded_token['auth_user_id']:
                    is_owner = True
                    is_member = True

                if is_member is False:
                    raise AccessError("Not a member of the DM")

                if is_owner is False:
                    raise AccessError("Not a owner of the DM")

                if dm_msg['is_pinned'] is False:
                    raise InputError("DM Message already unpinned")

                dm_msg['is_pinned'] = False

    for channel in data['channels']:
        for channel_msg in channel['Messages']:
            if channel_msg['message_id'] == message_id:

                is_member = False
                for member in channel['all_members']:
                    if member == decoded_token['auth_user_id']:
                        is_member = True

                is_owner = False
                for owner in channel['owner_members']:
                    if owner == decoded_token['auth_user_id']:
                        is_owner = True
                        is_member = True

                if is_member is False:
                    raise AccessError(
                        description="Not a member of this channel")

                if is_owner is False:
                    raise AccessError(
                        description="Not an owner of this channel")

                if channel_msg['is_pinned'] is False:
                    raise InputError(
                        description="Channel Message already unpinned")

                channel_msg['is_pinned'] = False

    save_data(data)

    return {}
