'''
This file contains channel_invite, channel_details, channel_messages, channel_join
'''
from src.error import InputError, AccessError
from src.data_store import check_if_channel_is_public_or_private, check_if_user_is_channel_member, remove_owner_channel
from src.data_store import channel_id_check, auth_user_id_check, user_id_check, token_check, token_to_user_id, check_existing_owner
from src.data_store import check_existing_member, leave_channel, add_owner_channel, remove_owner_channel, is_valid_token, find_channel, is_user_in_channel
from src.data_store import data_store, save_data
from src.auth import auth_register_v1
from src.channels import channels_create_v1, channels_list_v1, channels_listall_v1
from datetime import datetime


def channel_invite_v1(token, channel_id, u_id):
    '''
    Arguments:
        token (str)            - Token of a user after registration from auth_register
        channel_id (int)       - The id of a channel
        u_id (int)             - The auth_user_id of someone else

    Exceptions:
        InputError    - Occurs when channel_id does not refer to a valid channel
        InputError    - Occurs when u_id does not refer to a valid user
        InputError    - Occurs when u_id refers to user who is already part of selected channel
        AccessError   - Occurs when channel_id valid but auth_user_id is not member of the channel

    Return Value:
        Returns nothing on the condition that auth_user_id, channel_id and u_id are all correct
    '''

    # check if corect channel id otherwise return Input error (not valid channel)
    
    data = data_store.get()
    
    if channel_id_check(channel_id) == False:
        raise InputError
    
    if token_check(token) == False:
        raise AccessError(description="token not found")

    if check_existing_member(u_id, channel_id) == True:
        raise InputError
    
    auth_user_id = token_to_user_id(token) 
    
    if check_existing_member(auth_user_id, channel_id) == False:
        raise AccessError
    


    #Once all errors are checked, we can now invite the user to the channel, it
    #does not matter if the channel is public or private.

    data = data_store.get()
    #user = auth_user_id_check(u_id)
    for channel in data["channels"]:
        if channel["channel_id"] == channel_id:
            channel["all_members"].append(u_id)
    #user['channel_id_members'].append(channel_id)
    #data_store.set(data)


    #Adding this to notifications
    user_id = token_to_user_id(token)
    react_user = auth_user_id_check(user_id)
    channel = channel_id_check(channel_id)
    
    react_user_str_handle = react_user['handle_str']
    channel_name = channel['name']
    notif_message = f"{react_user_str_handle} added you to {channel_name}"
    user_notif = auth_user_id_check(u_id)
    user_notif['notifications'].insert(0, {'channel_id': channel_id, 'dm_id': -1, 'notification_message': notif_message})


    #User stats implementation

    for user in data['users']:
        if user['u_id'] == u_id:
            if len(user['user_stats']['channels_joined']) == 0:
                channels_joined = 1
            else:
                channels_joined = user['user_stats']['channels_joined'][-1]['num_channels_joined'] + 1  
            
            user['user_stats']['channels_joined'].append({
                'num_channels_joined':channels_joined, 
                'time_stamp':int(datetime.now().timestamp())
                })

    save_data(data)

    return {}


