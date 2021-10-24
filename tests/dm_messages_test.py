import pytest
from src.other import clear_v1
from src.auth import auth_register_v1
from src.dm import dm_create, dm_messages
from src.error import InputError, AccessError

@pytest.fixture
def token():
    clear_v1()
    # create a test user and return auth_id
    email = "testmail@gamil.com"
    password = "Testpass12345"
    token = auth_register_v1(email, password, "firstname", "lastname")['token']
    return token

@pytest.fixture
def dm_id(token):
    # create a public channel and return dm_id
    member1 = auth_register_v1("testmail@gamil1.com", "Testpass123456", "firstone", "lastone")['auth_user_id']
    member2 = auth_register_v1("testmail@gamil2.com", "Testpass1234567", "firsttwo", "lasttwo")['auth_user_id']
    dm_id = dm_create(token, [member1, member2])['dm_id']
    return dm_id

@pytest.fixture
def unauthorised_user():
    email = "testmail3@gamil.com"
    password = "Testpass12345"
    token = auth_register_v1(email, password, "firstthree", "lastthree")['token']
    return token

def test_invalid_token(dm_id):
    with pytest.raises(AccessError):
        dm_messages("invalid_token", dm_id, 0)

def test_invalid_dm_id(token, dm_id):
    with pytest.raises(InputError):
        dm_messages(token, dm_id + 1, 0)

def test_unauthorised_user(unauthorised_user, dm_id):
    # Test an user that does not belong to the dm with the given dm_id
    with pytest.raises(AccessError):
        dm_messages(unauthorised_user, dm_id, 0)

def test_invalid_start(token, dm_id):
    # this fail because no message is being sent to the dm yet
    with pytest.raises(InputError):
        dm_messages(token, dm_id, 51)