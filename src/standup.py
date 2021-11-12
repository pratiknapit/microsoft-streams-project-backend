from json import load 
from src.data_store import auth_user_id_check, channel_id_check, data_store, token_to_user_id, save_data
from src.data_store import is_valid_token
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from os import access 
from datetime import datetime, timezone
import threading
import time
from src.error import AccessError, InputError

from src.message import message_send 

def standup_start_v1(token, channel_id, length): 
    data = data_store.get() 

    #token check 
    if not is_valid_token(token):
        raise AccessError(description="not an authorised user")

    #channel id check 

    if not channel_id_check(channel_id):
        raise InputError(description='channel_id does not refer to a valid channel')

    #standup active check 
    if standup_active_v1(token, channel_id)['is_active'] == True:
        raise InputError("an active standup is currently running in the channel")

    #check if length is negative 

    if length <= 0: 
        raise InputError("length is a negative integer")
    
    #check if token user is part of the channel.

    channel = channel_id_check(channel_id)
    channel['standup']['is_active'] = True
    channel['standup']['time_finish'] = datetime.now().replace(tzinfo=timezone.utc).timestamp() + length
    channel['standup']['messages'] = ""
    channel['standup']['user_id'] = token_to_user_id(token) 

    global t

    t = threading.Timer(length, standup_end, args=[token, channel_id, data])
    t.start()

    save_data(data)

    return {'time_finish': channel['standup']['time_finish']}


def standup_end(*args):

    channel = channel_id_check(args[1])

    message = channel['standup']['messages']

    if len(message) != 0:
        message_send(args[0], args[1], message) #at the end of the timer, send all the queued msgs

    data = data_store.get()

    channel['standup']['is_active'] = False
    channel['standup']['time_finish'] = None 

    save_data(data)
    
    global t 
    t.cancel()

    return {}


def standup_active_v1(token, channel_id):

    data = data_store.get()

    #check valid token
    if not is_valid_token(token):
        raise AccessError(description="not an authorised user")

    #check if channel_id is an int type variable 

    #check valid channel id
    if not channel_id_check(channel_id):
        raise InputError(description='channel_id does not refer to a valid channel')

    channel = channel_id_check(channel_id)
    if channel['standup']['is_active'] == False:
        save_data(data) 
        return {
            'is_active': False,
            'time_finish': None
        }
    else: 
        save_data(data) 
        return {
            'is_active': True,
            'time_finish': channel['standup']['time_finish']
        }

def standup_send_v1(token, channel_id, message):

    data = data_store.get()

    #check valid token
    if not is_valid_token(token):
        raise AccessError(description="not an authorised user")

    #check if channel_id is an int type variable 

    #check valid channel id
    if not channel_id_check(channel_id):
        raise InputError(description='channel_id does not refer to a valid channel')


    if len(message) > 1000: 
        raise InputError("Message is longer than 1000 characters.")
    
    if standup_active_v1(token, channel_id)['is_active'] == False:
        raise InputError("No active standup")
    
    channel = channel_id_check(channel_id)

    user_id = token_to_user_id(token) 
    user_handle = auth_user_id_check(user_id)['handle_str']

    if len(channel['standup']['messages']) == 0: #empty string 
        channel['standup']['messages'] = f"{user_handle}: {message}"
    else: 
        channel['standup']['messages'] = channel['standup']['messages'] + '\n' f"{user_handle}: {message}"

    save_data(data) 

    return {} 


if __name__ == '__main__':
    dummy_user_1 = auth_register_v1('dummyuser1@gmail.com', 'passworddd', 'Alpha', 'AA')
    channel_user1 = channels_create_v1(dummy_user_1['token'], "channel1", True)
    standup_start_v1(dummy_user_1['token'], channel_user1['channel_id'], 1)
    
