from src.data_store import data_store, user_channels, add_channel
from src.error import InputError


def channels_list_v1(auth_user_id):
    
    #check user id -- need to create function in data_store
    """
    if user_id_check(auth_user_id) == False:
        raise Input Error
    """
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



def channels_listall_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }



def channels_create_v1(auth_user_id, name, is_public):

    #check user id -- need to create function in data_store

    if len(name) < 1 or len(name) > 20:
        raise InputError

    added_channel = add_channel(auth_user_id, name, is_public) #i need a function to add channel
    
    """
    if user_id_check(auth_user_id) == False:
        raise Input Error
    """

    """
    stored_data = data_store.get() #this will retrieve the initial object
    channels = stored_data['channels']
    print(channels) #this will print a list of all the channels
    """
    return added_channel
    """
    return { #here we return dictionary containing channel of the recently added chanel 
        'channel_id': added_channel['channel_id']
    }
    """

if __name__ == '__main__':
    print(channels_create_v1("1233241324", "School", "yes"))
    print(channels_create_v1("1233241324", "ChannelForSport", "yes"))
    print(channels_create_v1("1233241324", "ChannelForFriends", "no"))
    print(channels_create_v1('345', 'FavChannel', "yes"))
    print(channels_list_v1("1233241324"))

