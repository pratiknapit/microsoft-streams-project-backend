import pytest

from src.error import InputError
from src.channels import channels_create_v1, channels_list_v1
from src.other import clear_v1

#The first part of the testing is to test if the inputs are valid. 

#we might have to check if the user id that is inputted is valid 

"""
def test_channels_create_invalid_user_id(): #user id is invalid
    clear_v1()
    with pytest.raises(InputError): #invalid auth user id. 
        channels_create_v1("kjeklfjkfgksjfkdsajfasdkjfk", "name", "is_public")
"""

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

#The tests below actually check if the function works and does what we want it to do.
#That is creating the channel and adding to the data base.

def test_channels_create():
    clear_v1()
    channel_return = channels_create_v1("ConorMcgregor", "School", "yes")
    channel_id1 = channel_return['channel_id'] #this will just return the channel id
    
    channel_list = channels_list_v1("ConorMcgregor") #this should return a list of channels
    for channel in channel_list['channels']:
        if channel['name'] == "School":
            channel_id2 = channel['channel_id']
        else:
            channel_id2 = 100
    
    assert channel_id1 == channel_id2
            
    
            
    









