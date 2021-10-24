import pytest
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.user import user_profile_v1
from src.channels import channels_create_v1
from src.other import clear_v1


@pytest.fixture
def dummy_cases():

    dummy = auth_register_v1("dummydum@gmail.com", "wordpass", "dummy", "dum")
    token = dummy['token']
    dummy_id = dummy['auth_user_id']

    return token, dummy_id

@pytest.fixture
def clear():
    clear_v1()    

def test_invalid_token(clear, dummy_cases):
    token, dummy_id = dummy_cases
    dummy_id = dummy_id + 1
    with pytest.raises(InputError):
        user_profile_v1(token, dummy_id)

def test_valid_output(clear, dummy_cases):
    token, dummy_id = dummy_cases
    result = user_profile_v1(token, dummy_id)

    assert result['user']['u_id'] ==  dummy_id
    assert result['user']['email'] == 'dummydum@gmail.com'
    assert result['user']['name_first'] == 'dummy'
    assert result['user']['name_last'] == 'dum'
    assert result['user']['handle_str'] == 'dummydum'



