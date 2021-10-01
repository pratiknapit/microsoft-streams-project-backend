'''
data_store.py

This contains a definition for a Datastore class which you should use to store your data.
You don't need to understand how it works at this point, just how to use it :)

The data_store variable is global, meaning that so long as you import it into any
python file in src, you can access its contents.

Example usage:

    from data_store import data_store

    store = data_store.get()
    print(store) # Prints { 'names': ['Nick', 'Emily', 'Hayden', 'Rob'] }

    names = store['names']

    names.remove('Rob')
    names.append('Jake')
    names.sort()

    print(store) # Prints { 'names': ['Emily', 'Hayden', 'Jake', 'Nick'] }
    data_store.set(store)
'''

## YOU SHOULD MODIFY THIS OBJECT BELOW
initial_object = {
    'user': [    
    ],
    'channels': [

    ],
}


#Channels functions - made by Pratik 

# def function to make channel dictionary

def make_channel(auth_user_id, channel_id, name, is_public):

    return {
        'channel_id': channel_id, #need to make this in another function
        'name': name,
        'is_public': is_public,
        'owner_members': [auth_user_id],
        'all_members': [auth_user_id]
    }


# def function to add channel to list 

def add_channel(auth_user_id, name, is_public):
    store = data_store.get() #retrieve our initial object data
    channel_id = len(store['channels']) + 1 #use this function above to get channel id, we might not even need the function 
    channel = make_channel(auth_user_id, channel_id, name, is_public)
    store['channels'].append(channel)


    data_store.set(store) #believe that this should just make sure that the data is still a dictionary
    #need to make a new list which only returns { channel_id }
    return channel

# def function to return list of channels that user is part of 

def user_channels(auth_user_id):
    store = data_store.get()
    user_list_channel = {
        'channels': [

        ],
    } #this is empty list that we will append to
    for channel in store['channels']: 
        for member in channel['all_members']:
            if member == auth_user_id:
                user_list_channel['channels'].append(channel)
    

    return user_list_channel



## YOU SHOULD MODIFY THIS OBJECT ABOVE

class Datastore:
    def __init__(self):
        self.__store = initial_object

    def get(self):
        return self.__store

    def set(self, store):
        if not isinstance(store, dict):
            raise TypeError('store must be of type dictionary')
        self.__store = store

print('Loading Datastore...')

global data_store
data_store = Datastore()

