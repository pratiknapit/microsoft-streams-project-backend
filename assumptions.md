
    Our assumptions:

        1.  We assume that the input for is_public is either True or False.
        2.  We assume that there is only one channel owner for this iteration, who is the first user who created the channel.
        3.  We assume that only the very first user who enters our database (data store) can be a global owner, and everyone else is not.
        4.  We assume that if a user is a channel owner, they are also a channel member.
        5.  We assume that someone will never enter no first name and no last name when registering as a user.
        6.  We assume that someone will never enter a special character as their name, instead their first and last 
            name must be an alphabetic character.
        7.  We assume that the user id is generated from 1 and increments for each user that is added, for example, 
            the first user has id 1, second user has id 2, etc., therefore we also assume no id can be 0 or negative.
        8.  Furthermore we assume that once an user id is made, it cannot be changed.
        9.  Similarly, we assume that the channel id is generated from 1 and increments for each channel that is added,
            fore example, the first channel has id 1, the second has id 2, etc., therefore we also that no channel id can
            be 0 or negative.
        10. Furthmore we assume that once a channel id is made, it cannot be changed.
        11. We assume that the data store is stored as a dictionary with keys whos values are lists of dictionarys. Refer
            to our documentation for our assumed data structure that we have picked. 
        12. Anyone in a public channel can invite others, but 
            -   only the oweners of a private channel can invite others,
            -   gloabl owners/permissions can join both public or private channels and thus they have owner permissions and therefore 
                invite others, but they are not added to the owners list or the members list. This is because we have also assumed
                (Assumption 4) that the only person who is the channel owner is the person who made that channel.

