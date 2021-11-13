import requests
import pytest
from src import config

@pytest.fixture(autouse=True)
def clear():
    requests.delete(config.url + '/clear/v1')
    yield
    requests.delete(config.url + '/clear/v1')
###############
#auth_register#
###############
def test_given_email_is_invalid():
    registration = requests.post(config.url + "auth/register/v2",
                                 json={'email': 'test.unsw.edu.au', 'password': 'password', 'name_first': 'test123', 'name_last': 'last123'})
    assert registration.status_code == 400

def test_email_already_exists():
    requests.post(config.url + 'auth/register/v2',
                  json={'email': 'test@unsw.edu.au', 'password': 'password', 'name_first': 'test123', 'name_last': 'last123'})
    registration = requests.post(config.url + 'auth/register/v2',
                                 json={'email': 'test@unsw.edu.au', 'password': 'password2', 'name_first': 'test321', 'name_last': 'last321'})
    assert registration.status_code == 400

def test_password_incorrect_length():
    registration = requests.post(config.url + 'auth/register/v2',
                                 json={'email': 'test@unsw.edu.au', 'password': ' ', 'name_first': 'test123', 'name_last': 'last123'})
    assert registration.status_code == 400

def test_first_name_valid_length():
    registration = requests.post(config.url + 'auth/register/v2',
                                 json={'email': 'test@unsw.au', 'password': 'password', 'name_first': 'thisfirstnameistoolongandcontainsspecialcharacters##^^&&**!!123123123', 'name_last': 'last123'})
    assert registration.status_code == 400

def test_last_name_valid_length():
    registration = requests.post(config.url + 'auth/register/v2',
                                 json={'email': 'test@unsw.au', 'password': 'password', 'name_first': 'firstname', 'name_last': 'thislastnamecontainsspecialcharacters##^^&&**!!123123123'})
    assert registration.status_code == 400

def test_auth_reg_valid():
    response = requests.post(config.url + "auth/register/v2", 
                             json={
    "email": "use4r@gmail.com",
    "password": "dummypass",
    "name_first": "jacky",
    "name_last": "zhu"
    }) 
    assert response.status_code == 200

############
#auth_login#
############

# Test for email valid format
def test_invalid_email():
    login_call = requests.post(config.url + 'auth/login/v2',
                               json={'email': 'testing.unsw.au', 'password': 'password'})
    assert login_call.status_code == 400

# Test for email given belongs to user
def test_email_nonexistent():
    login_call = requests.post(config.url + 'auth/login/v2',
                               json={'email': 'testing123@unsw.au', 'password': 'password'})
    assert login_call.status_code == 400

# Test for correct password
def test_password_incorrect():
    requests.post(config.url + 'auth/register/v2',
                  json={'email': 'testing123@unsw.au', 'password': 'password', 'name_first': 'testing123', 'name_last': 'last123'})
    login_call = requests.post(config.url + 'auth/login/v2',
                               json={'email': 'testing123@unsw.au', 'password': 'failed123'})
    assert login_call.status_code == 400


# Test for correct email and password
def test_correct_login_details():
    registration = requests.post(config.url + 'auth/register/v2',
                                 json={'email': 'testing123@unsw.au', 'password': 'password', 'name_first': 'testing123', 'name_last': 'last123'})
    login_call = requests.post(config.url + 'auth/login/v2',
                               json={'email': 'testing123@unsw.au', 'password': 'password'})
    login_details = login_call.json()
    registration_details = registration.json()
    print(login_details)
    assert login_call.status_code == 200
    assert registration_details['auth_user_id'] == login_details['auth_user_id']


#############
#auth_logout#
#############

@pytest.fixture
def token():
    email = "test@unsw.au"
    password = "testPassword"
    firstname = "firstName"
    lastname = "lastName"
    response = requests.post(config.url + 'auth/register/v2', json={'email': email, 'password': password, 'name_first': firstname, 'name_last': lastname})
    token = response.json()['token']
    return token

def test_valid_response(token):
    response = requests.post(config.url + 'auth/logout/v1', json={'token': token})
    assert response.json()['is_success'] == True
    assert response.status_code == 200
