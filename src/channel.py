from src.error import InputError, AccessError
from src.data_store import channel_id_check, auth_user_id_check, check_if_user_is_channel_member
from src.data_store import auth_user_id_check
from src.data_store import data_store

def channel_invite_v1(auth_user_id, channel_id, u_id):
    # check if corect channel id otherwise return Input error (not valid channel)
    if not channel_id_check(channel_id): 
            raise InputError

    # check if user id correct otherwise return Input Error (not valid  user id or user 
    # already in channel)
    if not auth_user_id_check(u_id):
            raise InputError

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
            channel["all_members"].append(user["auth_user_id"])
    '''user['user_list_channel'].append(channel_id)'''
    data_store.set(data)
    return {}


def channel_details_v1(auth_user_id, channel_id):
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
        raise AccessError                            # User not exist at all

    if channel_id_check(channel_id) == False:                              # Channel does not exist
        raise InputError

    if check_if_user_is_channel_member(auth_user_id, channel_id) == False: # auth_user_id is not a member of channel
        raise AccessError

    total_messages = 0   
    store = data_store.get()
    
    for i in store['Messages']:
            if i['channel_id'] == channel_id:
                total_messages += 1
    
    if start > total_messages:                                      # Start is greater than the total number of messages in channel
        raise InputError

    dict_start = {
        'messages':[]
    }

    dict_finish = {
        'messages':[]
    }
    dict_start = data_store.get()['Messages']
   
    counter = 0
    if len(dict_start) != 0:
        for message in reversed(dict_start):
  
            if int(message['channel_id']) == int(channel_id):
             
                if counter >= start:
                  
                    dict = {
                        'message_id': message['message_id'],
                        'u_id': message['auth_user_id'],
                        'message': message['message'],
                        'time_created': message['time_created'].replace(tzinfo=timezone.utc).timestamp(),
                        
                    }
                    dict_finish['messages'].append(dict)    
                counter = counter + 1
            if counter >= 50:
                counter = -1
                break
    
    dict_finish['start'] = start
    dict_finish['end'] = counter
    return dict_finish
'''

def channel_join_v1(auth_user_id, channel_id):
    return {
    }
