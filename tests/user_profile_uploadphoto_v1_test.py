import pytest
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.user import user_profile_setemail_v1
from src.other import clear_v1
from src.user import users_all_v1, user_profile_uploadphoto_v1, user_profile_v1
from src import config



@pytest.fixture
def dummy_cases():
    clear_v1()
    # dummy user with details
    dummy = auth_register_v1("dummy1@gmail.com", "password1", "First", "One")
    return dummy

def test_token_invalid(dummy_cases):
    token = "NeverGonnaGiveYouUpppppNeverGonnaLetYouDownnnn"
    astley_url = "http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg"
    # 159 x 200
    with pytest.raises(AccessError):
        user_profile_uploadphoto_v1(token, astley_url, 0, 0, 100, 100)

def test_invalid_img_url(dummy_cases):
    valid_user = dummy_cases
    token = valid_user['token']
    url = "thisisanincorrecturl"
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(token, url , 0, 0, 300, 400)

def test_invalid_x_and_y_cases(dummy_cases):
    valid_user = dummy_cases
    token = valid_user['token']
    url = "http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg"
    # 159 x 200
    #invalid x start
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(token, url , -1, 0, 100, 100)
    # invalid y start
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(token, url , 0, -1, 100, 100)
    # invalid x end bound
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(token, url , 0, 0, 200, 100)
    # invalid y end bound
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(token, url , 0, 0, 100, 900)
    # invalid x end
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(token, url , 0, 0, -1, 100)
    # invalid y end
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(token, url , 0, 0, 100, -1)

def test_not_jpg(dummy_cases):
    valid_user = dummy_cases
    token = valid_user['token']
    url = "http://www.cse.unsw.edu.au/~richardb/index_files/RichardBuckland-200.png"
    # 159 x 200
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(token, url , 0, 0, 900, 1600)

def test_valid_case(dummy_cases):
    valid_user = dummy_cases
    token = valid_user['token']
    url = "http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg"
    # 159 x 200
    result = user_profile_uploadphoto_v1(token, url, 0, 0, 100, 100)
    assert result == {}
    profile = user_profile_v1(token, valid_user['auth_user_id'])
    assert profile['user']['profile_img_url'] != 'src/static/default.jpg'





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


