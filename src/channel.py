'''
This file contains channel_invite, channel_details, channel_messages, channel_join
'''
from src.error import InputError, AccessError
from src.data_store import check_if_channel_is_public_or_private, check_if_user_is_channel_member
from src.data_store import channel_id_check, auth_user_id_check, user_id_check
from src.data_store import data_store

def channel_invite_v1(auth_user_id, channel_id, u_id):
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
    if not channel_id_check(channel_id):
        raise InputError

    # checks if user_id is correct, if not, it raises an InputError
    if not user_id_check(u_id):
        raise InputError

    # check if auth_user_id correct otherwise return InputError
    if not auth_user_id_check(auth_user_id):
        raise InputError

    # check if channel id correct but auth user is not a member of the channel
    if check_if_user_is_channel_member(auth_user_id, channel_id) is False:
        raise AccessError

    # check if the user invited is already part of channel
    if check_if_user_is_channel_member(u_id, channel_id) is True:
        raise InputError

    data = data_store.get()
    user = auth_user_id_check(u_id)
    for channel in data["channels"]:
        if channel["channel_id"] == channel_id:
            channel["all_members"].append(user["u_id"])
    user['channel_id_members'].append(channel_id)
    data_store.set(data)
    return {}

def channel_details_v1(auth_user_id, channel_id):
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

    if not auth_user_id_check(auth_user_id):
        raise AccessError
    #Check if channel_id is valid
    if channel_id_check(channel_id) is False:
        raise InputError("channel id not valid")
        #Check if user is in the channel
    if check_if_user_is_channel_member(auth_user_id, channel_id) is False:
        raise AccessError

    #Create a new dictionery that will store all the channel_details
    channel_details_dictionary = {
    }

    #Something that will let me access the channels dictionary
    extract_channel_details = channel_id_check(channel_id)
    channel_details_dictionary['name'] = extract_channel_details['name']
    channel_details_dictionary['is_public'] = extract_channel_details['is_public']

    owner_auth_id = extract_channel_details['owner_members']
    channel_details_dictionary['owner_members'] = []
    new_owner_ids = {
    }
    owner_id = auth_user_id_check(owner_auth_id[0])
    new_owner_ids['u_id'] = owner_id['u_id']
    new_owner_ids['email'] = owner_id['email']
    new_owner_ids['name_first'] = owner_id['name_first']
    new_owner_ids['name_last'] = owner_id['name_last']
    new_owner_ids['handle_str'] = owner_id['handle_str']
    channel_details_dictionary['owner_members'].append(new_owner_ids)

    member_id = extract_channel_details['all_members']
    channel_details_dictionary['all_members'] = []

    for member in member_id:
        member_dict = {

        }
        mem_id = auth_user_id_check(member)
        member_dict['u_id'] = mem_id['u_id']
        member_dict['email'] = mem_id['email']
        member_dict['name_first'] = mem_id['name_first']
        member_dict['name_last'] = mem_id['name_last']
        member_dict['handle_str'] = mem_id['handle_str']
        channel_details_dictionary['all_members'].append(member_dict)

    return channel_details_dictionary

def channel_messages_v1(auth_user_id, channel_id, start):
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
    if not auth_user_id_check(auth_user_id):
        raise AccessError                                                  # User not exist at all

    if not channel_id_check(channel_id):                                   # Channel does not exist
        raise InputError

    if not check_if_user_is_channel_member(auth_user_id, channel_id):
        raise AccessError

    store = data_store.get()
    total_messages = len(store['Messages'])

    if start > total_messages:
        raise InputError


    messages_dictionary = {

    }
    messages_dictionary['messages'] = []

    msg_count = len(messages_dictionary['messages'])

    num_loop = min(msg_count, 50)
    data = data_store.get()
    msg_list = data["channels"]["Messages"]

    for msg_num in range(0, num_loop):
        messages_dictionary['messages'].append(msg_list[num_loop - 1])

    if num_loop < 50:
        end = -1
    else:
        end = start + 50


    messages_dictionary["start"] = start
    messages_dictionary["end"] = end

    return messages_dictionary

def channel_join_v1(auth_user_id, channel_id):
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
    if not auth_user_id_check(auth_user_id):
        raise AccessError

    if channel_id_check(channel_id) is False:
        raise InputError

    if check_if_user_is_channel_member(auth_user_id, channel_id) is True:
        raise InputError

    user_detail = auth_user_id_check(auth_user_id)
    if user_detail['is_global_owner'] == 2:
        if check_if_channel_is_public_or_private(channel_id) is False:
            raise AccessError

    store = data_store.get()
    channel_to_join = channel_id_check(channel_id)

    for channel in store['channels']:
        if channel['channel_id'] == channel_to_join['channel_id']:
            channel['all_members'].append(auth_user_id)

    return {}
