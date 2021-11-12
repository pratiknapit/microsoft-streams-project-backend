import pytest
from src.other import clear_v1
from src.error import AccessError, InputError
from src.auth import auth_register_v1
from src.dm import dm_list, dm_create

@pytest.fixture(autouse=True)
def clear():
    clear_v1() 
    yield
    clear_v1

def test_token_user_nonexistent():

    invalid_token = 100000

    with pytest.raises(AccessError):
        dm_list(invalid_token)


def test_success_case():

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