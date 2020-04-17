from google.cloud import datastore

# Shortlist the valid list items from the superset list based on difficulty level
def identify_valid_items_in_list(allItemsInList,difficultyLevel):
    validItemsInList = []
    for config in allItemsInList:
        if difficultyLevel[config['difficulty_level']] == 1:
            if int(config['active']):
                validItemsInList.append(config)
    return validItemsInList

# Validate whether the passed string is a valid integer, and return a boolean result
def is_valid_integer(str_number):
    # Validate 1st_number_lower_limit to be an Integer
    try:
        temp_int_variable = int(str_number)
    except ValueError:
        return False

    return True

def create_datastore_entity(entityKind,entityObject):
    # Create, populate and persist an entity with keyID passed as argument
    client = datastore.Client()
    key = client.key(entityKind)
    entity = datastore.Entity(key=key)
    entity.update(entityObject)
    client.put(entity)