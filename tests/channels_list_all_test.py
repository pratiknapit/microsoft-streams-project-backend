import pytest

from src.error import InputError
from src.auth import auth_register_v1
from src.channels import channels_listall_v1, channels_create_v1 
from src.other import clear_v1


#Creating Dummy Variables
dummy1 = auth_register_v1("dummyvariable1@gmail.com", "dummy1pw", "dummy1", "variable")
dummy2 = auth_register_v1("dummyvariable2@gmail.com", "dummy2pw", "dummy2", "variable")
dummy1_id = dummy1['auth_user_id']
dummy2_id = dummy2['auth_user_id']

#Testing Errors
def test_user_is_valid(): 
    clear_v1()
    with pytest.raises(InputError): 
        channels_listall_v1(12345)

#Testing functionality
def test_channels_list_all_basic():
    clear_v1()
    channel_id1 = channels_create_v1(dummy1_id, "School", True)
    channel_id2 = channels_create_v1(dummy1_id, "Football", False)
    channel_list = channels_listall_v1(dummy1_id)

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


