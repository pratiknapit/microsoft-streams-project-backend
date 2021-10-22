import pytest
from src.error import InputError, AccessError
from src.auth import auth_login_v1, auth_register_v1
from src.channels import channels_create_v1
from src.channel import channel_invite_v1, channel_details_v1, channel_join_v1
from src.other import clear_v1

#creating clear and dummy cases fixtures to use in every test
"""
@pytest.fixture
def dummy_cases():
    # Dummy case created for testing of different parts of channel_invite_v1
    dummy_user_1 = auth_register_v1('dummyuser1@gmail.com', 'passworddd', 'Alpha', 'AA')
    dummy_user_2 = auth_register_v1('dummyuser2@gmail.com', 'yessword', 'Beta', 'BB')
    dummy_user_3 = auth_register_v1('dummyuser3@gmail.com', 'passsssword', 'Ceal', 'CC')

    # Creating a new channel with the first member as an owner and member
    dummy_user_2_channel = channels_create_v1(dummy_user_2['token'], 'dummy_user_2_channel', True) # true means public channel
    combined_data = {
        "dummy_user_1": dummy_user_1,
        "dummy_user_2": dummy_user_2,
        "dummy_user_3": dummy_user_3,
        "dummy_user_2_channel": dummy_user_2_channel,
    }
    return combined_data 

@pytest.fixture
def clear():
    clear_v1()


def test_channel_invite_channel_invalid(clear, dummy_cases):
    # channel id is incorrect (no such channel id exists)
    with pytest.raises(InputError):
        assert channel_invite_v1(dummy_cases['dummy_user_2']['token'], 23455,
        dummy_cases['dummy_user_1']['auth_user_id'])


def test_channel_invite_incorrect_user_invalid(clear, dummy_cases):
    #user id is incorrect (no such user id exists)
    with pytest.raises(AccessError):
        channel_invite_v1(dummy_cases['dummy_user_2']['token'],
        dummy_cases['dummy_user_2_channel']['channel_id'], 
        0)

def test_channel_invite_auth_not_in_channel_invalid(clear, dummy_cases):
    with pytest.raises(AccessError):
        # Correct auth_user_id but the inviter is not a member of the channel
        # user 1 is not part of channel but they trying to create a channel invite for user 3
        channel_invite_v1(dummy_cases['dummy_user_1']['token'],
        dummy_cases['dummy_user_2_channel']['channel_id'], 
        dummy_cases['dummy_user_3']['auth_user_id'])

def test_channel_invite_already_in_channel_invalid(clear, dummy_cases):
    # user 1 is being added to channel in this test, 
    # next user 1 tries to inviter user 2 even though user 2 is already in channel
    channel_join_v1(dummy_cases['dummy_user_1']['token'], 
    dummy_cases['dummy_user_2_channel']['channel_id'])
    with pytest.raises(InputError):
        channel_invite_v1(dummy_cases['dummy_user_1']['token'],
        dummy_cases['dummy_user_2_channel']['channel_id'], 
        dummy_cases['dummy_user_2']['auth_user_id'])

#testing functionality of channel_invite
def test_channel_invite_valid(clear, dummy_cases):    
#    empty = channel_invite_v1(dummy_cases['dummy_user_2']['auth_user_id'], dummy_cases['dummy_user_2_channel']['channel_id'], dummy_cases['dummy_user_3']['auth_user_id']) 
    dummy_user_2_channel_details = channel_details_v1(dummy_cases['dummy_user_2']['token'], dummy_cases['dummy_user_2_channel']['channel_id'])
  
    valid = False

    for member in dummy_user_2_channel_details['all_members']:
        if member == dummy_cases['dummy_user_2']['auth_user_id']:
            valid = True
        else:
            valid = False
    assert (valid == False)

"""
@pytest.fixture
def user1():
    email = "test1email@gmail.com"
    password = "TestTest1"
    firstname = "firstname1"
    lastname = "lastname1"
    return auth_register_v1(email,password,firstname, lastname)

@pytest.fixture
def user2():
    email = "test2email@gmail.com"
    password = "TestTest2"
    firstname = "firstname2"
    lastname = "lastname2"
    return auth_register_v1(email,password,firstname, lastname)

@pytest.fixture
def channel_id():
    name = "Testchannel"
    user = auth_register_v1(
        "channelcreator@gmail.com", "TestTest", "channelcreator", "last")
    return channels_create_v1(user['token'], name, True)['channel_id']

@pytest.fixture
def clear():
    clear_v1()

def test_invalid_channel_id(clear, user1, user2):
    with pytest.raises(InputError):
        channel_invite_v1(user1['token'], 1, user2['auth_user_id'])
    clear_v1() 

def test_invalid_u_id(clear, channel_id):
    auth_user = auth_login_v1("channelcreator@gmail.com", "TestTest")
    user_id = auth_user['auth_user_id']
    with pytest.raises(InputError):
        channel_invite_v1(auth_user['token'], channel_id, user_id)
    clear_v1() 

def test_unauthorised_user(clear, user1, user2, channel_id):
    with pytest.raises(AccessError):
        channel_invite_v1(user2['token'], channel_id, user1['auth_user_id'])
    clear_v1() 

def test_all_valid(clear, user1, channel_id):
    auth_user = auth_login_v1("channelcreator@gmail.com", "TestTest")
    assert channel_invite_v1(auth_user['token'], channel_id, user1['auth_user_id']) == {}
    clear_v1() 

def test_user_already_in_channel(clear, user1, channel_id):
    auth_user = auth_login_v1("channelcreator@gmail.com", "TestTest")
    assert channel_invite_v1(auth_user['token'], channel_id, user1['auth_user_id']) == {}
    clear_v1()

def test_invalid_token(clear, user1, channel_id):
    with pytest.raises(AccessError):
        channel_invite_v1('bad.token.given', channel_id, user1['auth_user_id'])
    clear_v1()