import pytest
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.user import user_profile_setemail_v1
from src.other import clear_v1
from src.user import users_all_v1
from src.data_store import login_token


'''
@pytest.fixture
def dummy_cases():
    clear_v1()
    # 2 dummy users with details
    auth_register_v1("dummy1@gmail.com", "password1", "First", "One")
    user2 = auth_register_v1("dummy2@gmail.com", "password2", "Second", "Two")
    token = user2['token']
    return token





def test_invalid_token(dummy_cases):
    token = 'invalidtoken'
    with pytest.raises(AccessError):
        assert users_all_v1(login_token)


def test_users_all(dummy_cases):
    token = user2
    assert users_all_v1() == {
        [
            {
                'u_id': 0,
                'email': 'dummy1@gmail.com',
                'name_first': 'First',
                'name_last': 'One',
                'handle_str': 'firstone',
            }, 
            {
                'u_id': 1,
                'email': 'dummy2@gmail.com',
                'name_first': 'Second',
                'name_last': 'Two',
                'handle_str': 'secondtwo',
            },
        ]
    }
'''

@pytest.fixture
def token():
    email = "testemail@gmail.com"
    password = "TestTest"
    firstname = "firstname"
    lastname = "lastname"
    return auth_register_v1(email,password,firstname, lastname)['token']

@pytest.fixture
def token1():
    email = "testemai333l@gmail.com"
    password = "TestTest3333"
    firstname = "firstname333"
    lastname = "lastname33"
    return auth_register_v1(email,password,firstname, lastname)['auth_user_id']

@pytest.fixture
def users():
    for i in range(5):
        email = f"test{i}email@gmail.com"
        password = f"TestTest{i}"
        firstname = f"firstname{i}"
        lastname = f"lastname{i}"
        id = auth_register_v1(email,password,firstname, lastname)
    return id['auth_user_id']


@pytest.fixture
def clear():
    clear_v1()

def test_invalid_token(clear):
    with pytest.raises(AccessError):
        users_all_v1('token')

'''
def test_return_6_users(clear, token, users):
    u_list = users_all_v1(token)
    assert len(u_list['users']) == 6


def test_proper_dict_values(clear, token, users):
    u_list = users_all_v1(token)
    assert len(u_list) == 1
    assert 'users' in u_list
    assert 'u_id' in u_list['users'][0]
    assert 'email' in u_list['users'][0]
    assert 'name_first' in u_list['users'][0]
    assert 'name_last' in u_list['users'][0]
    assert 'handle_str' in u_list['users'][0]
'''