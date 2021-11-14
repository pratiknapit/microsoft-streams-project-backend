import json
import pytest
import requests
from src import config
from src.other import clear_v1


@pytest.fixture
def dummy_user():
    user = requests.post(config.url + "/auth/register/v2", json={
        "email": "dummy1@gmail.com",
        "password": "password1",
        "name_first": "First",
        "name_last": "One",
    })
    payload = user.json()
    return payload

@pytest.fixture(autouse=True)
def clear():
    requests.delete(config.url + '/clear/v1')
    yield
    requests.delete(config.url + '/clear/v1')



# incorrect url - done
#incorrect token - not needed here
# incorrect x start - done 
# incorrect y start - done 
# incorrect x end - done 
# incorrect y end - done 


# valid/success case - done
# not JPG - 
# x end < x start - done same time 
# y end < y start - 


def test_invalid_url(dummy_user):
    url = "HereIsACookie"
    user = dummy_user
    token = user['token']
    res = requests.post(config.url + "/user/profile/uploadphoto/v1", json={
        "token": token,
        "img_url": url,
        "x_start": 0,
        "y_start": 0,
        "x_end": 100,
        "y_end": 100,
    })
    assert res.status_code == 400

def test_valid_input(dummy_user):
    url = "http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg"
    user = dummy_user
    token = user['token']
    res = requests.post(config.url + "/user/profile/uploadphoto/v1", json={
        "token": token,
        "img_url": url,
        "x_start": 0,
        "y_start": 0,
        "x_end": 100,
        "y_end": 100,
    })
    payload = res.json()
    assert payload == {}

def test_invalid_x_start(dummy_user):
    url = "http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg"
    user = dummy_user
    token = user['token']

    res = requests.post(config.url + "/user/profile/uploadphoto/v1", json={
        "token": token,
        "img_url": url,
        "x_start": -1,
        "y_start": 0,
        "x_end": 100,
        "y_end": 100,
    })
    assert res.status_code == 400 # InputError


def test_invalid_y_start(dummy_user):
    url = "http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg"
    user = dummy_user
    token = user['token']

    res = requests.post(config.url + "/user/profile/uploadphoto/v1", json={
        "token": token,
        "img_url": url,
        "x_start": 0,
        "y_start": -1,
        "x_end": 100,
        "y_end": 100,
    })
    assert res.status_code == 400 # InputError

def test_switched_dimensions(dummy_user):
    url = "http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg"
    user = dummy_user
    token = user['token']

    res = requests.post(config.url + "/user/profile/uploadphoto/v1", json={
        "token": token,
        "img_url": url,
        "x_start": 50,
        "y_start": 50,
        "x_end": 0,
        "y_end": 0,
    })
    assert res.status_code == 400 # InputError

def test_ouside_boundaries_x_end_invalid(dummy_user):
    url = "http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg"
    user = dummy_user
    token = user['token']

    res = requests.post(config.url + "/user/profile/uploadphoto/v1", json={
        "token": token,
        "img_url": url,
        "x_start": 0,
        "y_start": 0,
        "x_end": 100000,
        "y_end": 100,
    })
    assert res.status_code == 400 # InputError

def test_ouside_boundaries_y_end_invalid(dummy_user):
    url = "http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg"
    user = dummy_user
    token = user['token']

    res = requests.post(config.url + "/user/profile/uploadphoto/v1", json={
        "token": token,
        "img_url": url,
        "x_start": 0,
        "y_start": 0,
        "x_end": 100,
        "y_end": 1000000,
    })
    assert res.status_code == 400 # InputError
