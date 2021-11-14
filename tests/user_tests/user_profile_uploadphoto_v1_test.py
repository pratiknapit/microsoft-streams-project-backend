import pytest
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.user import user_profile_setemail_v1
from src.other import clear_v1
from src.user import users_all_v1, user_profile_uploadphoto_v1, user_profile_v1
from src.data_store import login_token
from src import config



@pytest.fixture
def dummy_cases():
    clear_v1()
    # dummy user with details
    dummy = auth_register_v1("dummy1@gmail.com", "password1", "First", "One")
    return dummy

def test_token_invalid(dummy_cases):
    token = "NeverGonnaGiveYouUpppppNeverGonnaLetYouDownnnn"
    astley_url = "https://64.media.tumblr.com/277d94e0c64666d3da355e6fcee1ffc0/164bc9bb438e190e-f0/s1280x1920/d95fbed20dd8fc485bcba3f7121e81f5b80dbab6.jpg"
    # 360 x 450
    with pytest.raises(AccessError):
        user_profile_uploadphoto_v1(token, astley_url, 0, 0, 300, 400)

def test_invalid_img_url(dummy_cases):
    valid_user = dummy_cases
    token = valid_user['token']
    url = "thisisanincorrecturl"
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(token, url , 0, 0, 300, 400)

def test_invalid_x_and_y_cases(dummy_cases):
    valid_user = dummy_cases
    token = valid_user['token']
    url = "https://64.media.tumblr.com/277d94e0c64666d3da355e6fcee1ffc0/164bc9bb438e190e-f0/s1280x1920/d95fbed20dd8fc485bcba3f7121e81f5b80dbab6.jpg"
    # 1200 x 726
    #invalid x start
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(token, url , -1, 0, 300, 400)
    # invalid y start
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(token, url , 0, -1, 300, 400)
    # invalid x end bound
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(token, url , 0, 0, 1300, 500)
    # invalid y end bound
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(token, url , 0, 0, 1200, 900)
    # invalid x end
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(token, url , 0, 0, -1, 900)
    # invalid y end
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(token, url , 0, 0, 1000, -1)

def test_not_jpg(dummy_cases):
    valid_user = dummy_cases
    token = valid_user['token']
    url = "https://static.wikia.nocookie.net/typemoon/images/7/71/Neco-Arc_Remake.png/revision/latest?cb=20210902002059"
    # 957 x 1706
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(token, url , 0, 0, 900, 1600)

def test_valid_case(dummy_cases):
    valid_user = dummy_cases
    token = valid_user['token']
    rick_url = "https://jollycontrarian.com/images/6/6c/Rickroll.jpg"
    # 786 x 535
    result = user_profile_uploadphoto_v1(token, rick_url, 50, 50, 700, 500)
    assert result == {}
    profile = user_profile_v1(token, valid_user['auth_user_id'])
    assert profile['user']['profile_img_url'] != config.url + 'src/static/default.jpg'





# incorrect url - done
#incorrect token - done
# incorrect x start - done
# incorrect y start - done
# incorrect x end - done
# incorrect y end - done


# valid/success case
# not JPG - done
# x end < x start - done
# y end < y start - done


