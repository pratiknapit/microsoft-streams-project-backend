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
    dummy_user_3 = auth_register_v1('dummyuser3@gmail.com', 'passsssword', 'Ceal', 'CC')
    dummy_user_2_channel = channels_create_v1(dummy_user_2['token'], 'dummy_user_2_channel', False)

    with pytest.raises(InputError):
        assert channel_join_v1(dummy_user_2['token'], dummy_user_2_channel['channel_id'])

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

