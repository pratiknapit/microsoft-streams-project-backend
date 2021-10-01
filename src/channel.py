def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    
    #Check if channel_id is valid
    if channel_id_check(channel_id) == False:       
        raise InputError("channel id not valid")
        #Check if user is in the channel
    if check_if_user_is_channel_member(auth_user_id, channel_id) == False: 
        raise AccessError

    #Create a new dictionery that will store all the channel_details 
    channel_details_dictionary = {      
    }

    #Something that will let me access the channels dictionary
    extract_channel_details = channel_id_check(channel_id)            
    channel_details_dictionary['name'] = extract_channel_details['name']                        
    channel_details_dictionary['is_public'] = extract_channel_details['is_public']
    channel_details_dictionary['owner_members'] = extract_channel_details['owner_members']
    channel_details_dictionary['all_members'] = extract_channel_details['all_members']
    
    return channel_details_dictionery
    

def channel_messages_v1(auth_user_id, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_join_v1(auth_user_id, channel_id):
    return {
    }
