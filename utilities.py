from google.cloud import datastore
import os, re, datetime
from datastoreoperations import create_datastore_entity, update_datastore_entity

# Shortlist the valid list items from the superset list based on difficulty level
def identify_valid_items_in_list(allItemsInList,difficultyLevel):
    validItemsInList = []
    for config in allItemsInList:
        if difficultyLevel[config['difficulty_level']] == 1:
            if int(config['active']):
                validItemsInList.append(config)
    return validItemsInList

def isValidEmail(email):
    email_rules = [
        "Account, Domain and Domain extension must contain alphanumeric characters only",
        "Account, Domain and Domain extension should be atleast 3 characters in length",
        "Domain extension should be atleast 2 characters in length",
        "Must contain an '@' symbol between Account and Domain",
        "Must contain a '.' between Domain and Domain Extension"
    ]
    print("Entering isValidEmail...")
    # Initialize the response dictionary
    response = {
        "result": False,
        "message": {},
        "validOutputReturned": True
    }
    pattern = re.compile('^[a-zA-Z0-9]{3,}@[a-zA-Z0-9]{3,}\.[a-zA-Z0-9]{2,}')
    try:
        patternMatch = re.search(pattern, email)
    except:
        response['message'] = "Pattern match operation failed."
        response['validOutputReturned'] = False

    if not patternMatch:
        response['message'] = {
            "text": "Invalid email. Failed pattern match. See email rules.",
            "email_rules": email_rules
        }
    else:
        response['result'] = True
        response['message'] = {
            "text": "Valid email per the email rules.",
            "email_rules": email_rules
        }

    return response

def insert_in_datastore_and_get_id(entityKind,entity):
    print("Entering insert_in_datastore_and_get_id...")
    # Initialize the response dictionary
    response = {
        "id": 0,
        "message": "",
        "validOutputReturned": True
    }
    entity = create_datastore_entity(entityKind,entity)
    if not entity['validOutputReturned']:
        # Error creating datastore entity
        response['validOutputReturned'] = False
        response['message'] = entity['message']
        # Return. Don't move forward.
        return response
    
    id = entity['entity'].key.id
    # entity['datastore_id'] = id
    # Update the Datastore ID in Datastore
    updated_entity = {
        "last_modified_timestamp": datetime.datetime.now(),
        "datastore_id": id
        }
    entity = update_datastore_entity(entityKind,id,updated_entity)
    
    if not entity['validOutputReturned']:
        # Error creating datastore entity
        response['validOutputReturned'] = False
        response['message'] = entity['message']
        # Return. Don't move forward.
        return response

    # Update the Datastore ID in the Output Dictionary
    response['id'] = entity['entity'].key.id
    response['message'] = "Successfully inserted into the Datastore."
    return response