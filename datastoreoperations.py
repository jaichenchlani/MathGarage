from google.cloud import datastore
import os
import datetime
from config import read_configurations_from_config_file

# Load Defaults from Config
envVariables = read_configurations_from_config_file()
credential_key_file = envVariables['credential_key_file']

# Create the datastore client to be used by all functions
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_key_file
client = datastore.Client()

# Create, populate and persist an entity with keyID passed as argument
def create_datastore_entity(entityKind,entityObject):
    print("Entering create_datastore_entity...")
    # Initialize the response dictionary
    response = {
        "entity": None,
        "message": "",
        "validOutputReturned": True
    }
    try:
        # Perform the DB operation
        key = client.key(entityKind)
        entity = datastore.Entity(key=key)
        entity.update(entityObject)
        client.put(entity)
    except Exception as e:
        # Error performing the DB operation
        errorMessage = "Error creating datastore entity."
        errorMessage = "{0} Stacktrace: {1}".format(errorMessage,e)
        print(errorMessage)
        response['message'] = errorMessage
        response['validOutputReturned'] = False
        
    response['entity'] = entity

    return response

# Delete an entity by ID. Return success indicator and corresponding message.
def delete_datastore_entity(entityKind,id):
    print("Entering delete_datastore_entity...")
    # Initialize the response dictionary
    response = {
        "result": False,
        "message": "",
        "validOutputReturned": True
    }
    # Fetch the entity from datastore
    entity = get_datastore_entity(entityKind,id)
    if not entity['validOutputReturned']:
        # Error returned from get_datastore_entity
        response['message'] = entity['message']
    else:
        # Valid response returned from get_datastore_entity
        if not entity['entity']:
            # Entity does not exist. 
            response['message'] = "Entity does not exist in the DB."
        else:
            # Entity exists. Go ahead with Deletion
            try:
                # Perform the DB operation
                key = client.key(entityKind,id)
                client.delete(key)
            except Exception as e:
                # Error performing the DB operation
                errorMessage = "Error deleting datastore entity."
                errorMessage = "{0} Stacktrace: {1}".format(errorMessage,e)
                print(errorMessage)
                response['message'] = errorMessage
                response['validOutputReturned'] = False

    # Update the success message in the response dictionary.
    response['result'] = True
    return response

# Update single/multiple properties of an entity. 
# Return success indicator and corresponding message.
def update_datastore_entity(entityKind,id,updatedEntity):
    print("Entering update_datastore_entity...")
    # Initialize the response dictionary
    response = {
        "entity": None,
        "message": "",
        "validOutputReturned": True
    }
    # Fetch the entity from datastore
    entity = get_datastore_entity(entityKind,id)
    if not entity['validOutputReturned']:
        # Error returned from get_datastore_entity
        response = {
            "result": False,
            "message": entity['message'],
            "validOutputReturned": False
        }
    else:
        # Valid response returned from get_datastore_entity
        try:
            # Perform the DB update operation
            # Update the entity returned from the fetch, with the updatedEntity from arguments
            entity['entity'].update(updatedEntity)
            client.put(entity['entity'])
        except Exception as e:
            # Error performing the DB operation
            errorMessage = "Error updating the entity in datstore."
            errorMessage = "{0} Stacktrace: {1}".format(errorMessage,e)
            print(errorMessage)
            response['result'] = False
            response['message'] = errorMessage
            response['validOutputReturned'] = False

    response['entity'] = entity['entity']
    return response

# Fetch an entity by ID
def get_datastore_entity(entityKind,id):
    print("Entering get_datastore_entity...")
    # Initialize the response dictionary
    response = {
        "entity": None,
        "message": "",
        "validOutputReturned": True
    }
    try:
        # Perform the DB operation
        key = client.key(entityKind,id)
        entity = client.get(key)
    except Exception as e:
        # Error performing the DB operation
        errorMessage = "Error fetching datastore entity."
        errorMessage = "{0} Stacktrace: {1}".format(errorMessage,e)
        print(errorMessage)
        response['message'] = errorMessage
        response['validOutputReturned'] = False
    
    response['entity'] = entity
    return response

# Return the list of all the entities in the supplied Kind.
def get_datastore_entities_by_kind(entityKind):
    print("Entering get_datastore_entities_by_kind...")
    # Initialize the response dictionary
    response = {
        "entityList": None,
        "message": "",
        "validOutputReturned": True
    }
    try:
        # Perform the DB operation
        query = client.query(kind=entityKind)
    except Exception as e:
        # Error performing the DB operation
        errorMessage = "Error fetching datastore entity list."
        errorMessage = "{0} Stacktrace: {1}".format(errorMessage,e)
        print(errorMessage)
        response['message'] = errorMessage
        response['validOutputReturned'] = False
    response['entityList'] = list(query.fetch())
    return response

# Fetch an entity by a property
def get_datastore_entity_by_property(entityKind,propertyKey,propertyValue):
    print("Entering get_datastore_entity_by_property...")
    # Initialize the response dictionary
    response = {
        "entityList": [],
        "message": "",
        "validOutputReturned": True
    }
    try:
        query = client.query(kind=entityKind)
        query = query.add_filter(propertyKey, '=', propertyValue)
        query_iter = query.fetch()
    except Exception as e:
        # Error performing the DB operation
        errorMessage = "Error fetching user from the DB."
        errorMessage = "{0} Stacktrace: {1}".format(errorMessage,e)
        print(errorMessage)
        response['message'] = errorMessage
        response['validOutputReturned'] = False
    
    # response['entity'] = query_iter
    response['entityList'] = list(query_iter)
    return response

