import pytest
import jwt
from src.error import InputError, AccessError
from src.auth import auth_register_v1, auth_login_v1, auth_logout, auth_passwordreset_request, auth_passwordreset_reset
from src.other import clear_v1
from src.data_store import is_valid_token, data_store

@pytest.fixture
def clear():
    clear_v1()

@pytest.fixture
def token():
    email = "test2email@gmail.com"
    password = "TestTest2"
    firstname = "firstname2"
    lastname = "lastname2"
    return auth_register_v1(email, password, firstname, lastname)['token']

###############
#Auth_register#
###############
def test_auth_register_email_invalid(clear):
    with pytest.raises(InputError):
        assert auth_register_v1("yuchaocool.com", "password", "yuchao", "zhu")                          # Invalid email- no @

def test_auth_register_duplicate_email_invalid(clear):
    dummy_user_1 = auth_register_v1('dummyuser1@gmail.com', 'passworddd', 'Alpha', 'AA')
    with pytest.raises(InputError):
        assert auth_register_v1('dummyuser1@gmail.com', 'password', 'Alpha', 'AA')            # Same user email_repeat_check()

def test_auth_register_password_invalid(clear):
    with pytest.raises(InputError):
        assert auth_register_v1("jackysydau@gmail.com", "pie", "yuchao", "zhu")                 # Password less than 6 characters

def test_auth_register_first_min_invalid(clear):
    with pytest.raises(InputError):
        assert auth_register_v1("jackysydau@gmail.com", "password", "", "zhu")                  # name_first less than 1 character

def test_auth_register_last_min_invalid(clear):
    with pytest.raises(InputError):
        assert auth_register_v1("jackysydau@gmail.com", "password", "yuchao", "")               # name_last less than 1 character
        
def test_auth_register_first_max_invalid(clear):
    with pytest.raises(InputError):
        assert auth_register_v1("jackysydau@gmail.com", "password", "phoenixreborn12345phoenixreborn12345phoenixreborn12345", "xxxshadowlordxxx")           # name_first more than 50 characters

def test_auth_register_last_max_invalid(clear):
    with pytest.raises(InputError):
        assert auth_register_v1("jackysydau@gmail.com", "password", "xxxshadowlordxxx", "drownedangeldrownedangeldrownedangeldrownedangeldrownedangel")     # name_last more than 50 characters

def test_auth_register_user_valid(clear):
    valid_user = auth_register_v1("validummy@gmail.com", "password", "smart", "dummy")
    assert(valid_user == {"auth_user_id": valid_user["auth_user_id"], "token": valid_user["token"]})
############
#Auth_login#
############
def test_auth_login_email_invalid(clear):
    with pytest.raises(InputError):
        assert auth_login_v1("where@", "password")                                               # Invalid email

def test_auth_correct_login_details(clear):
    uid_1 = auth_register_v1('testing123@unsw.au', 'password', 'first123', 'last123')
    assert is_valid_token(uid_1['token'])
    
def test_auth_password_incorrect(clear):
    auth_register_v1('testing123@unsw.au', 'password', 'first123', 'last123')
    with pytest.raises(InputError):
        auth_login_v1('testing123@unsw.au', 'failed123')

    auth_register_v1('testing567@unsw.au', 'password', 'first567', 'last567')
    with pytest.raises(InputError):
        auth_login_v1('testing567@unsw.au', 'failed567')

    auth_register_v1('testing890@unsw.au', 'password', 'first890', 'last890')
    with pytest.raises(InputError):
        auth_login_v1('testing890@unsw.au', 'failed890')

def test_auth_email_nonexistent(clear):
    auth_register_v1('testing123@unsw.au', 'password', 'first123', 'last123')
    with pytest.raises(InputError):
        auth_login_v1('testfail1@unsw.au', 'password')

    auth_register_v1('testing567@unsw.au', 'password', 'first567', 'last567')
    with pytest.raises(InputError):
        auth_login_v1('testfail2@unsw.au', 'password')

    auth_register_v1('testing890@unsw.au', 'password', 'first890', 'last890')
    with pytest.raises(InputError):
        auth_login_v1('testfail3@unsw.au', 'password')

def test_auth_invalid_email(clear):
    invalid_email_1 = '@unsw.edu.au'
    with pytest.raises(InputError):
        auth_login_v1(invalid_email_1, 'password')

    invalid_email_2 = 'test@.au'
    with pytest.raises(InputError):
        auth_login_v1(invalid_email_2, 'password')

    invalid_email_3 = 'test.unsw.edu.au'
    with pytest.raises(InputError):
        auth_login_v1(invalid_email_3, 'password')

    invalid_email_4 = 'test_special!!!@unsw.au'
    with pytest.raises(InputError):
        auth_login_v1(invalid_email_4, 'password')

def test_auth_register_test_dummy(clear):
    dummy_user_1 = auth_register_v1('dummyuser1@gmail.com', 'passworddd', 'Alpha', 'AA')
    dummy_id = auth_login_v1("dummyuser1@gmail.com", "passworddd")
    assert(dummy_user_1['auth_user_id'] == dummy_id['auth_user_id'])

#############
#Auth_logout#
#############
def test_auth_logout_invalid():
    with pytest.raises(AccessError):
        auth_logout('This_is_a_wrong_token') 

def test_auth_correct_return(clear, token):    
    assert auth_logout(token) == True


#############################
#auth_password_request/reset#
#############################

def test_auth_password_request_test(clear):
    data = data_store.get()
    auth_register_v1('validemail@gmail.com', '123abc!@#', 'Jacky', 'Zhu')
    auth_passwordreset_request('validemail@gmail.com')

    for user in data['users']:
        if user['u_id'] == 1:
            assert user['reset_code'] != 0
            break

def test_auth_passwordreset_success(clear):
    id_check = auth_register_v1('jokeame@gmail.com', '123123123', 'Jack', 'Sparrow')['auth_user_id']
    reset_code = auth_passwordreset_request('jokeame@gmail.com')
    auth_passwordreset_reset(reset_code, 'TheNewPassword')
    assert auth_login_v1('jokeame@gmail.com', 'TheNewPassword')['auth_user_id'] == id_check


def test_auth_passwordrequest_invalid_email(clear):
    auth_register_v1('jokeame@gmail.com', '123123123', 'Jack', 'Sparrow')
    with pytest.raises(InputError):
        auth_passwordreset_request('dokesmate@gmail.com')

def test_auth_passwordreset_reset_invalid_password(clear):
    auth_register_v1('jokeame@gmail.com', '123123123', 'Jack', 'Sparrow')
    reset_code = auth_passwordreset_request('jokeame@gmail.com')
    invalid_password = '123'
    with pytest.raises(InputError):
        auth_passwordreset_reset(reset_code, invalid_password)

def test_auth_passwordreset_reset_invalid_reset_code(clear):
    auth_register_v1('jokeame@gmail.com', '123123123', 'Jack', 'Sparrow')
    reset_code = auth_passwordreset_request('jokeame@gmail.com')
    invalid_reset_code = reset_code + '123'
    with pytest.raises(InputError):
        auth_passwordreset_reset(invalid_reset_code, 'TheNewPassword')