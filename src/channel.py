from src.error import InputError, AccessError
from src.data_store import channel_id_check, user_id_check, check_if_user_is_channel_member
from src.data_store import data_store

def channel_invite_v1(auth_user_id, channel_id, u_id):
    # check if corect channel id otherwise return Input error (not valid channel)
    if not channel_id_check(channel_id): 
            raise InputError

    # check if user id correct otherwise return Input Error (not valid  user id or user 
    # already in channel)
    if not user_id_check(u_id):
            raise InputError

    # check when channel id corect but user(who invited) not part of channel
    if not check_if_user_is_channel_member(auth_user_id, channel_id):
            raise AccessError

    if auth_user_id == u_id:
        raise AccessError
    
    data = data_store.get()
    user = user_id_check(u_id)
    for channel in data["channels"]:
        if channel["channel_id"] == channel_id:
            channel["all_members"].append({"u_id": user["u_id"], "name_first": user['name_first'], "name_last": user["name_last"]})
    user['user_list_channel'].append(channel_id)
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

def channel_messages_v1(auth_user_id, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_join_v1(auth_user_id, channel_id):
    return {
    }
