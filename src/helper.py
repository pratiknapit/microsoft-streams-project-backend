from src.data_store import check_existing_member, check_existing_owner, data_store, is_user_in_dm, remove_owner_channel, save_data 

def global_owner_check(u_id): 
    data = data_store.get()

    users = data['users']

    for user in users:
        if user['u_id'] == u_id:
            if user['is_global_owner'] == 1: 
                return True
            else:
                return False 


def remove_user_id_from_channels(u_id):
    data = data_store.get()

    if len(data['channels']) != 0:
        #Need to remove the user from any channels they are in 
        for channel in data['channels']:
            if check_existing_member(u_id, channel['channel_id']):
                for member in channel['all_members']:
                    if member == u_id:
                        channel['all_members'].remove(u_id)
            
            if check_existing_owner(u_id, channel['channel_id']):
                remove_owner_channel(channel['channel_id'], u_id)
                   
            for message in channel['Messages']:
                if message['u_id'] == u_id:
                    message['message'] = "Removed user"
    
    save_data(data)
    return 

def remove_user_from_dms(u_id):
    data = data_store.get()

    if len(data['dms']) != 0:
        for dm in data['dms']:
            if is_user_in_dm(dm['dm_id'], u_id): 
                if dm['creator'] == u_id:
                    data['dms'].remove(dm) #if the user is the creator of the dm then, delete the whole dm
                else:
                    for member in dm['members']:
                        if member == u_id:
                            dm['members'].remove(member)
        
                for message in dm['messages']:
                    if message['u_id'] == u_id:
                        message['message'] = "Removed user"
    
    save_data(data)


    



    
                

    
        