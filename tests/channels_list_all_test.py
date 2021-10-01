import pytest

from src.error import InputError
from src.auth import auth_register_v1
from src.channels import channels_listall_v1, channels_create_v1 
from src.other import clear_v1

"""
def test_channels_create_invalid_user_id(): #user id is invalid
    clear_v1()
    with pytest.raises(InputError): #invalid auth user id. 
        channels_create_v1("kjeklfjkfgksjfkdsajfasdkjfk", "name", "is_public")
"""

def test_channels_list_all_basic():
    clear_v1()
    channel_id1 = channels_create_v1("12345", "School", True)
    channel_id2 = channels_create_v1("12345", "Football", False)
    User_id = auth_register_v1("pratiknapit7@gmail.com", "password", "Pratik", "Napit")
    channel_list = channels_listall_v1(User_id)

    result = 0
    for channel in channel_list['channels']:
        if channel['channel_id'] == channel_id1['channel_id'] and channel['name'] == "School":
            result += 1
        elif channel['channel_id'] == channel_id2['channel_id'] and channel['name'] == "Football":
            result += 1
        else:
            pass
    
    assert (result == 2)

#def test if channels list all works with different other functions in the iteration


