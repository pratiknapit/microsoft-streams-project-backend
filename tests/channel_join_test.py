import pytest
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.channel import channel_join_v1
from src.channel import channel_details_v1
from src.other import clear_v1

steven = auth_register_v1("stevensmart@gmail.com", "password", "stevenn", "chenn")
steven_channel_id = channels_create_v1(steven['auth_user_id'], 'steven_channel', True)

jacky = auth_register_v1("jackysmart@gmail.com", "jackypassword", "jackyn", "zhun")
jacky_channel_id = channels_create_v1(jacky['auth_user_id'], 'jacky_channel', False)

def test_channel_join_invalid_id():
    clear_v1()
    with pytest.raises(InputError):
        assert channel_join_v1(steven['auth_user_id'], 123123123)

def test_channel_join_private_channel():
    clear_v1()
    with pytest.raises(AccessError):
        assert channel_join_v1(steven['auth_user_id'], jacky_channel_id['channel_id'])

def test_user_is_already_member():
    clear_v1()
    with pytest.raises(InputError):
        assert channel_join_v1(steven['auth_user_id'], steven_channel_id['channel_id'])

'''
def test_if_joining_works():
    
    channel_join_v1(steven['auth_user_id'], jacky_channel_id['channel_id'])
    channel_data = channel_details_v1(jacky['auth_user_id'], jacky_channel_id['channel_id'])
    value = False

    for mem in channel_data['all_members']:
        if mem == steven['auth_user_id']:
            value = True

    assert (value == True)
'''
