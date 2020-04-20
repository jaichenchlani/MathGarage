from google.cloud import datastore
import os

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