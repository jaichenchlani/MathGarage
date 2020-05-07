import datastoreoperations, encryptionoperations, utilities, gmail, config
import datetime

# Load Environment
env = config.get_environment_from_env_file()

# Validate username and password
def login(login_credentials):
    print("Entering login..")
    # Declare the output dictionary
    login_response = declare_login_response_dictionary(login_credentials)
    # Validate login against the Password
    entityKind = utilities.get_value_by_entityKind_and_key(env['config_entityKind'],"datastore_kind_users")['config_value']
    login_response['is_valid_login_response'] = isValidLogin("login",entityKind,
        login_credentials['username'].lower(),
        login_credentials['password'])
    # Take the password and forgot password question/answer off from the response     
    if login_response['is_valid_login_response']['userDetails']:
        login_response['is_valid_login_response']['userDetails']['password'] = None
        login_response['is_valid_login_response']['userDetails']['forgot_password_answer'] = None
    return login_response

# Helper function for login
def declare_login_response_dictionary(login_credentials):
    print("Entering declare_login_response_dictionary..")
    login_response = {}
    login_response['login_credentials'] = login_credentials
    login_response['is_valid_login_response'] = {}
    return login_response

# Reset password functionality. 
# Send the clear text user password to the registered email id.
def reset_password(login_credentials):
    print("Entering forgot_password..")
    # Declare the output dictionary
    reset_password_response = declare_reset_response_dictionary(login_credentials)
    # Declare the output dictionary
    entityKind = utilities.get_value_by_entityKind_and_key(env['config_entityKind'],"datastore_kind_users")['config_value']
    reset_password_response['is_valid_login_response'] = isValidLogin("reset_password",entityKind,
        login_credentials['username'].lower(),
        login_credentials['forgot_password_answer'])
    # Check if the user got authenticate from isValidLogin
    if not reset_password_response['is_valid_login_response']['userDetails']:
        reset_password_response['result'] = False
        reset_password_response['message'] = "Invlid response from isValidLogin."
        return reset_password_response

    # Get the email attributes from Config
    email_attributes = utilities.get_value_by_entityKind_and_key(env['config_entityKind'],"email_attributes")['config_value']
    # Send the email with the password in clear text
    emailTo = reset_password_response['is_valid_login_response']['userDetails']['email']
    emailCC = email_attributes['admin_email_id']
    emailSubject = email_attributes['password_reset_email_subject']
    decrypted_password = utilities.decrypt_password(reset_password_response['is_valid_login_response']['userDetails']['password'])['decrypted_password']
    emailBody = "{}\n\n\n{}".format(email_attributes['password_reset_email_body'],decrypted_password)
    email = gmail.send_email(emailTo, emailCC, emailSubject, emailBody)
    if not email['result']:
        reset_password_response['result'] = False
        reset_password_response['message'] = email['message']
        return reset_password_response

    # Take the password and forgot password question/answer off from the response     
    reset_password_response['is_valid_login_response']['userDetails']['password'] = None
    reset_password_response['is_valid_login_response']['userDetails']['forgot_password_answer'] = None
    return reset_password_response

# Helper function for Reset Password
def declare_reset_response_dictionary(login_credentials):
    print("Entering declare_reset_response_dictionary..")
    reset_password_response = {}
    reset_password_response['result'] = True
    reset_password_response['message'] = "Reset password successful."
    reset_password_response['login_credentials'] = login_credentials
    reset_password_response['is_valid_login_response'] = {}
    return reset_password_response

def get_forgot_password_question(login_credentials):
    print("Entering get_forgot_password_question..")
    entityKind = utilities.get_value_by_entityKind_and_key(env['config_entityKind'],"datastore_kind_users")['config_value']
    user = isValidUser(entityKind,login_credentials['username'])
    login_credentials['validOutputReturned'] = user['validOutputReturned']
    login_credentials['isValidUser'] = user['result']
    login_credentials['message'] = user['message']
    if login_credentials['isValidUser']:
        login_credentials['forgot_password_question'] = user['userDetails']['forgot_password_question']
    return login_credentials