def channel_details_v1(token, channel_id):
    '''
    Arguments:
        token (str)            - Token of a user after registration from auth_register
        channel_id (int)            - The id of channel we need details from.

    Exceptions:
        InputError      - Occurs when the inputted channel_id is not valid.
        AccessError     - Occurs when user is not authorised and user not member of channel.

    Return Value:
        Returns a dictionary containing information about channel.
    '''

    data = data_store.get()

    if token_check(token) == False:
        raise AccessError(description="token not found")
    
    #Check if channel_id is valid
    if channel_id_check(channel_id) is False:
        raise InputError(description="channel id not valid")

    #Check if user is in the channel
    if check_if_user_is_channel_member(token, channel_id) is False:
        raise AccessError(description="User is already a channel member")

    #Create a new dictionary that will store all the channel_details
    channel_details_dictionary = {
    }
    #Something that will let me access the channels dictionary
    extract_channel_details = channel_id_check(channel_id)
    channel_details_dictionary['name'] = extract_channel_details['name']
    channel_details_dictionary['is_public'] = extract_channel_details['is_public']

    #Need to extract the owner details to meet spec for details output
    owner_auth_ids = extract_channel_details['owner_members'] #this will be a list of owner user ids
    owner_details = [
    ]
    for id in owner_auth_ids:
        owner = auth_user_id_check(id)
        owner_det = {}
        owner_det['u_id'] = owner['u_id']
        owner_det['email'] = owner['email']
        owner_det['name_first'] = owner['name_first']
        owner_det['name_last'] = owner['name_last']
        owner_det['handle_str'] = owner['handle_str']
        owner_details.append(owner_det)
    
    channel_details_dictionary['owner_members'] = owner_details

    #Need to extract the member details to meet spec for details output
    member_auth_ids = extract_channel_details['all_members'] 
    member_details = [
    ]
    for id in member_auth_ids:
        member = auth_user_id_check(id)
        member_det = {}
        member_det['u_id'] = member['u_id']
        member_det['email'] = member['email']
        member_det['name_first'] = member['name_first']
        member_det['name_last'] = member['name_last']
        member_det['handle_str'] = member['handle_str']
        member_details.append(member_det)
    
    channel_details_dictionary['all_members'] = member_details

    save_data(data)
    
    return channel_details_dictionary


def channel_messages_v1(token, channel_id, start):
    '''
    Arguments:
        token (str)          - Authorisation hash of the user that is in the channel.
        channel_id (int)     - The channel id of channel we need details from.
        start   (int)        - Index of start

    Exceptions:
        InputError      - Occurs when the inputted channel_id is not valid.
        AccessError     - Occurs when user is not authorised and user not member of channel.

    Return Value:
        Returns a dictionary containing messages, start and end
    '''

    data = data_store.get()

    if not channel_id_check(channel_id):                                   # Channel does not exist
        raise InputError

    if not check_if_user_is_channel_member(token, channel_id):
        raise AccessError

    channel = channel_id_check(channel_id)
    total_messages = len(channel['Messages'])

    if start >= total_messages and start != 0:
        raise InputError('Start is greater than the total number of messages in the channel.')

    # calculate the ending return value
    end = start + 50 if (start + 50 < len(data['channels']) - 1) else -1
    message_dictionary = {'messages': [],
                          'start': start,
                          'end': end
                          }

    if end == -1:
        for i in range(start, len(channel['Messages'])):
            message_dictionary['messages'].append(channel['Messages'][i])
    else:
        for i in range(start, end):
            message_dictionary['messages'].append(channel['Messages'][i])
    

    save_data(data)
    return message_dictionary

def channel_join_v1(token, channel_id):
    '''
    Arguments:
        token (str)            - Token of a user after registration from auth_register
        channel_id (int)            - The id of the channel that the user is trying to join

    Exceptions:
        InputError - Occurs when the inputted channel_id is not valid and user is not channel member
        AccessError- Occurs when user not authorised and when user is trying to join private channel

    Return Value:
        Returns an empty dictionary
    '''

    data = data_store.get()

    if not token_check(token):
        raise AccessError

    if channel_id_check(channel_id) is False:
        raise InputError("Channel id failed.")

    auth_user_id = token_to_user_id(token)
    user_detail = auth_user_id_check(auth_user_id)

    if check_existing_member(auth_user_id, channel_id) is True:
        raise InputError("Already a member.")

    if user_detail['is_global_owner'] == 2:
        if check_if_channel_is_public_or_private(channel_id) is False:
            raise AccessError

    store = data_store.get()
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            channel['all_members'].append(auth_user_id)


    #User stats implementation
    u_id = token_to_user_id(token)
    for user in data['users']:
        if user['u_id'] == u_id:
            if len(user['user_stats']['channels_joined']) == 0:
                channels_joined = 1
            else:
                channels_joined = user['user_stats']['channels_joined'][-1]['num_channels_joined'] + 1  
            
            user['user_stats']['channels_joined'].append({
                'num_channels_joined':channels_joined, 
                'time_stamp':int(datetime.now().timestamp())
                })

    save_data(data)

    return {}



