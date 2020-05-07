import datastoreoperations, utilities, config
import json

# Load Environment
env = config.get_environment_from_env_file()

def update_datastore_config_from_json():
    print("Entering update_config...")
    entityKind = env['config_entityKind']
    envVariables = config.read_configurations_from_config_file()
    # Process
    countTotal = len(envVariables)
    countCreate = 0
    countUpdate = 0
    countNoChange = 0
    for (key,value) in envVariables.items():
        # Check whether the key already exists in the DB.
        read = utilities.read_datastore_and_get_id(entityKind,"key",key)
        if not read['id']:
            # Key not found. Create.
            create = utilities.create_key_value_pair_in_datastore(entityKind,key,value)
            countCreate += 1
        elif read['id']:
            # Key found. 
            # Check whether the json supplied value has changed.
            entity = datastoreoperations.get_datastore_entity(entityKind,read['id'])
            if value == entity['entity']['value']:
                # json supplied value has NOT changed. Update NOT needed.
                pass
            else:
                # json supplied value has changed. Update.
                jsonEntity = {
                    "key": key,
                    "value": value
                }
                update = datastoreoperations.update_datastore_entity(entityKind,read['id'],jsonEntity)
                countUpdate += 1
        else:
            # Will never get here.
            pass
    # Calculate count of no change
    countNoChange = countTotal - countCreate - countUpdate
    print("Process completed. Total Configurations:{}. Created:{}, Updated:{}, No Change:{}.".format(countTotal, countCreate, countUpdate, countNoChange)) 

def download_datastore_kind_into_json():
    print("Entering download_datastore_kind_into_json...")
    entityKind = env['config_entityKind']
    filename = env['config_json']
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

# update_datastore_config_from_json()
download_datastore_kind_into_json()