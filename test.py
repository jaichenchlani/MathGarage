import utilities, login, gmail, config, setup
import datastoreoperations, encryptionoperations, pubsuboperations
import datetime, os
import mathfunctions, dashboard

# Load Environment
env = config.get_environment_from_env_file()

# Test only. Comment out for Production
difficultyLevel = { 
    "supereasy": 1, 
    "easy": 1, 
    "medium": 1, 
    "hard": 1, 
    "superhard": 1
    }
# print("difficultyLevel:{},{}\n\n".format(difficultyLevel, type(difficultyLevel)))

# Test Sequence Puzzle Generator
# for i in range(1,10):
    # puzzle = generate_sequence_puzzle(difficultyLevel)
# print("\nMissing Elements:{}".format(puzzle['config']['missing_elements_count']))
# print("Puzzle:{}\n".format(puzzle['question']))

# Test Linear Equations Generator
# for i in range(1,10):
#     print("Iteration # {}:".format(i))
    # result = generate_linear_equations(difficultyLevel)
#     print("\n")
#     print("Difficulty Level: {}".format(result['config']['difficulty_level']))
#     print("Configuration: {}".format(result['config']['description']))
#     for count, equation in enumerate(result['question'], start=1):
#         print("Equation # {}: {}".format(count, equation))
#     print("Answer: {}\n".format(result['answer']))
#     print("\n")

# Test Basic Arithematic Operations
# operation_request = {
#     "operator": "x",
#     "first_number_lower_limit": -99,
#     "first_number_upper_limit": 99,
#     "second_number_lower_limit": -9,
#     "second_number_upper_limit": 9,
#     "number_of_questions": 6
# }

# for i in range(1,10):
#     basic_arithematic_object = generate_basic_arithmatic_operations(operation_request)
    # # Test creating a Datastore Entity
    # create_datastore_entity("basic_arithematic",basic_arithematic_object)

# for question in response['questions']:
    # print("{} {} {} = {}".format(question['first_number'],question['operator'],question['second_number'],question['answer']))
    
# Test Login
# google_user = {
#     "name": "Jai Chenchlani",
#     "email": "jaichenchlani@gmail.com"
# }
# store_sign_in_info(google_user)

# # Test GCS Interaction
# get_buckets()


# # Test all combined.
# difficultyLevel = { 
#     "supereasy": 1, 
#     "easy": 1, 
#     "medium": 1, 
#     "hard": 1, 
#     "superhard": 1
#     }
# operation_request = {
#     "operator": "x",
#     "first_number_lower_limit": -99,
#     "first_number_upper_limit": 99,
#     "second_number_lower_limit": -9,
#     "second_number_upper_limit": 9,
#     "number_of_questions": 6
# }
# for i in range(1,10):
#     print("\nIteration # {}\n".format(i))
#     basic_arithematic_object = generate_basic_arithmatic_operations(operation_request)
#     puzzle = generate_sequence_puzzle(difficultyLevel)
#     result = generate_linear_equations(difficultyLevel)
#     generated_multiplication_facts = get_multiplication_facts(i+10,10)


# test_object = {
#     "create_timestamp": datetime.datetime.now(),
#     "last_modified_timestamp": datetime.datetime.now(),
#     "first_name": "Sudhir",
#     "last_name": "Chenchlani",
#     "employer": "Mindtree",
#     "year_joined": 2019,
#     "active": True
# }



# Create Datastore Entity
# datastore_entity = create_datastore_entity("test",test_object)
# print("datastore_entity.key.id:{},{}".format(datastore_entity.key.id, type(datastore_entity.key.id)))
# print("datastore_entity.key.kind:{},{}".format(datastore_entity.key.kind, type(datastore_entity.key.kind)))


# Delete Datastore Entity
# entityKind = "linear_equations"
# id = 5078308135895040
# return_object = delete_datastore_entity(entityKind,id)
# print("return_object:{},{}".format(return_object, type(return_object)))

# entityKind = "linear_equations"
# id = 5071950955151360
# datastore_entity = get_datastore_entity(entityKind,id)
# if datastore_entity != None:
#     id = datastore_entity.key.id
#     kind = datastore_entity.key.kind
#     test_item = datastore_entity.items()
#     # print("datastore_entity:{},{}".format(datastore_entity, type(datastore_entity)))
#     print("ID:{},{}".format(id, type(id)))
#     print("Kind:{},{}".format(kind, type(kind)))
#     for (key,value) in test_item:
#         print("{}: {}".format(key, value))
# else:
#     print("Key not found.")

# entityKind = "test"
# id = 5669079989878784
# updated_entity = {
#     "last_name": "Chhatwani",
#     "year_joined": 2021,
#     "last_modified_timestamp": datetime.datetime.now()
# }