def create_account(userInfo):
    print("Entering create_account..")
    # Declare the output dictionary
    create_account_response = declare_create_account_response_dictionary(userInfo)
    entityKind = utilities.get_value_by_entityKind_and_key(env['config_entityKind'],"datastore_kind_users")['config_value']
    create_account_response['created_userInfo'] = create_user(entityKind,userInfo)
    return create_account_response

def declare_create_account_response_dictionary(userInfo):
    print("Entering declare_create_account_response_dictionary..")
    create_account_response = {}
    create_account_response['userInfo'] = userInfo
    create_account_response['created_userInfo'] = {}
    return create_account_response

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
    entityKind = utilities.get_value_by_entityKind_and_key(env['config_entityKind'],"datastore_kind_users")['config_value']
    entityProperty = utilities.get_value_by_entityKind_and_key(env['config_entityKind'],"datastore_property_username")['config_value']
    entityList = datastoreoperations.get_datastore_entity_by_property(entityKind,entityProperty,username.lower())  
    if not entityList['validOutputReturned']:
        # Error returned from get_datastore_entity_by_property
        response['message'] = entityList['message']
        # Return. Don't move forward.
        return response

    # Valid response returned from get_datastore_entity_by_property
    number_of_records = 0
    for entity in entityList['entityList']:
        username = entity['username']
        password = entity['password']
        id = entity.key.id
        first_name = entity['first_name']
        last_name = entity['last_name']
        email = entity['email']
        forgot_password_question = entity['forgot_password_question']
        forgot_password_answer = entity['forgot_password_answer']
        create_timestamp = entity['create_timestamp'],
        last_logged_timestamp = entity['last_logged_timestamp'],
        last_modified_timestamp = entity['last_modified_timestamp']
        number_of_records += 1

    if number_of_records == 0:
        # User record does not exist. 
        response['message'] = "User does not exist in DB."
        # Return. Don't move forward.
        return response
        
    if number_of_records > 1:
        # More than 1 records exist in the DB. Something wrong. Return False.
        response['message'] = "Multiple records exist for the user in DB. Invalid User."
        # Return. Don't move forward.
        return response
    
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
            "forgot_password_question": forgot_password_question,
            "forgot_password_answer": forgot_password_answer,
            "create_timestamp": create_timestamp,
            "last_logged_timestamp": last_logged_timestamp,
            "last_modified_timestamp": last_modified_timestamp
        }
    }
    return response

def isValidLogin(callingFrom,entityKind,username,password):
    print("Entering isValidLogin...")
    login_user_message_codes = utilities.get_value_by_entityKind_and_key(env['config_entityKind'],"login_user_message_codes")['config_value']
    # Initialize the response dictionary
    response = {
        "result": login_user_message_codes['login_failure'],
        "message": "",
        "validOutputReturned": True,
        "userDetails": {}
    }

    user = isValidUser(entityKind,username)
    print(user)
    if not user['validOutputReturned']:
        # Error returned from isValidUser. 
        response['message'] = user['message']
        response['validOutputReturned'] = False
        response['result'] = login_user_message_codes['login_server_error']
        # Return. Don't move forward.
        return response
    
    # Valid response returned from isValidUser.
    if not user['result']:
        # Invalid User. Return False.
        response['message'] = user['message']
        response['result'] = login_user_message_codes['login_user_does_not_exist']
        # Return. Don't move forward.
        return response

    # User is valid. Validate the password.
    # Validate the password against the right password field
    if callingFrom == "login":
        # Calling from login. Validate against "password" field
        dbPassword = utilities.decrypt_password(user['userDetails']['password'])['decrypted_password']
    else:
        # Calling from login. Validate against "forgot_password_answer" field
        dbPassword = utilities.decrypt_password(user['userDetails']['forgot_password_answer'])['decrypted_password']

    if not dbPassword == password:
        # Incorrect password. Return False
        response['message'] = utilities.get_value_by_entityKind_and_key(env['config_entityKind'],"login_failure_message")['config_value']
        response['result'] = login_user_message_codes['login_failure']
        # Return. Don't move forward.
        return response

    # All good. Valid user, correct password. Return True
    response = {
        "result": login_user_message_codes['login_success'],
        "message": utilities.get_value_by_entityKind_and_key(env['config_entityKind'],"login_success_message")['config_value'],
        "validOutputReturned": True,
        "userDetails": user['userDetails']
    }  
    return response

