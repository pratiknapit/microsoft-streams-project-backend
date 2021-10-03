from src.data_store import data_store, is_public_check, user_channels, add_channel, user_all_channels
from src.data_store import auth_user_id_check 
from src.auth import auth_register_v1
from src.error import AccessError, InputError



"""
**********************************************************************
  
   channels_list_v1() should take in a user id and output a list of 
   channels that the user is a member of, regardless of if it is public 
   or private channel.

**********************************************************************
"""

def channels_list_v1(auth_user_id):
    

    if auth_user_id_check(auth_user_id) == False:
        raise AccessError
    
    
    #this will just return a dictionary that looks like the stub below
    return user_channels(auth_user_id) 

    """
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }
    """



"""
**********************************************************************
  
   channels_listall_v1() should take in a user id and output a list of 
   channels all channels that have been made in Streams, regardless of if 
   the authorised user is a member of the channel or not.

**********************************************************************
"""

def channels_listall_v1(auth_user_id):
    
    if auth_user_id_check(auth_user_id) == False:
        raise AccessError
    

    return user_all_channels(auth_user_id)
    
    """
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }
    """



"""
**********************************************************************
  
   channels_create_v1() should make a new channel and details and add
   it to the global variable/our data store with the user as an owner 
   and a member of the channel, as well as a channel id. 

**********************************************************************
"""

def channels_create_v1(auth_user_id, name, is_public):

    if auth_user_id_check(auth_user_id) == False:
        raise AccessError

    if len(name) < 1 or len(name) > 20:
        raise InputError


    if is_public_check(is_public) == False:
        raise InputError

    added_channel = add_channel(auth_user_id, name, is_public) #i need a function to add channel
   
    return { #here we return dictionary containing channel of the recently added chanel 
        'channel_id': added_channel['channel_id'],
        'name': added_channel['name']
    }




#this is a basic prints to see what our functions output.
if __name__ == '__main__':

    dummy_user_1 = auth_register_v1('dummyuser1@gmail.com', 'passworddd', 'Alpha', 'AA')
    dummy_user_2 = auth_register_v1('dummyuser2@gmail.com', 'yessword', 'Beta', 'BB')
    dummy_user_3 = auth_register_v1('dummyuser3@gmail.com', 'passsssword', 'Ceal', 'CC')

    print(channels_create_v1(dummy_user_1['auth_user_id'], 'dummy_user_1_channel', True))
    print("")
    print(channels_create_v1(dummy_user_2['auth_user_id'], 'dummy_user_2_channel', True))
    print("")
    print(channels_create_v1(dummy_user_3['auth_user_id'], 'dummy_user_3_channel', True))
    print("")
    print(channels_create_v1(dummy_user_1['auth_user_id'], 'dummy_user_4_channel', True))
    print("")
    print(channels_list_v1(dummy_user_1['auth_user_id']))
    print("")
    print(channels_listall_v1(dummy_user_1['auth_user_id'])) 
    