# Update Datastore Entity
# return_object = update_datastore_entity(entityKind,id,updated_entity)
# print("return_object:{},{}".format(return_object, type(return_object)))

# # Get Datastore Entities by Kind
# # entity_list = get_datastore_entities_by_kind('linear_equations')
# entity_list = get_datastore_entities_by_kind('sequence_puzzles')
# print("Number of Entities Returned:{}".format(len(entity_list)))
# for entity in entity_list:
#     print("entity:{},{}".format(entity, type(entity)))


# # # Test isEven Function
# for i in range(-20,20):
#     print("{}: {}".format(i,isEven(i)))
# print(isEven("test"))


# # Test isPositive Function
# for i in range(-20,20):
#     print("{}: {}".format(i,isPositive(i)))
# print(isPositive("test"))

# # Test all Math functions in a loop
# for i in range(1,20):
#     print("Processing {}:".format(i))
#     print("isEven:{}".format(isEven(i)))
#     print("isPositive:{}".format(isPositive(i)))
#     print("getBinary:{}".format(getBinary(i)))
#     print("isPrime:{}".format(isPrime(i)))
#     print("getFactors:{}\n".format(getFactors(i)))
#     print("getPrimeFactors:{}\n".format(getPrimeFactors(i)))

# # Test all Math functions for a specific number
# i=9999999
# print("Processing {}:".format(i))
# print("isEven:{}".format(isEven(i)))
# print("isPositive:{}".format(isPositive(i)))
# print("getBinary:{}".format(getBinary(i)))
# print("isPrime:{}".format(isPrime(i)))
# print("getFactors:{}\n".format(getFactors(i)))
# print("getPrimeFactors:{}\n".format(getPrimeFactors(i)))



# # Test the isPrime function
# for i in range(1,200):
#     print("{}: {}".format(i,isPrime(i)))


# # Test the getBinary function
# for i in range(-20,50):
#     print("{}: {}".format(i,getBinary(i)))


# # # Test the changeBase function
# for i in range(2,37):
#     print("1000 Base {}: {}".format(i,changeBase(1000,i)))


# # Test the getPrimeFactors function
# for i in range(-20,50):
#     print("{}: {}".format(i,getPrimeFactors(i)))

# Test get_number_wiki
# print(get_number_wiki(1000))




# # Create Datastore Entity
# datastore_entity = create_datastore_entity("users",admin_user)
# print("datastore_entity.key.id:{},{}".format(datastore_entity.key.id, type(datastore_entity.key.id)))
# print("datastore_entity.key.kind:{},{}".format(datastore_entity.key.kind, type(datastore_entity.key.kind)))

# login_credentials = {
#     "username": "admin",
#     "password": "password"
# }

# return_object = login(login_credentials)
# print(return_object)
# Below is how you access each property of a Datastore Entity
# print(return_object['datastore_entity'][0]['username'])
# print(return_object['datastore_entity'][0]['password'])
# print(return_object['datastore_entity'][0]['create_timestamp'])
# print(return_object['datastore_entity'][0]['last_logged_timestamp'])
# print(return_object['datastore_entity'][0]['last_modified_timestamp'])
# print(return_object['datastore_entity'][0]['first_name'])
# print(return_object['datastore_entity'][0]['last_name'])


# entityKind = "users"
# id = 5167610110935040

# updated_user = {
#     "first_name": "Jai",
#     "last_name": "Chenchlani",
#     "last_modified_timestamp": datetime.datetime.now()
# }

# updated_user = {
#     "active": True
# }

# # Update Datastore Entity
# return_object = update_datastore_entity(entityKind,id,updated_user)
# print("return_object:{},{}".format(return_object, type(return_object)))



# Test Create/Update User
entityKind = "users"

adminUser = {
    "username": "admin",
    "password": "password",
    "first_name": "jai",
    "last_name": "chenchlani",
    "email": "jaichenchlani@gmail.com"
    }

testUser = {
    "username": "testencryption",
    "password": "1234",
    "first_name": "FIRST_NAME_1",
    "last_name": "LAST_name_1",
    "email": "test@mathgarage.com"
    }
# print(create_user(entityKind,testUser))
# print(update_user(entityKind,user))

# id=5652115070386176
# print(get_datastore_entity(entityKind,id))

# Test isValidUser function
# entityKind = "users"
# username = "admin"
# print(isValidUser(entityKind,username))


# # Test delete_user function
# print(delete_user(entityKind,"admin"))

# Test isValidEmail function
# email = "jaichenchlani@gmail.com"
# email = "jaichenchlani@gmail.com"
# email = "test@mathgarage.com"
# print(isValidEmail(email))


# id = 5738420181663744
# entityKind = "users"

