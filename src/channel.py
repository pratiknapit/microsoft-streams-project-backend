from src.error import InputError, AccessError
from src.data_store import auth_user_id_check, channel_id_check, check_if_user_is_channel_member, data_store, check_if_channel_is_public_or_private
from src.data_store import channel_id_check, check_if_user_is_channel_member, auth_user_id_check
from src.data_store import data_store

def channel_invite_v1(auth_user_id, channel_id, u_id):
    # check if corect channel id otherwise return Input error (not valid channel)
    if not channel_id_check(channel_id): 
            raise InputError

    # check if user id correct otherwise return Input Error (not valid  user id or user 
    # already in channel)
    if not auth_user_id_check(auth_user_id):
            raise AccessError
            #not inputerror

    if not auth_user_id_check(u_id):
            raise AccessError

    # check when channel id corect but user(who invited) not part of channel
    if not check_if_user_is_channel_member(auth_user_id, channel_id):
            raise AccessError


    #check if user is inviting himself
    if auth_user_id == u_id:
        raise AccessError
    
    data = data_store.get()
    user = auth_user_id_check(auth_user_id)
    for channel in data["channels"]:
        if channel["channel_id"] == channel_id:
            channel["all_members"].append(user["u_id"])
    user['channel_id_members'].append(channel_id)
    data_store.set(data)
    return {}

def channel_details_v1(auth_user_id, channel_id):
    '''
    Arguments:
        auth_user_id (int)          - Autherisation hash of the user that is in the channel.
        channel_id (int)            - The id of channel we need details from.
    
    Exceptions: 
        InputError      - Occurs when the inputted channel_id is not valid.
        AccessError     - Occurs when user is not autherised and when user is not a member of the channel.
    
    Return Value:
        Returns a dictionery containing information about the channel such as 'name', 'is_public', 'owner_members', 'all_members'
    '''
    
    if not auth_user_id_check(auth_user_id):
        raise AccessError
    #Check if channel_id is valid
    if channel_id_check(channel_id) == False:       
        raise InputError("channel id not valid")
        #Check if user is in the channel
    if check_if_user_is_channel_member(auth_user_id, channel_id) == False: 
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
'''
return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            }
        ],
    }
'''

def channel_messages_v1(auth_user_id, channel_id, start):

    if not auth_user_id_check(auth_user_id):   
        raise AccessError                                                  # User not exist at all

    if not channel_id_check(channel_id):                                   # Channel does not exist
        raise InputError

    if not check_if_user_is_channel_member(auth_user_id, channel_id):      # auth_user_id is not a member of channel
        raise AccessError

    total_messages = 0   
    store = data_store.get()
    
    for message in store['Messages']:
        total_messages += 1
    
    if start > total_messages:                                             # Start is greater than the total number of messages in channel
        raise InputError

    dict_start = {
        'messages':[]
    }

    dict_finish = {
        'messages':[]
    }
    dict_start = data_store.get()['Messages']
   
    count = 0
    if len(dict_start) != 0:
        for msg in reversed(dict_start):            
            if count >= start:                 
                fields = {
                    'message_id': msg['message_id'],
                    'u_id': msg['auth_user_id'],
                    'message': msg['message'],
                    'time_created': msg['time_created'],                        
                }
                dict_finish['messages'].append(fields)    
                count += 1
            if count >= 50:
                count = -1
                break
    
    dict_finish['start'] = start
    dict_finish['end'] = count
    return dict_finish

####
#    return {
#        'messages': [
#            {
#                'message_id': 1,
#                'u_id': 1,
#                'message': 'Hello world',
#                'time_created': 1582426789,
#            }
#        ],
#        'start': 0,
#        'end': 50,
#    }

def channel_join_v1(auth_user_id, channel_id):
    '''
    Arguments:
        auth_user_id (int)          - Autherisation hash of the user that is trying to join the channel
        channel_id (int)            - The id of the channel that the user is trying to join
    
    Exceptions: 
        InputError      - Occurs when the inputted channel_id is not valid and user is not a channel member
        AccessError     - Occurs when user is not autherised and when user is trying to join a private channel
    
    Return Value:
        Returns an empty dictionery
    '''
    if not auth_user_id_check(auth_user_id):
        raise AccessError

    if channel_id_check(channel_id) == False:
        raise InputError

    if check_if_user_is_channel_member(auth_user_id, channel_id) == True:
        raise InputError 

    user_detail = auth_user_id_check(auth_user_id)
    if user_detail['is_global_owner'] == 2:
        if check_if_channel_is_public_or_private(channel_id) == False: 
            raise AccessError
        

    
    All_channels_storage = data_store.get()
    channel_to_join = channel_id_check(channel_id)
    access_user = auth_user_id_check(auth_user_id)

    for channel in All_channels_storage['channels']:
        if channel['channel_id'] == channel_to_join['channel_id']:
            channel['all_members'].append(auth_user_id)

    return {}

