
import pytest
import jwt
from src.other import clear_v1
from src.error import AccessError, InputError
from src.auth import auth_register_v1, auth_login_v1
from src.dm import dm_list, dm_create, dm_remove, dm_details, dm_leave, dm_messages
from src.data_store import login_token, user_id_check
#from src.message import message_senddm

###########
#dm_create#
###########

@pytest.fixture
def token():
    email = "testmail@gamil.com"
    password = "Testpass12345"
    first_name = "firstone"
    last_name = "lastone"
    token = auth_register_v1(email, password, first_name, last_name)['token']
    return token

@pytest.fixture
def u_id1():
    email = "testmail1@gamil.com"
    password = "Testpass123456"
    first_name = "firsttwo"
    last_name = "lasttwo"
    u_id = auth_register_v1(email, password, first_name, last_name)['auth_user_id']
    return u_id

@pytest.fixture
def u_id2():
    email = "testmail2@gamil.com"
    password = "Testpass1234567"
    first_name = "firstthree"
    last_name = "lastthree"
    u_id = auth_register_v1(email, password, first_name, last_name)['auth_user_id']
    return u_id

@pytest.fixture
def user0():
    email = "testemail@gmail.com"
    password = "TestTest"
    firstname = "firstname"
    lastname = "lastname"
    return auth_register_v1(email, password, firstname, lastname)

@pytest.fixture
def user1():
    email = "test1email@gmail.com"
    password = "TestTest1"
    firstname = "firstname1"
    lastname = "lastname1"
    return auth_register_v1(email, password, firstname, lastname)

@pytest.fixture
def user2():
    email = "test2email@gmail.com"
    password = "TestTest2"
    firstname = "firstname2"
    lastname = "lastname2"
    return auth_register_v1(email, password, firstname, lastname)

@pytest.fixture
def clear():
    clear_v1()

def test_invalid_token(u_id1):
    with pytest.raises(AccessError):
        dm_create("Invalid token", [u_id1])
    clear_v1()

def test_invalid_u_ids(token, u_id1):
    with pytest.raises(InputError):
        dm_create(token, [u_id1, 123])
    clear_v1()

def test_valid_return(token, u_id1, u_id2):
    assert dm_create(token, [u_id1])['dm_id'] == 1
    assert dm_create(token, [u_id1, u_id2])['dm_id'] == 2
    clear_v1()


#########
#dm_list#
#########

def test_token_int_invalid(clear):

    invalid_token = 10000
    with pytest.raises(AccessError):
        dm_list(invalid_token)

def test_success_case(clear):

    admin = auth_register_v1('test1@unsw.au', 'password1', 'first1', 'last1')
    member_1 = auth_register_v1(
        'test2@unsw.au', 'password2', 'first2', 'last2')
    member_2 = auth_register_v1(
        'test3@unsw.au', 'password3', 'first3', 'last3')

    members_list = []
    members_list.append(member_1['auth_user_id'])
    members_list.append(member_2['auth_user_id'])

    dm_create(admin['token'], members_list)

    member_1_dm_list = dm_list(member_1['token'])
    member_2_dm_list = dm_list(member_2['token'])

    assert len(member_1_dm_list) == 1
    assert len(member_2_dm_list) == 1

###########
#dm_remove#
###########

def test_invalid_dm_id(clear, user0):
    with pytest.raises(InputError):
        dm_remove(user0['token'], 1) 
    clear_v1()

def test_invalid_token(clear, user0):
    owner_token = auth_register_v1("dmcreator@gmail.com", "TestTest1", "first", "last")['token']
    dm = dm_create(owner_token, [user0['auth_user_id']])
    
    with pytest.raises(AccessError):
        dm_remove("invalid.token.input", dm['dm_id'])
    clear_v1()

def test_not_creator(clear, user0):
    owner_token = auth_register_v1("dmcreator@gmail.com", "TestTest1", "first", "last")['token']
    dm = dm_create(owner_token, [user0['auth_user_id']])
    
    with pytest.raises(AccessError):
        dm_remove(user0['token'],dm['dm_id'])
    clear_v1()

def test_successful_remove(clear, user0):
    owner_token = auth_register_v1("dmcreator@gmail.com", "TestTest1", "first", "last")['token']
    dm = dm_create(owner_token, [user0['auth_user_id']])
    
    assert dm_remove(owner_token, dm['dm_id']) == {}
    clear_v1()

############
#dm_details#
############

@pytest.fixture
def num_members():
    return 5

@pytest.fixture
def users(num_members):

    u_ids = []
    tokens = []
    for i in range(num_members):
        email = f"test{i}email@gmail.com"
        password = f"TestTest{i}"
        name_first = f"firstname{i}"
        name_last = f"lastname{i}"
        user = auth_register_v1(email, password, name_first, name_last)
        u_ids.append(user['auth_user_id'])
        tokens.append(user['token'])
    return {'tokens' : tokens, 'u_ids': u_ids}


def test_invalid_token(clear):
    with pytest.raises(AccessError):
        dm_details(jwt.encode({'test' : 'token'}, 'testSecret', algorithm='HS256'), 5)

