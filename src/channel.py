

from src.error import InputError, AccessError
def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

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

def channel_messages_v1(auth_user_id, channel_id, start):

    if channel_check(channel_id) == False:                          # Does not refer valid channel
        raise InputError

    if check_if_user_in_channel_member(, channel_id) == False: # Valid channel_id & auth_user_id not part of channel
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
                  
                    dict_to_app = {
                        'message_id':message['message_id'],
                        'u_id': message['user_id'],
                        'message': message['message'],
                        'time_created': message['time_created'].replace(tzinfo=timezone.utc).timestamp(),
                        
                    }
                    dict_finish['messages'].append(dict_to_app)    
                counter = counter + 1
            if counter >= 50:
                counter = -1
                break
    
    dict_finish['start'] = start
    dict_finish['end'] = counter
    return dict_finish


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
    return {
    }
