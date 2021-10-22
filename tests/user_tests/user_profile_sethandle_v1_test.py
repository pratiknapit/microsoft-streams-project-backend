import pytest
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.user import user_profile_sethandle_v1
from src.other import clear_v1


@pytest.fixture
def dummy_cases():
    # Dummy case created for testing of different parts of channel_invite_v1
    auth_register_v1('dummyuser2@gmail.com', 'yessword', 'Betta', 'BB')
    dummy_user_3 = auth_register_v1('dummyuser3@gmail.com', 'pspassword', 'Tree', 'Three')
    token = dummy_user_3['token']
    return token

@pytest.fixture
def clear():
    clear_v1()
    

def test_handle_already_taken(clear, dummy_cases):
    token = dummy_cases
    with pytest.raises(InputError):
        user_profile_sethandle_v1(dummy_cases, "bettabb")

def test_handle_invalid(clear, dummy_cases):
    token = dummy_cases
    with pytest.raises(InputError):
        user_profile_sethandle_v1(token, "y"*0)
    with pytest.raises(InputError):
        user_profile_sethandle_v1(token, "y")
    with pytest.raises(InputError):
        user_profile_sethandle_v1(token, "y"*99)

def test_valid_sethandle(clear, dummy_cases):
    token = dummy_cases
    result = user_profile_sethandle_v1(token, "newdummy")
    assert result == {}




