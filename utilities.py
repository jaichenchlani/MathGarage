from google.cloud import datastore
import os, re, datetime
import datastoreoperations, encryptionoperations
from config import read_configurations_from_config_file


# Load Defaults from Config
envVariables = read_configurations_from_config_file()
password_vault_entityKind = envVariables['password_vault_entityKind']
password_vault_account_field_name = envVariables['password_vault_account_field_name']

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
    except Exception as e:
        errorMessage = "Pattern match operation failed."
        errorMessage = "{0} Stacktrace: {1}".format(errorMessage,e)
        print(errorMessage)
        response['message'] = errorMessage
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
    entity = datastoreoperations.create_datastore_entity(entityKind,entity)
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
    entity = datastoreoperations.update_datastore_entity(entityKind,id,updated_entity)
    
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


def create_password_in_password_vault(account,password):
    print("Entering password_in_password_vault...")
    encryption = encrypt_password(password)
    # print("encryption:{},{}".format(encryption,type(encryption)))
    encrypted_password = encryption['encrypted_password']
    # print("encrypted_password:{},{}".format(encrypted_password,type(encrypted_password)))

    # Create Password Vault Entry
    password_valut_entity = {
        "account": account,
        "password": encrypted_password
    }
    # Create a datastore entry with the encrypted password.
    datastoreoperations.create_datastore_entity(password_vault_entityKind,password_valut_entity)


def get_password_from_password_vault(account_value):
    print("Entering get_password_from_password_vault...")
    # Password Vault Entity
    entityKind = password_vault_entityKind
    # Configuted field name from Config
    propertyKey = password_vault_account_field_name
    # Passed argument
    propertyValue = account_value
    # Fetch the datastore operation function to get the password and return

    entityList = datastoreoperations.get_datastore_entity_by_property(entityKind,propertyKey,propertyValue)
    encrypted_password = entityList['entityList'][0]['password']

    # Decrypt the password
    decryption = decrypt_password(encrypted_password)
    # print("decryption:{},{}".format(decryption,type(decryption)))
    decrypted_password = decryption['decrypted_password']
    # print("decrypted_password:{},{}".format(decrypted_password,type(decrypted_password)))

    return decrypted_password

def encrypt_password(plaintext_password):
    print("Entering encrypt_password...")
    # Initialize the response dictionary
    response = {
        "encrypted_password": None,
        "message": "Password encryption successful.",
        "validOutputReturned": True,
    }
    encryption = encryptionoperations.encrypt_symmetric(plaintext_password)
    if not encryption['validOutputReturned']:
        # Error returned from encrypt_symmetric
        response['message'] = encryption['message']
        # Return. Don't move forward.
        return response

    if not encryption['result']:
        # Invalid output returned from encrypt_symmetric
        response['message'] = encryption['message']
        # Return. Don't move forward.
        return response
    # All good. Return the response dictionary
    response['encrypted_password'] = encryption['ciphertext']
    return response
    
def decrypt_password(encrypted_password):
    print("Entering decrypt_password...")
    # Initialize the response dictionary
    response = {
        "decrypted_password": None,
        "message": "Password decryption successful.",
        "validOutputReturned": True,
    }
    decryption = encryptionoperations.decrypt_symmetric(encrypted_password)
    if not decryption['validOutputReturned']:
        # Error returned from encrypt_symmetric
        response['message'] = decryption['message']
        # Return. Don't move forward.
        return response

    if not decryption['result']:
        # Invalid output returned from encrypt_symmetric
        response['message'] = decryption['message']
        # Return. Don't move forward.
        return response
        
    # All good. Return the response dictionary
    response['decrypted_password'] = decryption['plaintext']
    return response