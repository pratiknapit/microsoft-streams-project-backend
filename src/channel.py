'''
This file contains channel_invite, channel_details, channel_messages, channel_join
'''
from src.error import InputError, AccessError
from src.data_store import check_if_channel_is_public_or_private, check_if_user_is_channel_member
from src.data_store import channel_id_check, auth_user_id_check, user_id_check, token_check, token_to_user_id, check_existing_owner
from src.data_store import check_existing_member
from src.data_store import data_store
from src.auth import auth_register_v1
from src.channels import channels_create_v1, channels_list_v1, channels_listall_v1

def channel_invite_v1(token, channel_id, u_id):
    '''
    Arguments:
        auth_user_id (int)     - Authorisation hash of a user after registration from auth_register
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
    if channel_id_check(channel_id) == False:
        raise InputError
    
    if token_check(token) == False:
        raise AccessError(description="token not found")
    
    if auth_user_id_check(u_id) == False:
        raise InputError  

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

    return {}


def channel_details_v1(token, channel_id):
    '''
    Arguments:
        auth_user_id (int)          - Authorisation hash of the user that is in the channel.
        channel_id (int)            - The id of channel we need details from.

    Exceptions:
        InputError      - Occurs when the inputted channel_id is not valid.
        AccessError     - Occurs when user is not authorised and user not member of channel.

    Return Value:
        Returns a dictionary containing information about channel.
    '''

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
    member_auth_ids = extract_channel_details['all_members'] #this will be a list of member user ids
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
    
    return channel_details_dictionary


def channel_messages_v1(token, channel_id, start):
    '''
    Arguments:
        auth_user_id (int)          - Authorisation hash of the user that is in the channel.
        channel_id (int)            - The id of channel we need details from.
        start   (int)               - Index of start

    Exceptions:
        InputError      - Occurs when the inputted channel_id is not valid.
        AccessError     - Occurs when user is not authorised and user not member of channel.

    Return Value:
        Returns a dictionary containing messages, start and end
    '''

    if not channel_id_check(channel_id):                                   # Channel does not exist
        raise InputError

    if not check_if_user_is_channel_member(token, channel_id):
        raise AccessError

    store = data_store.get()
    total_messages = len(store['Messages'])

    if start > total_messages:
        raise InputError

    message_dictionary = {
        'message': [],
    }
    msg_count = len(message_dictionary['message'])

    num_loop = min(msg_count, 50)
    data = data_store.get()['channels']
    
    for msg_num in range(0, num_loop):
        msg_list = data[msg_num]["Messages"]
        message_dictionary['message'].append(msg_list[num_loop - 1])

    if num_loop < 50:
        end = -1
    else:
        end = start + 50


    message_dictionary["start"] = start
    message_dictionary["end"] = end

    return message_dictionary
    

def channel_join_v1(token, channel_id):
    '''
    Arguments:
        auth_user_id (int)          - Authorisation hash of user that is trying to join channel
        channel_id (int)            - The id of the channel that the user is trying to join

    Exceptions:
        InputError - Occurs when the inputted channel_id is not valid and user is not channel member
        AccessError- Occurs when user not authorised and when user is trying to join private channel

    Return Value:
        Returns an empty dictionary
    '''
    if not token_check(token):
        raise AccessError

    if channel_id_check(channel_id) is False:
        raise InputError("Channel id failed.")

    auth_user_id = token_to_user_id(token)
    user_detail = auth_user_id_check(auth_user_id)

    if check_existing_member(auth_user_id, channel_id) is True:
        raise InputError

    if user_detail['is_global_owner'] == 2:
        if check_if_channel_is_public_or_private(channel_id) is False:
            raise AccessError

    store = data_store.get()

    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            channel['all_members'].append(auth_user_id)

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
    
    user_id = token_to_user_id(token)

    if channel_id_check(channel_id) is False:
        raise InputError
    
    for channel in data['channels']:
        if channel_id == channel['channel_id']:
            #Remove the user from the owner members if they are an owner 
            for owner in channel['owner_members']:
                if owner == user_id:
                    channel['owner_members'].remove(user_id)
                    break
            #Remove the user for the member list
            valid_member = False
            for member in channel['all_members']:  
                if user_id == member: 
                    channel['all_members'].remove(user_id)
                    valid_member = True
                    break
    
    if valid_member == False:
        raise AccessError("User is not a member of the channel")

    return {}

def channel_add_owner_v2(token, channel_id, u_id):

    data = data_store.get()

    if token_check(token) == False:
        raise AccessError(description="token not found")
    
    if not auth_user_id_check(u_id):
        raise AccessError  

    if check_existing_owner(u_id, channel_id) is False:
        raise InputError("User is not an owner of the channel.")

    if channel_id_check(channel_id) is False:
        raise InputError
    
    if check_existing_member(u_id, channel_id) is False:
        raise InputError
    
    auth_user_id = token_to_user_id(token) 

    if check_existing_owner(auth_user_id, channel_id) is False:
        raise AccessError
    
    user_detail = auth_user_id_check(auth_user_id)

    if user_detail['is_global_owner'] == 2:
        if check_existing_owner(auth_user_id, channel_id) is False:
            raise AccessError
        
    #If no error was raised, we can then add a new owner to the channel.

    new_owner_id = u_id  
    for channel in data['channels']:	
        if channel["channel_id"] == channel_id:
            channel['owner_members'].append(new_owner_id)
            break
    
    return {}
    
def channel_remove_owner_v2(token, channel_id, u_id):
    data = data_store.get()

    if token_check(token) == False:
        raise AccessError(description="token not found")
    
    if not auth_user_id_check(u_id):
        raise AccessError  

    if check_existing_owner(u_id, channel_id) is False:
        raise InputError("User is not an owner of the channel.")

    if channel_id_check(channel_id) is False:
        raise InputError
    
    if check_existing_member(u_id, channel_id) is False:
        raise InputError
    
    auth_user_id = token_to_user_id(token) 

    if check_existing_owner(auth_user_id, channel_id) is False:
        raise AccessError
    
    user_detail = auth_user_id_check(auth_user_id)

    if user_detail['is_global_owner'] == 2:
        if check_existing_owner(auth_user_id, channel_id) is False:
            raise AccessError
    
    new_owner_id = u_id  
    for channel in data['channels']:	
        if channel["channel_id"] == channel_id:
            channel['owner_members'].remove(new_owner_id)
            break
    
    return {}
    



    

if __name__ == '__main__':

    dummy_user_1 = auth_register_v1('dummyuser1@gmail.com', 'passworddd', 'Alpha', 'AA')
    dummy_user_2 = auth_register_v1('dummyuser2@gmail.com', 'yessword', 'Beta', 'BB')
    dummy_user_3 = auth_register_v1('dummyuser3@gmail.com', 'passsssword', 'Ceal', 'CC')

    data = data_store.get()

    channel = channels_create_v1(dummy_user_1['token'], 'dummy_user_1_channel', True)
    channels_create_v1(dummy_user_2['token'], 'dummy_user_2_channel', True)
    channels_create_v1(dummy_user_3['token'], 'dummy_user_3_channel', True)
    channel_priv = channels_create_v1(dummy_user_1['token'], 'dummy_user_4_channel', False)





    
    """
    channel_invite_v1(dummy_user_1['token'], 1, 2)
    channel_invite_v1(dummy_user_3['token'], 3, 2)
    channel_invite_v1(dummy_user_2['token'], 2, 3)
    channel_invite_v1(dummy_user_3['token'], 2, 1)
    channel_invite_v1(dummy_user_1['token'], 4, 3)

    
    channel_leave_v2(dummy_user_3['token'], 1)
    channel_leave_v2(dummy_user_3['token'], 2)
    channel_leave_v2(dummy_user_3['token'], 3)
    
    channel_add_owner_v2(dummy_user_1['token'], 1, dummy_user_2['auth_user_id'])
    channel_add_owner_v2(dummy_user_2['token'], 2, dummy_user_3['auth_user_id'])
    channel_add_owner_v2(dummy_user_3['token'], 2, dummy_user_1['auth_user_id'])
    """
    #channel_remove_owner_v2(dummy_user_1['token'], 1, dummy_user_2['auth_user_id'])
    #channel_remove_owner_v2(dummy_user_2['token'], 2, dummy_user_3['auth_user_id'])
    """
    print("")
    for channel in data['channels']:
        print(channel['all_members'])
    print("")
    for channel in data['channels']:
        print(channel['owner_members'])
    print("")
    print(channel_details_v1(dummy_user_1['token'], 1))
    print(channel_details_v1(dummy_user_2['token'], 2))
    """
    #channel_join_v1(dummy_user_1['token'], 2)
    print(channels_list_v1(dummy_user_1['token']))
    #print(token_to_user_id(dummy_user_1['token']))
    
    
