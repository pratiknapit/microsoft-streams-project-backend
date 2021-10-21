import pytest
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.user import user_profile_setname_v1, user_profile_setemail_v1, user_profile_sethandle_v1
from src.channels import channels_create_v1
from src.other import clear_v1


@pytest.fixture
def dummy_cases():
    # Dummy case created for testing of different parts of channel_invite_v1
    dummy_user_2 = auth_register_v1('dummyuser2@gmail.com', 'yessword', 'Beta', 'BB')
    
    # Creating a new channel with the first member as an owner and member
    dummy_user_2_channel = channels_create_v1(dummy_user_2['auth_user_id'], 'dummy_user_2_channel', True) # true means public channel
    token = dummy_user_2['token']
    return token

@pytest.fixture
def clear():
    clear_v1()
    

def test_handle_already_taken(clear, dummy_cases):
    token = dummy_cases
    with pytest.raises(InputError):
        user_profile_sethandle_v1(token, "superman")

def test_handle_invalid(clear, dummy_cases):
    token = dummy_cases
    with pytest.raises(InputError):
        user_profile_sethandle_v1(token, "a")
    with pytest.raises(InputError):
        user_profile_sethandle_v1(token, "a"*99)

def test_valid_sethandle(clear, dummy_cases):
    token = dummy_cases
    res = user_profile_sethandle_v1(token, "new_dummy")
    assert res == {}




