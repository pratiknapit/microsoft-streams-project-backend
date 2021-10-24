import pytest
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.channel import channel_join_v1
from src.channel import channel_details_v1
from src.other import clear_v1
from src.data_store import auth_user_id_check
'''
dummy_user_1 = auth_register_v1('dummyuser1@gmail.com', 'passworddd', 'Alpha', 'AA')
dummy_user_2 = auth_register_v1('dummyuser2@gmail.com', 'yessword', 'Beta', 'BB')
dummy_user_3 = auth_register_v1('dummyuser3@gmail.com', 'passsssword', 'Ceal', 'CC')

dummy1_id = dummy_user_1['auth_user_id']
dummy2_id = dummy_user_2['auth_user_id']

dummy_user_2_channel = channels_create_v1(dummy_user_2['auth_user_id'], 'dummy_user_2_channel', True)
'''

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

@pytest.fixture
def clear():
    clear_v1()

def test_invalid_token(channel1):
    clear_v1()
    with pytest.raises(AccessError):
        assert channel_join_v1("random_token", channel1['channel_id'])

def test_non_global_owner(clear, user1, user2, channel2):
    with pytest.raises(AccessError):
        assert channel_join_v1(user2['token'], channel2['channel_id'])


def test_channel_join_invalid_id():
    clear_v1()
    dummy_user_2 = auth_register_v1('dummyuser2@gmail.com', 'yessword', 'Beta', 'BB')
    with pytest.raises(InputError):
        assert channel_join_v1(dummy_user_2['token'], 123123123)

def test_channel_join_private_channel():
    clear_v1()
    dummy_user_2 = auth_register_v1('dummyuser2@gmail.com', 'yessword', 'Beta', 'BB')
    dummy_user_3 = auth_register_v1('dummyuser3@gmail.com', 'passsssword', 'Ceal', 'CC')
    dummy_user_2_channel = channels_create_v1(dummy_user_2['token'], 'dummy_user_2_channel', False)

    with pytest.raises(AccessError):
        assert channel_join_v1(dummy_user_3['token'], dummy_user_2_channel['channel_id'])

def test_user_is_already_member():
    clear_v1()
    dummy_user_2 = auth_register_v1('dummyuser2@gmail.com', 'yessword', 'Beta', 'BB')
    dummy_user_2_channel = channels_create_v1(dummy_user_2['token'], 'dummy_user_2_channel', False)

    with pytest.raises(InputError):
        assert channel_join_v1(dummy_user_2['token'], dummy_user_2_channel['channel_id'])

def test_priv_chan_join():
    clear_v1()
    dummy_user_1 = auth_register_v1('dummyuser1@gmail.com', 'asfdasdf', 'Pratik', 'Napit')
    dummy_user_2 = auth_register_v1('dummyuser2@gmail.com', 'yessword', 'Beta', 'BB')
    dummy_user_1_channel = channels_create_v1(dummy_user_1['token'], 'dummy_user_1_channel', False)

    with pytest.raises(AccessError):
        assert channel_join_v1(dummy_user_2['token'], dummy_user_1_channel['channel_id'])


def test_if_joining_works():
    clear_v1()
    dummy_user_2 = auth_register_v1('dummyuser2@gmail.com', 'yessword', 'Beta', 'BB')
    dummy_user_3 = auth_register_v1('dummyuser3@gmail.com', 'passsssword', 'Ceal', 'CC')
    dummy_user_2_channel = channels_create_v1(dummy_user_2['token'], 'dummy_user_2_channel', True)

    
    channel_join_v1(dummy_user_3['token'],  dummy_user_2_channel['channel_id'])
    channel_data = channel_details_v1(dummy_user_2['token'], dummy_user_2_channel['channel_id'])
    value = False

    for member in channel_data['all_members']:
        if member['u_id'] == dummy_user_3['auth_user_id']:
            value = True

    assert (value == True)

