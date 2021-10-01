def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    
    ## some variable and function names are just placeholder for now remember to replace them 
    ## placeholder code will have "pl" at the start
    
    if channel_id_check(channel_id) == False:     #Check if channel_id is valid  
        raise InputError
    if member_of_channel_check(auth_user_id, channel_id) == False: #Check if user is in the channel
        raise AccessError


    channel_details_dictionary = {      #Create a new dictionery that will store all the channel_details 
    }
    
    extract_channel_details = channel_id_check(channel_id) #Something that will let me access the channels dictionary
    channel_details_dictionary['name'] = extract_channel_details['name']                        #Populate the details dictionary
    channel_details_dictionary['is_public'] = extract_channel_details['is_public']
    channel_details_dictionary['owner_members'] = extract_channel_details['owner_members']
    channel_details_dictionary['all_members'] = extract_channel_details['all_members']
    
    return {channel_details_dictionery}
    

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
