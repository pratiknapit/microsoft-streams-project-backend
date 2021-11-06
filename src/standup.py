from json import load 
from src.data_store import channel_id_check, data_store, token_to_user_id, save_data
from os import access 
from datetime import datetime, timezone
import threading
from src.error import AccessError, InputError

from src.message import message_send 

def standup_start_v1(token, channel_id, length): 
    data = data_store.get() 

    #token check 

    #channel id check 

    #standup active check 
    if standup_active_v1(token, channel_id)['is_active'] == True:
        raise InputError("Standup already in progress")

    channel = channel_id_check(channel_id)
    channel['standup']['is_active'] = True
    channel['standup']['time_finish'] = datetime.now().replace(tzinfo=timezone.utc).timestamp() + length
    channel['standup']['messages'] = ''
    channel['standup']['user_id'] = token_to_user_id(token) 

    global t

    t = threading.Timer(length, standup_end, args=[token, channel_id, data])
    t.start()

    save_data(data)

    return; 


def standup_end(*args):

    channel = channel_id_check[args[1]]

    message = channel['standup']['messages']

    message_send(args[0], args[1], message)

    data = data_store.get()

    channel['standup']['is_active'] = False
    channel['standup']['time_finish'] = None 

    save_data(data)
    
    global t 
    t.cancel()


def standup_active_v1(token, channel_id):

    data = data_store.get()

    #check valid token

    #check if channel_id is an int type variable 

    #check valid channel id

    channel = channel_id_check(channel_id)

    if channel['standup']['is_active'] == False:
        return {
            'is_active': False,
            'time_finish': None
        }
    else: 
        return {
            'is_active': True,
            'time_finish': channel['standup']['time_finish']
        }

def standup_send_v1(token, channel_id, message):

    data = data_store.get()

    #check valid token

    #check if channel_id is an int type variable 

    #check valid channel id

    if len(message) > 1000: 
        raise InputError("Message is longer than 1000 characters.")
    
    if not standup_active_v1(token, channel_id)['is_active']:
        raise InputError("No active standup")
    
    channel = channel_id_check(channel_id)

    channel['standup']['messages'] = channel['standup']['messages'] + ' ' + message

    save_data(data) 

    return {} 
