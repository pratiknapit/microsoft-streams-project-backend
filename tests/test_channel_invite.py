import pytest
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.channels import channel_create_v1
from src.channel import channel_invite_v1


# Dummy case created for testing of different parts of channel_invite_v1
dummy = auth_register_v1('smartdummy@gmail.com', 'password', 'smart', 'dummy')
bad_dummy = auth_register_v1('bad_dummy@gmail.com', 'yessword', 'bad', 'dummy')
good_dummy = auth_register_v1('baddummy@gmail.com', 'passsssword', 'good', 'dummy')
# Creating a new channel with the first member as an owner and member
bad_dummy_channel = channel_create_v1(bad_dummy['auth_user_id'], 'new_bad_dummy_channel', True) # true means public channel


def test_channel_invite_invalid():
    with pytest.raises(AccessError):
        # Correct auth_user_id but the inviter is not a member of the channel 
        channel_invite_v1(dummy['auth_user_id'], bad_dummy_channel['channel_id'], bad_dummy['auth_id'])
        # incorrect auth_user id since user not registered, channel_id is wrong but u_id is correct
        channel_invite_v1(dumba['auth_user_id'], bad_duma['channel_id'], dummy['auth_id'])
        # Incorrect auth_user_id (not registered) and incorrect u_id but correct channel_id
        channel_invite_v1(dumba['auth_user_id'], bad_dummy_channel['channel_id'], domba['auth_id'])
        # Incorrect auth_user_id (not registered) but correct channeL_id and u_id
        channel_invite_v1(gooba['auth_user_id'], bad_dummy_channel['channel_id'], dummy['auth_id'])
        # Everything is incorrect
        channel_invite_v1(dumba['auth_user_id'], bad_duma['channel_id'], goomba['auth_id'])



    with pytest.raises(InputError):
        #correct  auth_user_id and channel id but incorrect user id
        channel_invite_v1(bad_dummy['auth_user_id'], bad_dummy_channel['channel_id'], dumdum['auth_id'])
        #correct auth_user_id but wrong channel_id and wrong u_id
        channel_invite_v1(bad_dummy['auth_user_id'], bad_duma_channel['channel_id'], dumdum['auth_id'])
        # correct auth_user_id and u_id but incorrect channel_id
        channel_invite_v1(bad_dummy['auth_user_id'], bad_duma_channel['channel_id'], dummy['auth_id'])



        


def test_channel_invite_valid():
    channel_invite_v1(channel_id_bad_dummy['channel_id'], good_dummy['u_id'])
    assert(channel_invite_v1(bad_dummy['auth_user_id'], bad_dummy_channel['channel_id'], dummy['auth_id']))
        