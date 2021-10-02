#tests for channel join function 
import pytest
from src.other import clear_v1

from src.channels import channels_create_v1
from src.channel import channels_join_v1
from src.auth import auth_register_v1

dummy1 = auth_register_v1("dummyvariableone@gmail.com", "password", "pratik", "napit")
dummy2 = auth_register_v1("dummyvariabletwo@gmail.com", "password", "conor", "mishra")
dummy1_id = dummy1['auth_user_id']
dummy2_id = dummy2['auth_user_id']

dummy1_channel = channels_create_v1(dummy1_id, "School", True)

def channels_join_test():
    clear_v1()

