import pytest
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.channel import channel_messages_v1
from src.other import clear_v1

#creating clear and dummy cases fixtures to use in every test
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

def test_channel_messages_channel_id_invalid(clear, dummy_cases):
    # Channel id is incorrect (no such channel id exists)
    with pytest.raises(InputError):
        channel_messages_v1(dummy_cases['dummy_user_2']['auth_user_id'], -1, 39283)

def test_channel_messages_start_greater_than_total_messages_error(clear, dummy_cases):
    # Total messages is less than start (causes error)
    with pytest.raises(InputError):
        channel_messages_v1(dummy_cases['dummy_user_2']['auth_user_id'],
        dummy_cases['dummy_user_2_channel']['channel_id'], -1)

def test_channel_messages_auth_not_in_channel_invalid(clear, dummy_cases):
    # Correct auth_user_id but they are not a member of the channel
    with pytest.raises(AccessError):
        channel_messages_v1(dummy_cases['dummy_user_1']['auth_user_id'],
        dummy_cases['dummy_user_2_channel']['channel_id'], 100)

def test_channel_messages_functionality(clear, dummy_cases):
    assert channel_messages_v1(dummy_cases['dummy_user_2']['auth_user_id'],
    dummy_cases['dummy_user_2_channel']['channel_id'], 0) == {
        'message': [],
        'start': 0,
        'end':-1 
    }


    