# print(delete_datastore_entity(entityKind,id))


# Test isValidLogin function
# entityKind = "users"
# username = "TESt"
# password = "12345678"
# print(isValidLogin(entityKind,username.lower(),password))

# project_id = "mathgarage"
# location_id = "global"
# key_ring_id = "passwords"
# crypto_key_id = "user_password"

# project_id = password_encryption_codes['project_id']
# location_id = password_encryption_codes['location_id']
# key_ring_id = password_encryption_codes['key_ring_id']
# crypto_key_id = password_encryption_codes['crypto_key_id']


# password = "12345678".encode()

# # get_keyrings(PROJECT_ID, LOCATION_ID)
# encrypted_password = encrypt_symmetric(password)
# print("encrypted_password:{},{}".format(encrypted_password,type(encrypted_password)))

# # projects/mathgarage/locations/global/keyRings/test/cryptoKeys/quickstart
# decrypted_password = decrypt_symmetric(encrypted_password['ciphertext'])
# print("decrypted_password:{},{}".format(decrypted_password,type(decrypted_password)))


# password = "12345678"

# print("password:{},{}".format(password,type(password)))

# encryption = encrypt_password(password)
# # print("encryption:{},{}".format(encryption,type(encryption)))
# encrypted_password = encryption['encrypted_password']
# print("encrypted_password:{},{}".format(encrypted_password,type(encrypted_password)))

# decryption = decrypt_password(encrypted_password)
# # print("decryption:{},{}".format(decryption,type(decryption)))

# decrypted_password = decryption['decrypted_password']
# print("decrypted_password:{},{}".format(decrypted_password,type(decrypted_password)))

# # TEST EMAIL
# emailTo = "jai.chenchlani@mindtree.com"
# emailCC = "jaichenchlani@gmail.com"
# emailSubject = "Test Email Utility"
# emailBody = "Test Email Body"
# gmail.send_email(emailTo, emailCC, emailSubject, emailBody)

# "password": "CiQAJ4B9l+ssDcKwAQ4XbEFSwvLxQZna6DbJnMLh3rmlkkyuS4ESMQClP4o2kJiyqwZs7QNwQs5QGCNqANMhjOKraqIO7fRVUrUcPck125KYKGvTDvHYcxc="


# account = admin_email_id

# encryption = login.encrypt_password(password)
# # print("encryption:{},{}".format(encryption,type(encryption)))
# encrypted_password = encryption['encrypted_password']
# print("encrypted_password:{},{}".format(encrypted_password,type(encrypted_password)))


# decryption = login.decrypt_password(encrypted_password)
# # print("decryption:{},{}".format(decryption,type(decryption)))
# decrypted_password = decryption['decrypted_password']
# print("decrypted_password:{},{}".format(decrypted_password,type(decrypted_password)))




# entityList = utilities.get_password_from_password_vault(account)
# print(entityList['entityList'][0]['password'])


# password = utilities.get_password_from_password_vault(account)
# print("password:{},{}".format(password,type(password)))


# entityKind = utilities.get_value_by_entityKind_and_key("mathgarage-prod","change_base_config")['config_value']
# print(entityKind)


# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = env['credential_key_file']
# print(os.getenv('GOOGLE_APPLICATION_CREDENTIALS['project_id'])) 

# PUBSUB TESTING...

# pubsub_topics = utilities.get_value_by_entityKind_and_key(env['config_entityKind'],"pubsub_topics")['config_value']
# topic = pubsub_topics['register_topic']
# # Test Create Topic
# response = pubsuboperations.create_topic(topic)
# for key,value in response.items():
#     print("{}: {},{}".format(key,value,type(value)))

# # Test Publish Messages to a PubSub Topic
# # message = str(datetime.datetime.now())
# message = "Test message for cloud functions."
# response = pubsuboperations.publish_message_to_topic(message.encode(),topic)
# print(response)
# for key,value in response.items():
#     print("{}: {},{}".format(key,value,type(value)))


# setup.update_datastore_config_from_json()
# setup.download_datastore_kind_into_json()

# email = "jai.chenchlani@mindtree.com"
# response = utilities.isValidEmail(email)
# for key,value in response.items():
#     print("{}: {},{}".format(key,value,type(value)))


# # Create Password Vault Entry
# utilities.create_password_in_password_vault('jaichenchlani@gmail.com',"")

# print(config.get_environment_from_env_file())

# utilities.get_url()

# print(mathfunctions.isEven(-1))

# for i in range(-10,10):
#     print("{}:{}".format(i,mathfunctions.isPrime(i)))

# timestamp = datetime.datetime.now()

# print(config.get_environment_from_env_file())

# print(dashboard.generate_user_dashboard("jaichenchlani"))


