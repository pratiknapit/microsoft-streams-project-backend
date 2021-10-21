import pytest
from src.error import AccessError, InputError
from src.auth import auth_register_v1
from src.user import user_profile_setname_v1
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


def test_user_profile_setname_empty_inputs():
    clear_v1()
    user = auth_register_v1('emptyemail@gmail.com', 'paassworda', 'Empty', 'Email')
    with pytest.raises(InputError):
        user_profile_setname_v1('', '', '')

def test_first_name_too_short(clear, dummy_cases):
    token = dummy_cases
    with pytest.raises(InputError):
        user_profile_setname_v1(dummy_cases['token'], '', 'user')

def test_first_name_too_long(clear, dummy_cases):
    token = dummy_cases
    with pytest.raises(InputError):
        user_profile_setname_v1(dummy_cases['token'], 'dummy'*99, 'user')

def test_last_name_too_short(clear, dummy_cases):
    token = dummy_cases
    with pytest.raises(InputError):
        user_profile_setname_v1(dummy_cases['token'], 'dummy', '')

def test_last_name_too_long(clear, dummy_cases):
    token = dummy_cases
    with pytest.raises(InputError):
        user_profile_setname_v1(dummy_cases['token'], 'dummy', 'a'*99)

def test_valid_setname(clear, dummy_cases):
    token = dummy_cases
    res = user_profile_setname_v1(dummy_cases['token'], 'Gamma', 'GG')
    assert res == {}

def test_invalid_token():
    incorrect_token = '2289372834yes'
    with pytest.raises(AccessError):
        user_profile_setname_v1(incorrect_token, 'Gamma', 'GG')