def create_user(entityKind,user_details):
    print("Entering create_user...")
    # Initialize the response dictionary
    response = {
        "result": True,
        "datastore_id": None,
        # "userDetails": {},
        "message": "User created in the DB.",
        "validOutputReturned": True
    }
    # Validate User Data
    attribute_validation = validate_user_attributes(user_details)
    if not attribute_validation['validOutputReturned']:
        # Error returned from validate_user_attributes
        response['message'] = attribute_validation['message']
        response['validOutputReturned'] = False
        response['result'] = False
        # Return. Don't move forward.
        return response

    # Valid output returned from validate_user_attributes
    if not attribute_validation['result']:
        # Invalid attributes.
        response['message'] = attribute_validation['message']
        response['result'] = False
        # Return. Don't move forward.
        return response

    # All attributes are valid. Check whether the user is already in the DB.
    if isValidUser(entityKind,user_details['username'].lower())['result']:
    # User already exists in the DB. Cannot create.
        response['message'] = "Cannot create user. User already exists."
        response['result'] = False
        # Return. Don't move forward.
        return response

    # All good. Proceed with creating user in datastore    
    user_entity = {
            # username should always be stored in lowercase.
            "username": user_details['username'].lower(),
            "password": utilities.encrypt_password(user_details['password'])['encrypted_password'],
            # first_name and last_name should be first letter capital
            "first_name": user_details['first_name'].title(),
            "last_name": user_details['last_name'].title(),
            # email should always be stored in lowercase.
            "email": user_details['email'].lower(),
            "forgot_password_question": user_details['forgot_password_question'],
            "forgot_password_answer": utilities.encrypt_password(user_details['forgot_password_answer'])['encrypted_password'],
            "active": True,
            "create_timestamp": datetime.datetime.now(),
            "last_logged_timestamp": datetime.datetime.now(),
            "last_modified_timestamp": datetime.datetime.now()
        }
    entityKind = utilities.get_value_by_entityKind_and_key(env['config_entityKind'],"datastore_kind_users")['config_value']
    entity = datastoreoperations.create_datastore_entity(entityKind,user_entity)
    if not entity['validOutputReturned']:
        # Error returned from create_datastore_entity
        response['message'] = entity['message']
        response['validOutputReturned'] = False
        response['result'] = False
        # Return. Don't move forward.
        return response

    # Valid output returned from create_datastore_entity
    response['datastore_id'] = entity['entity'].key.id
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
    user = isValidUser(entityKind,username.lower())
    if not user['validOutputReturned']:
        # Error returned from isValidUser. Cannot delete.
        response['message'] = user['message']
        response['validOutputReturned'] = False
        # Return. Don't move forward.
        return response

    # Valid output returned from isValidUser
    if not user['result']:
        # User does not exist. Cannot update.
        response['message'] = user['message']
        # Return. Don't move forward.
        return response

    # User exists. Go ahead with delete.
    id = user['userDetails']['id']
    flag_user_hard_delete = utilities.get_value_by_entityKind_and_key(env['config_entityKind'],"flag_user_hard_delete")['config_value']
    if flag_user_hard_delete:
        # HARD delete from Datastore
        entityKind = utilities.get_value_by_entityKind_and_key(env['config_entityKind'],"datastore_kind_users")['config_value']
        delete_user = datastoreoperations.delete_datastore_entity(entityKind,id)
        if not delete_user['validOutputReturned']:
            # Error returned from delete_user
            response['message'] = delete_user['message']
            response['validOutputReturned'] = False
        else:
            # Valid output returned from delete_user
            response['message'] = "User HARD deleted from the DB."
            response['result'] = True
        return response

    if not flag_user_hard_delete:
        # SOFT delete from Datastore
        # Update the Active flag to False in Datastore
        updated_user = {
            "active": False
        }
        entityKind = utilities.get_value_by_entityKind_and_key(env['config_entityKind'],"datastore_kind_users")['config_value']
        updated_user = datastoreoperations.update_datastore_entity(entityKind,id,updated_user)
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
    # Get the User attributes from Config
    user_attributes = utilities.get_value_by_entityKind_and_key(env['config_entityKind'],"user_attributes")['config_value']
    # Initialize the response dictionary
    response = {
        "result": False,
        "message": "",
        "validOutputReturned": True
    }
    if user_details['username'] is None or user_details['username'] == "":
        response['message'] = "Invalid attribute. Username missing."
    elif len(user_details['username']) < user_attributes['username_minimum_length']:
        response['message'] = "Invalid attribute. Username should be atleast {} characters.".format(user_attributes['username_minimum_length'])
    elif user_details['password'] is None  or user_details['password'] == "":
        response['message'] = "Invalid attribute. password missing."
    elif len(user_details['password']) < user_attributes['password_minimum_length']:
        response['message'] = "Invalid attribute. Password should be atleast {}} characters.".format(user_attributes['password_minimum_length'])
    elif user_details['first_name'] is None or user_details['first_name'] == "":
        response['message'] = "Invalid attribute. First Name missing."
    elif user_details['last_name'] is None  or user_details['last_name'] == "":
        response['message'] = "Invalid attribute. Last Name missing."
    elif user_details['email'] is None  or user_details['email'] == "":
        response['message'] = "Invalid attribute. email missing."
    elif not utilities.isValidEmail(user_details['email'])['result']:
        response['message'] = utilities.isValidEmail(user_details['email'])['message']
    elif user_details['forgot_password_question'] is None  or user_details['forgot_password_question'] == "":
        response['message'] = "Invalid attribute. Forgot Password Question missing."
    elif len(user_details['forgot_password_question']) < user_attributes['forgot_password_question_minimum_length']:
        response['message'] = "Invalid attribute. Forgot Password Question should be atleast {} characters.".format(user_attributes['forgot_password_question_minimum_length'])
    elif user_details['forgot_password_answer'] is None  or user_details['forgot_password_answer'] == "":
        response['message'] = "Invalid attribute. Forgot Password Answer missing."
    elif len(user_details['forgot_password_answer']) < user_attributes['forgot_password_answer_minimum_length']:
        response['message'] = "Invalid attribute. Forgot Password Answer should be atleast {} characters.".format(user_attributes['forgot_password_answer_minimum_length'])
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
    # Validate User Data
    attribute_validation = validate_user_attributes(user_details)
    if not attribute_validation['validOutputReturned']:
        # Error returned from validate_user_attributes
        response['message'] = attribute_validation['message']
        response['validOutputReturned'] = False
        # Return. Don't move forward.
        return response
    
    # Valid output returned from validate_user_attributes
    if not attribute_validation['result']:
        # Attribute validation result failed. Cannot proceed with update.
        response['message'] = attribute_validation['message']
        # Return. Don't move forward.
        return response

    # All attributes are valid. 
    # Check whether the user is already in the DB.
    user = isValidUser(entityKind,user_details['username'].lower())
    if not user['validOutputReturned']:
        # Error returned from isValidUser
        response['message'] = user['message']
        # Return. Don't move forward.
        return response
    
    # Valid output returned from isValidUser
    if not user['result']:
        # User does not exist. Cannot update.
        response['message'] = user['message']
        # Return. Don't move forward.
        return response

    # User exists; proceed with update.
    id = user['userDetails']['id']
    updated_user_entity = {
            # username should always be stored in lowercase.
            "username": user_details['username'].lower(),
            "password": user_details['password'],
            # first_name and last_name should always be stored with first letter Capital.
            "first_name": user_details['first_name'].title(),
            "last_name": user_details['last_name'].title(),
            # email should always be stored in lowercase.
            "email": user_details['email'].lower(),
            "forgot_password_question": user_details['forgot_password_question'],
            "forgot_password_answer": user_details['forgot_password_answer'],
            "active": True,
            "last_modified_timestamp": datetime.datetime.now()
        }
    entityKind = utilities.get_value_by_entityKind_and_key(env['config_entityKind'],"datastore_kind_users")['config_value']
    entity = datastoreoperations.update_datastore_entity(entityKind,id,updated_user_entity)
    if not entity['validOutputReturned']:
        # Error returned from update_datastore_entity
        response['message'] = entity['message']
        # Return. Don't move forward.
        return response
    
    # Valid output returned from update_datastore_entity
    response['message'] = "User updated successfully in the DB."
    response['entity'] = entity['entity']
    
    return response