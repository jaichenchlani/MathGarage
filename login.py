from config import read_configurations_from_config_file
from datastoreoperations import create_datastore_entity, get_datastore_entity_by_property, delete_datastore_entity, update_datastore_entity
import datetime
from utilities import isValidEmail

# Load Defaults from Config
envVariables = read_configurations_from_config_file()
login_failure_message = envVariables['login_failure_message']
login_success_message = envVariables['login_success_message']
entityKind = envVariables['datastore_kind_users']
entityProperty = envVariables['datastore_property_username']
flag_user_hard_delete = envVariables['flag_user_hard_delete']

def login(login_credentials):
    print("Entering login..")

    login_response = isValidLogin(entityKind,login_credentials['username'],login_credentials['password'])
    return login_response

def isValidUser(entityKind,username):
    print("Entering isValidUser...")
    # Initialize the response dictionary
    response = {
        "result": False,
        "message": "",
        "validOutputReturned": True,
        "userDetails": {}
    }
    # Fetch entity from the datastore by property
    entity = get_datastore_entity_by_property(entityKind,entityProperty,username)  
    if not entity['validOutputReturned']:
        # Error returned from get_datastore_entity_by_property
        response['message'] = entity['message']
    else:
        # Valid response returned from get_datastore_entity_by_property
        number_of_records = 0
        for entity in entity['entityList']:
            username = entity['username']
            password = entity['password']
            id = entity.key.id
            first_name = entity['first_name']
            last_name = entity['last_name']
            email = entity['email']
            create_timestamp = entity['create_timestamp'],
            last_logged_timestamp = ['last_logged_timestamp'],
            last_modified_timestamp = ['last_modified_timestamp']
            number_of_records += 1

        if number_of_records == 0:
            # User record does not exist. Return False
            response['message'] = "User does not exist in DB."
        elif number_of_records > 1:
            # More than 1 records exist in the DB. Something wrong. Return False.
            response['message'] = "Multiple records exist for the user in DB. Invalid User."
        else:
            # Valid User. Build the response dictionary.
            response = {
                "result": True,
                "message": "Valid User.",
                "validOutputReturned": True,
                "userDetails": {
                    "id": id,
                    "username": username,
                    "password": password,
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "create_timestamp": create_timestamp,
                    "last_logged_timestamp": last_logged_timestamp,
                    "last_modified_timestamp": last_modified_timestamp
                }
            }
    return response

def isValidLogin(entityKind,username,password):
    print("Entering isValidLogin...")
    # Initialize the response dictionary
    response = {
        "result": False,
        "message": "",
        "validOutputReturned": True,
        "userDetails": {}
    }
    user = isValidUser(entityKind,username)
    if not user['result']:
        # Invalid User. Return False.
        response['message'] = user['message']
    else:
        # User is valid. Validate the password.
        if not user['userDetails']['password'] == password:
            # Incorrect password. Return False
            response['message'] = login_failure_message
        else:
             # All good. Valid user, correct password. Return True
            response = {
                "result": True,
                "message": login_success_message,
                "validOutputReturned": True,
                "userDetails": user['userDetails']
            }  
    return response

def create_user(entityKind,user_details):
    print("Entering create_user...")
    # Initialize the response dictionary
    response = {
        "entity": None,
        "message": "",
        "validOutputReturned": True,
        "userDetails": {}
    }
    # Validate User Data: Username, Password, First Name, Last Name and Email are mandatory fields.
    attribute_validation = validate_user_attributes(user_details)
    if not attribute_validation['validOutputReturned']:
        # Error returned from validate_user_attributes
        response['message'] = attribute_validation['message']
        response['validOutputReturned'] = False
    else:
        # Valid output returned from validate_user_attributes
        response['message'] = attribute_validation['message']
        if attribute_validation['result']:
            # All attributes are valid. Check whether the user is already in the DB.
            if isValidUser(entityKind,user_details['username'])['result']:
            # User already exists in the DB. Cannot create.
                response['message'] = "Cannot create user. User already exists."
            else:
                user_entity = {
                        "username": user_details['username'],
                        "password": user_details['password'],
                        "first_name": user_details['first_name'],
                        "last_name": user_details['last_name'],
                        "email": user_details['email'],
                        "active": True,
                        "create_timestamp": datetime.datetime.now(),
                        "last_logged_timestamp": datetime.datetime.now(),
                        "last_modified_timestamp": datetime.datetime.now()
                    }
                entity = create_datastore_entity(entityKind,user_entity)
                if not entity['validOutputReturned']:
                    # Error returned from create_datastore_entity
                    response['message'] = entity['message']
                else:
                    # Valid output returned from create_datastore_entity
                    response['entity'] = entity['entity']

    return response
        
