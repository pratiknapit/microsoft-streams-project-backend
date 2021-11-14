from src.data_store import data_store

def clear_v1():
    store = data_store.get()
    store['users'] = []
    store['channels'] = []
    store['Messages'] = []
    store['dms'] = []
    data_store.set(store)

def search_v1(token, query_str):

    '''
    Given a query string, it returns a collection of messages in all of the 
    channels/DMs that the user has joined that contain the query.

    Arguments:
        token (str)   - A jwt encoded dictionary with u_id key
        query_str (str) - The query string which is being searched

    Exceptions:
        AccessError     - Occurs when the token is invalid
        InputError      - length of query_str is less than 1 or over 1000 characters
    Return Value:
        Returns {messages}, on the condition that everything is correct. Where messages is a 
        list of dictionaries where each dictionary contains types { message_id, u_id, message, 
        time_created, reacts, is_pinned  } 
    '''
    

    # Get list of all channels the user is in
    all_channels = []
    query_str = re.escape(query_str) # Treats special characters as normal text
    for channel in data.channels:
        check_u_id = [user.u_id for user in channel.all_members]
        if user_id in check_u_id:
            all_channels.append(channel)

    # Search each relevent channel for messages that match the query
    return_messages = []
    for channel in all_channels:
        for message in channel.channel_messages:
            if re.search(query_str, message.message):
                return_messages.append(message.message_details())
    return {
        'messages': return_messages
    }

    if token_check(token) == False:
        raise AccessError("Token provided is not valid")

    if len(query_str) > 1000:
        raise InputError("Query string is too long")



    # Created empty list, looping through the channels. If the user is a member 
    # of the channel and they have sent a DM, it will append this message to 
    # the list as a dictionary and return this list 
    messages_list = []
    for channel in data["channels"]:
        for member in channel['all_members']:
            if auth_user_id == member['auth_user_id'] and channel["dm_id"] == -1: 
                for message in channel["messages"]:
                    if query_str in  message["message"]:
                        mess_dict = {
                            "message_id": message["message_id"] ,
                            "u_id": message["auth_user_id"] , 
                            "message": message["message"], 
                            "time_created": message["timestamp"],
                        }
                        messages_list.append(mess_dict)
    return {
        'messages': messages_list
    }
    # return {messages}
    pass