def channel_leave_v2(token, channel_id):
    '''
    Given a channel with ID channel_id that the authorised user is a member of, 
    remove them as a member of the channel. Their messages should remain in the channel. 
    If the only channel owner leaves, the channel will remain.

    Arguments:
        token (string) - an input token that validates a session
        channel_id (integer) - the id number of the channel the user, who is 
                               to be removed, belongs to          
    Exceptions:
        InputError  - Occurs if the channel ID is not of a valid channel
        AccessError - Occurs when the authorised user (the one who is inputting
                      the token) is not a member of the channel 
    
    Return Value:
        Returns an empty dictionary
    ''' 

    data = data_store.get()

    if token_check(token) == False:
        raise AccessError(description="token not found")

    if channel_id_check(channel_id) is False:
        raise InputError
    
    v_member = leave_channel(token, channel_id)
    
    if v_member == False:
        raise AccessError("User is not a member of the channel")


    #User stats implementation
    u_id = token_to_user_id(token)
    for user in data['users']:
        if user['u_id'] == u_id:

            channels_joined = user['user_stats']['channels_joined'][-1]['num_channels_joined'] - 1  
            
            user['user_stats']['channels_joined'].append({
                'num_channels_joined':channels_joined, 
                'time_stamp':int(datetime.now().timestamp())
                })
    
    save_data(data)

    return {}

def channel_add_owner_v2(token, channel_id, u_id):

    '''
        Arguments:
            token (str)                 - Token of user that is trying to join channel
            channel_id (int)            - The id of the channel that the user is trying to join
            u_id (int)                  - The id of the user is trying to join


        Exceptions:
            InputError - Occurs when the inputted channel_id is not valid and user is not channel member
            AccessError- Occurs when user not authorised and when user is trying to join private channel

        Return Value:
            Returns an empty dictionary
    '''

    data = data_store.get()

    if token_check(token) == False:
        raise AccessError(description="token not found")
    
    if not auth_user_id_check(u_id):
        raise InputError("Failed user id check.")

    if check_existing_owner(u_id, channel_id) is True:
        raise InputError("User is already an owner of the channel.")

    if channel_id_check(channel_id) is False:
        raise InputError("Failed channel id check.")
    
    if check_existing_member(u_id, channel_id) is False:
        raise InputError("Existing member is false.")
    
    auth_user_id = token_to_user_id(token) 
    user_detail = auth_user_id_check(auth_user_id)

    if user_detail['is_global_owner'] == 2:
        if check_existing_owner(auth_user_id, channel_id) is False:
            raise AccessError("User does not have owner permissions.")
        
    #If no error was raised, we can then add a new owner to the channel.

    save_data(data)

    return add_owner_channel(channel_id, u_id)
    
def channel_remove_owner_v2(token, channel_id, u_id):

    '''
        Arguments:
            token (str)                 - Token of user that is trying to join channel
            channel_id (int)            - The id of the channel that the user is trying to join
            u_id (int)                  - The id of the user is trying to join


        Exceptions:
            InputError - Occurs when the inputted channel_id is not valid and user is not channel member
            AccessError- Occurs when user not authorised and when user is trying to join private channel

        Return Value:
            Returns an empty dictionary
    '''
    
    data = data_store.get()

    if token_check(token) == False:
        raise AccessError(description="token not found")
    
    if not auth_user_id_check(u_id):
        raise InputError 

    if channel_id_check(channel_id) is False:
        raise InputError
    
    if check_existing_member(u_id, channel_id) is False:
        raise InputError
    
    channel_info = channel_id_check(channel_id)
    if len(channel_info['owner_members']) == 1:
        if check_existing_owner(u_id, channel_id) is True:
            raise InputError("User is only owner of the channel.")
     
    auth_user_id = token_to_user_id(token) 
    user_detail = auth_user_id_check(auth_user_id)
    if user_detail['is_global_owner'] == 2:
        if check_existing_owner(auth_user_id, channel_id) is False:
            raise AccessError

    save_data(data)
    
    return remove_owner_channel(channel_id, u_id)