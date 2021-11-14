import re
import pytest
from src.admin import admin_user_remove_v1
from src.data_store import check_existing_member
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.channel import channel_join_v1
from src.other import clear_v1

@pytest.fixture
def clear():
    clear_v1()

@pytest.fixture
def globaluser():
    dummy_user_1 = auth_register_v1('dummyuser1@gmail.com', 'passworddd', 'Alpha', 'AA')
    return dummy_user_1

@pytest.fixture
def channel1(globaluser):
    channel_user1 = channels_create_v1(globaluser['token'], "channel1", True)
    return channel_user1

@pytest.fixture
def channel2(globaluser):
    channelpriv_user1 = channels_create_v1(globaluser['token'], "channelPriv", False)
    return channelpriv_user1

@pytest.fixture
def user2():
    dummy_user_2 = auth_register_v1('dummy2my@gmail.com', 'random', 'Jack', 'Grealish')
    return dummy_user_2

@pytest.fixture
def user3():
    dummy_user_3 = auth_register_v1('dummy333my@gmail.com', 'yessiaf', 'Pra', 'Beckham')
    return dummy_user_3

def test_admin_remove(clear, channel1, globaluser, user2):

    channel_join_v1(user2['token'], channel1['channel_id'])

    assert check_existing_member(user2['auth_user_id'], channel1['channel_id']) == True

    re = admin_user_remove_v1(globaluser['token'], user2['auth_user_id'])
    assert re == {}
