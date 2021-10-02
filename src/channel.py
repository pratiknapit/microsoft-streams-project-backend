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
    channel_details_dictionary['owner_members'] = extract_channel_details['owner_members']
    channel_details_dictionary['all_members'] = extract_channel_details['all_members']
    
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

    if not auth_user_id_check(auth_user_id):
        raise AccessError

    if channel_id_check(channel_id) == False:
        raise InputError

    if check_if_user_is_channel_member(auth_user_id, channel_id) == True:
        raise InputError 

    if check_if_channel_is_public_or_private(channel_id) == False: 
        raise AccessError

    
    All_channels_storage = data_store.get()
    channel_to_join = channel_id_check(channel_id)
    access_user = auth_user_id_check(auth_user_id)

    for channel in All_channels_storage['channels']:
        if channel['channel_id'] == channel_to_join['channel_id']:
            channel['all_members'].append(auth_user_id)

    return {}