def delete_user(entityKind,username):
    print("Entering delete_user...")
    # Initialize the response dictionary
    response = {
        "result": False,
        "message": "",
        "validOutputReturned": True
    }
    # Check whether user exists, and fetch the ID.
    user = isValidUser(entityKind,username)
    if not user['validOutputReturned']:
        # User does not exist in the DB. Cannot delete.
        response['message'] = user['message']
    else:
        # User exists. Go ahead with delete.
        id = user['userDetails']['id']
        if flag_user_hard_delete:
            # HARD delete from Datastore
            delete_user = delete_datastore_entity(entityKind,id)
            if not delete_user['validOutputReturned']:
                # Error returned from delete_user
                response['message'] = delete_user['message']
                response['validOutputReturned'] = False
            else:
                # Valid output returned from delete_user
                response['message'] = "User HARD deleted from the DB."
                response['result'] = True
        else:
            # SOFT delete from Datastore
            # Update the Active flag to False in Datastore
            updated_user = {
                "active": False
            }
            updated_user = update_datastore_entity(entityKind,id,updated_user)
            if not updated_user['validOutputReturned']:
                # Error returned from update_datastore_entity
                response['message'] = updated_user['message']
                response['validOutputReturned'] = False
            else:
                # Valid output returned from update_datastore_entity
                response['message'] = "User SOFT deleted from the DB."
                response['result'] = True
        
    return response

def validate_user_attributes(user_details):
    print("Entering validate_user_attributes...")
    # Initialize the response dictionary
    response = {
        "result": False,
        "message": "",
        "validOutputReturned": True
    }
    if user_details['username'] is None or user_details['username'] == "":
        response['message'] = "Cannot create user. Username missing."
    elif user_details['password'] is None  or user_details['password'] == "":
        response['message'] = "Cannot create user. password missing."
    elif len(user_details['password']) < 8:
        response['message'] = "Cannot create user. password should be atleast 8 characters."
    elif user_details['first_name'] is None or user_details['first_name'] == "":
        response['message'] = "Cannot create user. First Name missing."
    elif user_details['last_name'] is None  or user_details['last_name'] == "":
        response['message'] = "Cannot create user. Last Name missing."
    elif user_details['email'] is None  or user_details['email'] == "":
        response['message'] = "Cannot create user. email missing."
    elif not isValidEmail(user_details['email'])['result']:
        response['message'] = isValidEmail(user_details['email'])['message']
    else:
        response['message'] = "All attributes are valid."
        response['result'] = True

    return response

def update_user(entityKind,user_details):
    print("Entering update_user...")
    # Initialize the response dictionary
    response = {
        "entity": None,
        "message": "",
        "validOutputReturned": True,
        "userDetails": {}
    }
    # Validate User Data: Username, Password, First Name, Last Name and Email are mandatory fields.
    attribute_validation = validate_user_attributes(user_details)
    if not attribute_validation['validOutputReturned']:
        # Error returned from validate_user_attributes
        response['message'] = attribute_validation['message']
        response['validOutputReturned'] = False
    else:
        # Valid output returned from validate_user_attributes
        response['message'] = attribute_validation['message']
        if attribute_validation['result']:
            # All attributes are valid. Go ahead with updating the User in Datastore.
            updated_user_entity = {
                    "username": user_details['username'],
                    "password": user_details['password'],
                    "first_name": user_details['first_name'],
                    "last_name": user_details['last_name'],
                    "email": user_details['email'],
                    "active": True,
                    "last_modified_timestamp": datetime.datetime.now()
                }
            # entity = create_datastore_entity(entityKind,user_entity)
            entity = update_datastore_entity(entityKind,id,updated_user_entity)
            if not entity['validOutputReturned']:
                # Error returned from create_datastore_entity
                response['message'] = entity['message']
            else:
                # Valid output returned from create_datastore_entity
                response['message'] = "User updated successfully in the DB."
                response['entity'] = entity['entity']
    return response