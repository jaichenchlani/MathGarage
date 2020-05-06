import utilities, datastoreoperations
import json
from config import read_configurations_from_config_file

# Load Defaults from Config
envVariables = read_configurations_from_config_file()
entityKind = envVariables['config_entityKind']

def update_datastore_config_from_json(entityKind):
    print("Entering update_config...")
    # Process
    count = 0
    for (key,value) in envVariables.items():
        # Check whether the key already exists in the DB.
        entity = utilities.read_datastore_and_get_id(entityKind,"key",key)
        # if not entity['validOutputReturned']:
        #     # Not a valid output from read_datastore_and_get_id. Print message and proceed.
        #     print(entity['message'])
        if not entity['id']:
            # Key not found. Create.
            create = utilities.create_key_value_pair_in_datastore(entityKind,key,value)
            print(create)
            count += 1
        elif entity['id']:
            # Key found. Update.
            updatedEntity = {
                "key": key,
                "value": value
            }
            update = datastoreoperations.update_datastore_entity(entityKind,entity['id'],updatedEntity)
            print(update)
        else:
            # Will never get here.
            pass

    print("Process completed. Updated {} entities in Datastore.".format(count)) 

def download_datastore_kind_into_json(entityKind, filename):
    print("Entering download_datastore_kind_into_json...")
    # Process
    json_dictionary = {}
    count = 0

    entities = datastoreoperations.get_datastore_entities_by_kind(entityKind)
    if not entities['validOutputReturned']:
        # Error returned from get_datastore_entities_by_kind
        print(entities['message'])
    else:
        # Got the list of entities. Build dictionary.
        for entity in entities['entityList']:
            json_dictionary[entity['key']] = entity['value']
            count += 1
    
    try:
        with open(filename, 'w') as outfile:
            json.dump(json_dictionary, outfile)
    except Exception as e:
        # Error performing the File operation
        errorMessage = "Error creating the output json file."
        errorMessage = "{0} Stacktrace: {1}".format(errorMessage,e)
        print(errorMessage)
    
    print("Process completed. Downloaded {} entities from Datastore in the json file {}.".format(count,filename)) 

# update_datastore_config_from_json(entityKind)
download_datastore_kind_into_json(entityKind,"prodconfig.json")