import pytest
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.channel import channel_invite_v1, channel_details_v1
from src.other import clear_v1

@pytest.fixture
def dummy_cases():
    # Dummy case created for testing of different parts of channel_invite_v1
    dummy_user_1 = auth_register_v1('dummyuser1@gmail.com', 'passworddd', 'Alpha', 'AA')
    dummy_user_2 = auth_register_v1('dummyuser2@gmail.com', 'yessword', 'Beta', 'BB')
    dummy_user_3 = auth_register_v1('dummyuser3@gmail.com', 'passsssword', 'Ceal', 'CC')
    # Creating a new channel with the first member as an owner and member
    dummy_user_2_channel = channels_create_v1(dummy_user_2['auth_user_id'], 'dummy_user_2_channel', True) # true means public channel
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

def test_channel_invite_user_invalid(clear, dummy_cases):
    with pytest.raises(AccessError):
        # Correct auth_user_id but the inviter is not a member of the channel 
        channel_invite_v1(dummy_cases['dummy_user_1']['auth_user_id'],
        dummy_cases['dummy_user_2_channel']['channel_id'], 
        dummy_cases['dummy_user_2']['auth_user_id'])

def test_channel_invite_channel_invalid(clear, dummy_cases):
    pass

def test_channel_invite_no_user_invalid(clear, dummy_cases):
    pass

def test_channel_invite_self_invalid(clear, dummy_cases):
    pass

def test_channel_invite_no_user_in_channel_invalid(clear, dummy_cases):
    pass

def test_channel_invite_already_in_channel_invalid(clear, dummy_cases):
    pass











'''
def test_channel_invite_invalid():
    with pytest.raises(AccessError):
        # Correct auth_user_id but the inviter is not a member of the channel 
        channel_invite_v1(dummyy['auth_user_id'], bad_dummy_channel['channel_id'], bad_dummy['auth_user_id'])
        # incorrect auth_user id since user not registered, channel_id is wrong but u_id is correct
'''
        
''' 
    with pytest.raises(InputError):
        #correct  auth_user_id and channel id but incorrect user id
        channel_invite_v1(bad_dummy['auth_user_id'], bad_dummy_channel['channel_id'], dumdum['auth_id'])
        #correct auth_user_id but wrong channel_id and wrong u_id
        channel_invite_v1(bad_dummy['auth_user_id'], bad_duma_channel['channel_id'], dumdum['auth_id'])
        # correct auth_user_id and u_id but incorrect channel_id
        channel_invite_v1(bad_dummy['auth_user_id'], bad_duma_channel['channel_id'], dummy['auth_id'])
        
        channel_invite_v1(dumba['auth_user_id'], bad_duma['channel_id'], dummy['auth_id'])
        # Incorrect auth_user_id (not registered) and incorrect u_id but correct channel_id
        channel_invite_v1(dumba['auth_user_id'], bad_dummy_channel['channel_id'], domba['auth_id'])
        # Incorrect auth_user_id (not registered) but correct channeL_id and u_id
        channel_invite_v1(gooba['auth_user_id'], bad_dummy_channel['channel_id'], dummy['auth_id'])
        # Everything is incorrect
        channel_invite_v1(dumba['auth_user_id'], bad_duma['channel_id'], goomba['auth_id'])
'''

#testing functionality
'''
def test_channel_invite_valid():    
    empty = channel_invite_v1(bad_dummy['auth_user_id'], bad_dummy_channel['channel_id'], good_dummy['auth_user_id']) 
    bad_dummy_channel_details = channel_details_v1(bad_dummy['auth_user_id'], bad_dummy_channel['channel_id'])
  
    valid = False

    for member in bad_dummy_channel_details['all_members']:
        if member == good_dummy['auth_user_id']:
            valid = True
        else:
            valid = False
    assert (valid == True)


def test_channel_invite_invalid():

    empty = channel_invite_v1(bad_dummy['auth_user_id'], bad_dummy_channel['channel_id'], dummyy['auth_user_id']) 
    bad_dummy_channel_details = channel_details_v1(bad_dummy['auth_user_id'], bad_dummy_channel['channel_id'])
  
    valid = False

    for member in bad_dummy_channel_details['all_members']:
        if member == good_dummy['auth_user_id']:
            valid = True
        else:
            valid = False
    assert (valid == False)

        
channel_invite_v1(dumba['auth_user_id'], bad_duma['channel_id'], dummy['auth_id'])
# Incorrect auth_user_id (not registered) and incorrect u_id but correct channel_id
channel_invite_v1(dumba['auth_user_id'], bad_dummy_channel['channel_id'], domba['auth_id'])
# Incorrect auth_user_id (not registered) but correct channeL_id and u_id
channel_invite_v1(gooba['auth_user_id'], bad_dummy_channel['channel_id'], dummy['auth_id'])
# Everything is incorrect
channel_invite_v1(dumba['auth_user_id'], bad_duma['channel_id'], goomba['auth_id'])
'''