def test_user_not_in_dm(clear, users):
    dm = dm_create(users['tokens'][1], users['u_ids'][2:])
    with pytest.raises(AccessError):
        dm_details(users['tokens'][0], dm['dm_id'])

def test_invalid_dm_id(clear, users):
    with pytest.raises(InputError):
        dm_details(users['tokens'][0], 'test_dm_id')

def test_user_in_dm(clear, users, num_members):
    dm = dm_create(users['tokens'][0], users['u_ids'][1:])
    details = dm_details(users['tokens'][1], dm['dm_id'])
    assert len(details) == 2
    assert len(details['members']) == num_members

def test_valid_dict_keys(clear, users):
    dm = dm_create(users['tokens'][0], users['u_ids'])
    details = dm_details(users['tokens'][1], dm['dm_id'])
    assert 'names' and 'members' in details 
    assert 'u_id' in details['members'][0] 
    assert 'email' in details['members'][0] 
    assert 'name_first' in details['members'][0] 
    assert 'name_last' in details['members'][0]
    assert 'handle_str' in details['members'][0] 



##########
#dm_leave#
##########

def test_dm_not_valid():
    clear_v1()

    user = auth_register_v1('test1@unsw.au', 'password1', 'first1', 'last1')

    with pytest.raises(InputError):
        dm_leave(user['token'], 300)

    clear_v1()


def test_auth_user_not_dm_member():
    clear_v1()

    admin = auth_register_v1('test1@unsw.au', 'password1', 'first1', 'last1')
    member_1 = auth_register_v1(
        'test2@unsw.au', 'password2', 'first2', 'last2')
    member_2 = auth_register_v1(
        'test3@unsw.au', 'password3', 'first3', 'last3')

    member_list = []
    member_list.append(member_1['auth_user_id'])
    member_list.append(member_2['auth_user_id'])

    dm_1 = dm_create(admin['token'], member_list)

    invalid_user = 321321

    with pytest.raises(AccessError):
        dm_leave(invalid_user, dm_1['dm_id'])

    clear_v1()


def test_success_case():
    clear_v1()

    admin = auth_register_v1('test1@unsw.au', 'password1', 'first1', 'last1')
    member_1 = auth_register_v1(
        'test2@unsw.au', 'password2', 'first2', 'last2')
    member_2 = auth_register_v1(
        'test3@unsw.au', 'password3', 'first3', 'last3')

    member_list = []
    member_list.append(member_1['auth_user_id'])
    member_list.append(member_2['auth_user_id'])

    dm_1 = dm_create(admin['token'], member_list)

    dm_leave(member_2['token'], dm_1['dm_id'])

    member_2_dm_list = dm_list(member_2['token'])

    assert member_2_dm_list['dms'] == []

    clear_v1()


#############
#dm_messages#
#############

@pytest.fixture
def token2():
    clear_v1()
    # create a test user and return auth_id
    email = "testmail@gamil.com"
    password = "Testpass12345"
    token = auth_register_v1(email, password, "firstname", "lastname")['token']
    return token

@pytest.fixture
def dm_id(token2):
    # create a public channel and return dm_id
    member1 = auth_register_v1("testmail@gamil1.com", "Testpass123456", "firstone", "lastone")['auth_user_id']
    member2 = auth_register_v1("testmail@gamil2.com", "Testpass1234567", "firsttwo", "lasttwo")['auth_user_id']
    dm_id = dm_create(token2, [member1, member2])['dm_id']
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

def test_invalid_dm_id(token2, dm_id):
    with pytest.raises(InputError):
        dm_messages(token2, dm_id + 1, 0)

def test_unauthorised_user(unauthorised_user, dm_id):
    # Test an user that does not belong to the dm with the given dm_id
    with pytest.raises(AccessError):
        dm_messages(unauthorised_user, dm_id, 0)

def test_invalid_start(token2, dm_id):
    # this fail because no message is being sent to the dm yet
    with pytest.raises(InputError):
        dm_messages(token2, dm_id, 51)
'''
def test_last_message(token2, dm_id):
    # Test if end = -1 when there are no more messages to load after the current return
    message_senddm(token2, dm_id, "Hi, everyone!")
    end = dm_messages(token2, dm_id, 0)['end']
    assert end == -1
'''
'''
def test_more_messages(token2, dm_id):
    count = 60
    while count >= 0:
        message_senddm(token2, dm_id, f"{count}")
        count -= 1

    # Test first 50 newest messages
    message_1 = dm_messages(token, dm_id, 0)['messages'][49]['message']
    assert message_1 == "49"
    # Test the first message in the returned message dictionary
    message_2 = dm_messages(token, dm_id, 10)['messages'][0]['message']
    assert message_2 == "10"
    # Test the second message in the returned message dictionary
    message_3 = dm_messages(token, dm_id, 30)['messages'][1]['message']
    assert message_3 == '31'
    # Test the earliest message that was sent to the dm
    message_4 = dm_messages(token, dm_id, 60)['messages'][0]['message']
    assert message_4 == '60'
'''