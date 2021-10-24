import pytest
from src.other import clear_v1
from src.auth import auth_register_v1
from src.dm import dm_create
from src.error import InputError, AccessError

@pytest.fixture
def token():
    email = "unilove0@gamil.com"
    password = "unipass12345"
    first_name = "jacky"
    last_name = "yuchao"
    token = auth_register_v1(email, password, first_name, last_name)['token']
    return token

@pytest.fixture
def user1():
    email = "testmail1@gamil.com"
    password = "Testpass123456"
    first_name = "firsttwo"
    last_name = "lasttwo"
    u_id = auth_register_v1(email, password, first_name, last_name)['auth_user_id']
    return u_id

@pytest.fixture
def user2():
    email = "testmail2@gamil.com"
    password = "Testpass1234567"
    name_first = "firstthree"
    name_last = "lastthree"
    u_id = auth_register_v1(email, password, name_first, name_last)['auth_user_id']
    return u_id

def test_invalid_token(user1):
    with pytest.raises(AccessError):
        dm_create("Invalid token", [user1])
    clear_v1()

def test_invalid_u_ids(token, user1):
    with pytest.raises(InputError):
        dm_create(token, [user1, 123])
    clear_v1()

def test_valid_return(token, user1, user2):
    assert dm_create(token, [user1])['dm_id'] == 1
    assert dm_create(token, [user1, user2])['dm_id'] == 2
    clear_v1()