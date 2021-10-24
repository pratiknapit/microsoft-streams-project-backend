import pytest
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.channels import channels_create_v1, channels_list_v1
from src.channel import channel_join_v1, channel_leave_v2
from src.other import clear_v1

@pytest.fixture
def clear():
    clear_v1()

@pytest.fixture
def user1():
    dummy_user_1 = auth_register_v1('dummyuser1@gmail.com', 'passworddd', 'Alpha', 'AA')
    return dummy_user_1

@pytest.fixture
def channel1(user1):
    channel_user1 = channels_create_v1(user1['token'], "channel1", True)
    return channel_user1

@pytest.fixture
def channel2(user1):
    channelpriv_user1 = channels_create_v1(user1['token'], "channelPriv", False)
    return channelpriv_user1

@pytest.fixture
def user2():
    dummy_user_2 = auth_register_v1('dummy2my@gmail.com', 'random', 'Jack', 'Grealish')
    return dummy_user_2

def test_invalid_token(clear, channel1):
    with pytest.raises(AccessError):
        assert channel_leave_v2("random_token", channel1['channel_id'])

def test_invalid_channel_id(clear, user1):
    with pytest.raises(InputError):
        assert channel_leave_v2(user1['token'], -1)

def test_non_member(clear, user1, user2, channel1):
    with pytest.raises(AccessError):
        assert channel_leave_v2(user2['token'], channel1['channel_id'])

def test_channel_leave_works(clear, user1, user2, channel1):
    data = channels_list_v1(user1['token'])
    channel_join_v1(user2['token'], channel1['channel_id'])
    channel_leave_v2(user2['token'], channel1['channel_id'])
    data_new = channels_list_v1(user1['token'])
    assert data == data_new

