import pytest
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.channels import channels_create_v1, channels_list_v1
from src.channel import channel_join_v1, channel_leave_v2, channel_add_owner_v2, channel_details_v1
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

@pytest.fixture
def user3():
    dummy_user_3 = auth_register_v1('dummy333my@gmail.com', 'yessiaf', 'Pra', 'Beckham')
    return dummy_user_3

def test_invalid_token(clear, channel1, user2):
    with pytest.raises(AccessError):
        assert channel_add_owner_v2("random_token", channel1['channel_id'], user2['auth_user_id'])

def test_invalid_user(clear, user1, channel1, user2):
    with pytest.raises(InputError):
        assert channel_add_owner_v2(user1['token'], channel1['channel_id'], -1)

def test_existing_owner(clear, user1, channel1, user2):
    channel_join_v1(user2['token'], channel1['channel_id']) 
    channel_add_owner_v2(user1['token'], channel1['channel_id'], user2['auth_user_id'])
    with pytest.raises(InputError):
        assert channel_add_owner_v2(user1['token'], channel1['channel_id'], user2['auth_user_id'])

def test_invalid_channel_id(clear, user1, user2):
    with pytest.raises(InputError):
        assert channel_add_owner_v2(user1['token'], -1, user2['auth_user_id'])

def test_non_member(clear, user1, user2, channel1, user3):
    channel_join_v1(user2['token'], channel1['channel_id']) 
    with pytest.raises(InputError):
        assert channel_add_owner_v2(user2['token'], channel1['channel_id'], user3['auth_user_id'])

def test_non_global_member_non_owner(clear, user1, channel1, user2, user3):
    channel_join_v1(user2['token'], channel1['channel_id']) 
    channel_join_v1(user3['token'], channel1['channel_id']) 
    with pytest.raises(AccessError):
        assert channel_add_owner_v2(user2['token'], channel1['channel_id'], user3['auth_user_id'])


def test_channel_addowner_works(clear, user1, user2, channel1):
    channel_join_v1(user2['token'], channel1['channel_id']) 
    channel_add_owner_v2(user1['token'], channel1['channel_id'], user2['auth_user_id'])
    data = channel_details_v1(user1['token'], channel1['channel_id'])
    assert data == {'name': 'channel1', 'is_public': True, 'owner_members': [{'u_id': 1, 'email': 'dummyuser1@gmail.com', 'name_first': 'Alpha', 'name_last': 'AA', 'handle_str': 'alphaaa'}, 
            {'u_id': 2, 'email': 'dummy2my@gmail.com', 'name_first': 'Jack', 'name_last': 'Grealish', 'handle_str': 'jackgrealish'}], 
            'all_members': [{'u_id': 1, 'email': 'dummyuser1@gmail.com', 'name_first': 'Alpha', 'name_last': 'AA', 'handle_str': 'alphaaa'}, 
            {'u_id': 2, 'email': 'dummy2my@gmail.com', 'name_first': 'Jack', 'name_last': 'Grealish', 'handle_str': 'jackgrealish'}]}