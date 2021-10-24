import pytest
from src.auth import auth_register_v1 
from src.error import InputError, AccessError  
from src.channel import channel_details_v1 
from src.channels import channels_create_v1, channels_list_v1
from src.other import clear_v1

@pytest.fixture
def user1():
    dummy_user_1 = auth_register_v1('dummyuser1@gmail.com', 'passworddd', 'Alpha', 'AA')
    return dummy_user_1

@pytest.fixture
def user2():
    dummy_user_2 = auth_register_v1('dummy2my@gmail.com', 'random', 'Jack', 'Grealish')
    return dummy_user_2

@pytest.fixture
def channel1(user1):
    channel_user1 = channels_create_v1(user1['token'], "channel1", True)
    return channel_user1

@pytest.fixture
def clear():
    clear_v1()

def test_invalid_token():
    clear_v1()
    dummy_user_1 = auth_register_v1('dummyuser1@gmail.com', 'passworddd', 'Alpha', 'AA')
    channel_user1 = channels_create_v1(dummy_user_1['token'], "channel1", True)
    with pytest.raises(AccessError):
        assert channel_details_v1("random_token", channel_user1['channel_id'])

def test_if_user_is_channel_member(clear, user1, channel1):
    user_2 = auth_register_v1('dummy2my@gmail.com', 'random', 'Jack', 'Grealish')
    with pytest.raises(AccessError):
        assert channel_details_v1(user_2['token'], channel1['channel_id'])



def test_channel_invalid(clear, user1, channel1):
    with pytest.raises(InputError):
        assert channel_details_v1(user1['token'], 872483)

def test_invalid_channel_details(clear):
    clear_v1()
    dummy_user_2 = auth_register_v1('dummyuser2@gmail.com', 'yessword', 'Beta', 'BB')
    dummy_user_3 = auth_register_v1('dummyuser3@gmail.com', 'passsssword', 'Ceal', 'CC')
    dummy_user_2_channel = channels_create_v1(dummy_user_2['token'], 'dummy_user_2_channel', True)

def test_valid_channel_details(clear):
    clear_v1()
    dummy_user_2 = auth_register_v1('dummyuser2@gmail.com', 'yessword', 'Beta', 'BB')
    dummy_user_3 = auth_register_v1('dummyuser3@gmail.com', 'passsssword', 'Ceal', 'CC')
    dummy_user_2_channel = channels_create_v1(dummy_user_2['token'], 'dummy_user_2_channel', True)
    dummy_user_2_list_channel = channels_list_v1(dummy_user_2['token'])

    channel = channel_details_v1(dummy_user_2['token'], dummy_user_2_channel['channel_id'])

    value = False
    if channel['name'] == 'dummy_user_2_channel':
        if channel['is_public'] == True:
            for member in channel['owner_members']:
                if member['u_id'] == dummy_user_2['auth_user_id']:
                    for mem in channel['all_members']:
                        if mem['u_id'] == dummy_user_2['auth_user_id']:
                            value = True 
    else:
        value = False
    
    assert (value == True)
    