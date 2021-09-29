import pytest

from src.error import InputError
from src.channels import channels_create_v1, channels_list_v1
from src.other import clear_v1



#we might have to check if the user id that is inputted is valid 

def test_channels_create_invalid_user_id(): #user id is invalid
    clear_v1()
    with pytest.raises(InputError): #invalid auth user id. 
        channels_create_v1("kjeklfjkfgksjfkdsajfasdkjfk", "name", "is_public")

def test_channels_create_min_invalid_name(): 
    clear_v1()
    with pytest.raises(InputError): #length of name is less than 1 
        channels_create_v1("pratiknapit", "", "is_public")

def test_channels_create_max_invalid_name(): 
    clear_v1()
    with pytest.raises(InputError): #length of name is more than 20
        channels_create_v1("pratiknapit", "channel24istheworstchannelEver", "is_public")

"""
def test_channels_create_invalid_ispublic(): 
    clear_v1()
    with pytest.raises(InputError): #is_public is invalid --> needs to be either TRUE or FALSE
        channels_create_v1("pratiknapit", "BestChannel", "maybe")
"""

#the test below will tests if channel_create_v1 works and if the channel has been added to the data store
def test_channels_create_works(): 
    clear_v1()
    channel_return = channels_create_v1("auth_user_id", "name", "is_public")
    channel_id1 = channel_return['channel_id']

    channel_list = channels_list_v1("auth_user_id") #this should return a list of channels
    for channel in channel_list:
        if channel['owners'] == "auth_user_id":
            channel_id2 = channel['channel_id']
        else:
            pass

    assert channel_id1 == channel_id2
            
    
            
    









