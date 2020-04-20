from google.cloud import datastore
import os
import datetime

# Create, populate and persist an entity with keyID passed as argument
def create_datastore_entity(entityKind,entityObject):
    print("Entering create_datastore_entity...")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "keys/Credentials.json"
    client = datastore.Client()
    key = client.key(entityKind)
    entity = datastore.Entity(key=key)
    entity.update(entityObject)
    client.put(entity)
    # Update Datastore ID in datastore_id property
    id = entity.key.id
    updated_entity = {
    "last_modified_timestamp": datetime.datetime.now(),
    "datastore_id": id
    }
    status = update_datastore_entity(entityKind,id,updated_entity)
    if not status['success_indicator']:
        entity = None
        
    return entity

# Delete an entity by ID. Return success indicator and corresponding message.
def delete_datastore_entity(entityKind,id):
    print("Entering delete_datastore_entity...")
    return_object = {
        "message": "",
        "success_indicator": True
    }
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "keys/Credentials.json"
    client = datastore.Client()
    entity = get_datastore_entity(entityKind,id)
    if entity == None:
        # Entity does not exist.
        return_object = {
            "message": "Entity {} does not exist in Kind {}.".format(id,entityKind),
            "success_indicator": False
        }
    else:
        key = client.key(entityKind,id)
        client.delete(key)
        return_object = {
            "message": "Entity {} deleted from Kind {}.".format(id,entityKind),
            "success_indicator": True
        }
    return return_object

# Update single/multiple properties of an entity. 
# Return success indicator and corresponding message.
def update_datastore_entity(entityKind,id,updatedEntity):
    print("Entering update_datastore_entity...")
    return_object = {
        "message": "",
        "success_indicator": True
    }
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "keys/Credentials.json"
    client = datastore.Client()
    entity = get_datastore_entity(entityKind,id)
    if entity == None:
        # Entity does not exist.
        return_object = {
            "message": "Entity {} does not exist in Kind {}.".format(id,entityKind),
            "success_indicator": False
        }
    else:
        entity.update(updatedEntity)
        client.put(entity)
        return_object = {
            "message": "Entity {} updated in Kind {}.".format(id,entityKind),
            "success_indicator": True
        }
    return return_object


# Fetch an entity by ID
def get_datastore_entity(entityKind,id):
    print("Entering get_datastore_entity...")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "keys/Credentials.json"
    client = datastore.Client()
    key = client.key(entityKind,id)
    entity = client.get(key)
    return entity

# Return the list of all the entities in the supplied Kind.
def get_datastore_entities_by_kind(entityKind):
    print("Entering get_datastore_entities_by_kind...")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "keys/Credentials.json"
    client = datastore.Client()
    query = client.query(kind=entityKind)
    return list(query.fetch())
