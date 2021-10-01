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
        channels_create_v1(12345, "", True)

def test_channels_create_max_invalid_name(): 
    clear_v1()
    with pytest.raises(InputError): #length of name is more than 20
        channels_create_v1(12345, "channel24istheworstchannelEver", False)

def test_channels_create_wrong_public_input():
    clear_v1()
    with pytest.raises(InputError):
        channels_create_v1(12345, "Sports", "Not private")

#The tests below actually check if the function works and does what we want it to do.
#That is creating the channel and adding to the data base.

def test_channels_create():
    clear_v1()
    channel_id = channels_create_v1(12345, "School", True)  #this will just return the channel id
    channel_list = channels_list_v1(12345) #this should return a list of channels
    for channel in channel_list['channels']:
        if channel['channel_id'] == channel_id['channel_id'] and channel['name'] == "School":
            result = True

    assert (result == True)
            

def test_multiple_channels_create():
    clear_v1()
    channel_1 = channels_create_v1(12345, "School", True) #this shud return
    channel_2 = channels_create_v1(12345678, "Play", True)
    channel_3 = channels_create_v1(12345, "Tutoring", True) #this shud return
    channel_4 = channels_create_v1(12345, "Yellow", False) #this shud return

    channel_list = channels_list_v1(12345)
    
    result = 0
    for channel in channel_list['channels']:
        if channel['channel_id'] == channel_1['channel_id'] and channel['name'] == "School":
            result = result + 1
        elif channel['channel_id'] == channel_3['channel_id'] and channel['name'] == "Tutoring":
            result = result + 1
        elif channel['channel_id'] == channel_4['channel_id'] and channel['name'] == "Yellow":
            result = result + 1
        else:
            pass
    #result should return 3 
    assert (result == 3)
        
#testing if channels create works using channel_list_all


#testing if channels create works using channel_join


#testing if channels create works using channels_invite 

#testing if channels create works using channel details 











