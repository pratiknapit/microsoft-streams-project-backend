###########
#Functions#
###########
from src.data_store import add_user, login_email

##########################
# Helper Check Functions #
##########################
from src.data_store import email_check, email_repeat_check, password_check

###################
# Error Functions #
###################
from src.error import InputError

'''
<Logs in an Authorised user with correct password and email.>

Arguments:

    <email> (str)       - <A string which holds the email>

    <password> (str)    - <A string of set password>

    ...

Exceptions:

    InputError  - Occurs when the email is not a valid format for an email

    InputError  - Occurs when the email does not belong to the user

    InputError  - Occurs when password is not correctly entered

Return Value:

    Returns auth_user_id on condition that the user is valid and passes the check tests
'''
 

def auth_login_v1(email, password):
    if not email_check(email):
        raise InputError
    if not email_repeat_check(email):
        raise InputError
    if not password_check(password):
        raise InputError

    cur_user = login_email(email)
    return {
        "auth_user_id": cur_user["u_id"],
    }
'''
<Registers an authorised user given its arguments (email, password, name_first, name_last)>

Arguments:
    <email> (str) - <A string which holds the email>

    <password> (str) - <A string of set password>

    <name_first> (str) - <A string of the first name of the user>

    <name_last> (str) - <A string of the last name of the user>

    ...

Exceptions:

    InputError  - Occurs when the email is not a valid format for an email

    InputError  - Occurs when the email does not belong to the user

    InputError  - Occurs when length of password is less than 6

    InputError  - Occurs when length of name_first is less than 1 or greater than 50

    InputError  - Occurs when length of name_last is less than 1 or greater than 50


Return Value:

    Returns auth_user_id on condition that the user is valid and passes the check tests
'''
def auth_register_v1(email, password, name_first, name_last):                     # Add_user

    if email_check(email) == False:
        raise InputError
    if email_repeat_check(email) == True:
        raise InputError
    if len(password) < 6:
        raise InputError
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError

    added_user = add_user(email, password, name_first, name_last)
    return {
        "auth_user_id": added_user["u_id"],
    }


    if __name__ == '__main__':

        dummy_user_1 = add_user('dummyuser1@gmail.com', 'passworddd', 'Alpha', 'Napit')
        dummy_user_2 = add_user('dummyuser2@gmail.com', 'yessword', 'Alpha', 'Napit')
        dummy_user_3 = add_user('dummyuser3@gmail.com', 'passsssword', 'Alpha', 'Napit')
        print(dummy_user_1) 
        print(dummy_user_2)
        print(dummy_user_3)
