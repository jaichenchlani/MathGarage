from random import randint
import datastoreoperations, utilities, config
from mathfunctions import isInteger
import datetime

# Load Environment
env = config.get_environment_from_env_file()
datastore_kind_basic_arithematic_operations_key = "datastore_kind_basic_arithematic_operations"

def generate_basic_arithmatic_operations(requestData):
    print("Start - Entering generate_basic_arithmatic_operation...")

    # Declare the output dictionary
    generated_basic_arithmatic_operation = declare_output_dictionary(requestData)

    # Read config file and and load the configurations for the supplied difficulty level 
    get_config(generated_basic_arithmatic_operation)
    # print("Selected Puzzle Configuration:{}".format(selected_random_puzzle))

    # Apply Business Rules on Operation Request.
    # And, if all good, go ahead with generating the puzzle progression
    if is_valid_configuration(generated_basic_arithmatic_operation):
        process_request(generated_basic_arithmatic_operation)
    
    # Insert the generated Output Dictionary in Datastore
    # Get entityKind config from Datastore
    entityKind = utilities.get_value_by_entityKind_and_key(env['config_entityKind'],datastore_kind_basic_arithematic_operations_key)['config_value']
    insert_response = utilities.insert_in_datastore_and_get_id(entityKind,generated_basic_arithmatic_operation)
    if not insert_response['validOutputReturned']:
        # Error creating datastore entity
        generated_basic_arithmatic_operation['validOutputReturned'] = False
        generated_basic_arithmatic_operation['message'] = insert_response['message']
    else:
        pass
        print("Persisted generated_basic_arithmatic_operation object in Datastore...")
        # Update the Datastore ID in the Output Dictionary
        generated_basic_arithmatic_operation['datastore_id'] = insert_response['id']

    # Return the generated Output Dictionary to the caller.
    print("End - Returning to caller.")
    return generated_basic_arithmatic_operation

def declare_output_dictionary(requestData):
    print("Entering declare_output_dictionary...")
    
    generated_basic_arithmatic_operation = {}
    generated_basic_arithmatic_operation['datastore_id'] = 0
    generated_basic_arithmatic_operation['user'] = "Guest"
    generated_basic_arithmatic_operation['create_timestamp'] = datetime.datetime.now()
    generated_basic_arithmatic_operation['last_modified_timestamp'] = datetime.datetime.now()
    generated_basic_arithmatic_operation['operator'] = requestData['operator']
    generated_basic_arithmatic_operation['number_of_questions'] = int(requestData['number_of_questions'])
    generated_basic_arithmatic_operation['difficultyLevel'] = requestData['difficultyLevel']
    generated_basic_arithmatic_operation['config'] = {}
    generated_basic_arithmatic_operation['questions'] = []
    generated_basic_arithmatic_operation['message'] = ""
    generated_basic_arithmatic_operation['validOutputReturned'] = True
    generated_basic_arithmatic_operation['showUserHelp'] = utilities.get_value_by_entityKind_and_key(env['config_entityKind'],"showUserHelp")['config_value']
    
    return generated_basic_arithmatic_operation

def get_config(generated_basic_arithmatic_operation):
    print("Entering get_config...")
    difficultyLevel = generated_basic_arithmatic_operation['difficultyLevel']

    # All(i.e. all Difficulty Levels) Valid Puzzle Configurations from Config
    allConfigurations = utilities.get_value_by_entityKind_and_key(env['config_entityKind'],"basic_arithematic_operation_configurations")['config_value']
    # print("allConfigurations:{},{}".format(allConfigurations, type(allConfigurations)))
    # print("Total Puzzle Configurations: {}".format(len(allConfigurations)))

    # Shortlist the valid puzzle configurations based on difficulty level
    validConfigurations = utilities.identify_valid_items_in_list(allConfigurations,difficultyLevel)
    # print("validConfigurations:{},{}".format(validConfigurations, type(validConfigurations)))
    # print("Valid Puzzle Configurations: {}".format(len(validConfigurations)))

    # There is only 1 configuration per Difficulty Level. 
    # If there are multiple by mistake in Config, select 1 at random.
    # selected_random_puzzle = {}
    total_valid_configs = len(validConfigurations)

    if total_valid_configs > 0:
        random_index = randint(0,total_valid_configs-1)
        selected_config = validConfigurations[random_index]
        generated_basic_arithmatic_operation['config'] = selected_config
    else:
        generated_basic_arithmatic_operation['validOutputReturned'] = False
        generated_basic_arithmatic_operation['message'] = "No valid configurations found for selected Difficulty Levels."


def is_valid_configuration(generated_basic_arithmatic_operation):
    print("Entering is_valid_configuration...")

    # Validate the request operations against the allowed operations in Config
    requested_operation = generated_basic_arithmatic_operation['operator']
    valid_operations = utilities.get_value_by_entityKind_and_key(env['config_entityKind'],"valid_basic_arithmatic_operations_list")['config_value']
    if requested_operation not in valid_operations:
        user_message = "{} is invalid Math operator; Valid operators are {}.".format(requested_operation,valid_operations)
        generated_basic_arithmatic_operation['message'] = user_message
        generated_basic_arithmatic_operation['validOutputReturned'] = False
        return False

    # Validate first_number_lower_limit to be an Integer
    # validate_all_numbers_in_operation_request(generated_basic_arithmatic_operation)
    number_validation_list = []
    number_validation_list.append(generated_basic_arithmatic_operation['config']['first_number_lower_limit'])
    number_validation_list.append(generated_basic_arithmatic_operation['config']['first_number_upper_limit'])
    number_validation_list.append(generated_basic_arithmatic_operation['config']['second_number_lower_limit'])
    number_validation_list.append(generated_basic_arithmatic_operation['config']['second_number_upper_limit'])
    number_validation_list.append(generated_basic_arithmatic_operation['number_of_questions'])
    # Run each number through a for loop and call the Utilities function to validate
    for temp_str_variable in number_validation_list:
        if not isInteger(temp_str_variable):
            user_message = "{} is invalid; Only integer values are allowed.".format(temp_str_variable)
            generated_basic_arithmatic_operation['message'] = user_message
            generated_basic_arithmatic_operation['validOutputReturned'] = False
            return False    

    number_of_questions = int(generated_basic_arithmatic_operation['number_of_questions'])
    if number_of_questions < 1:
        user_message = "{} is invalid; Number of questions should be >= 1.".format(number_of_questions)
        generated_basic_arithmatic_operation['message'] = user_message
        generated_basic_arithmatic_operation['validOutputReturned'] = False
        return False    

    return True

def process_request(generated_basic_arithmatic_operation):
    print("Entering process_request...")
    number_of_questions = generated_basic_arithmatic_operation['number_of_questions']
    for i in range(0,number_of_questions):
        # Initialize the questions Dictionary
        question_dictionary = {
        "first_number": 0,
        "second_number": 0,
        "operator": "",
        "text": "",
        "answer": 0,
        "user_answer": 0,
        "is_user_answer_correct": 0
        }
        # Generate the first number
        question_dictionary['first_number'] = randint(int(generated_basic_arithmatic_operation['config']['first_number_lower_limit']),
        int(generated_basic_arithmatic_operation['config']['first_number_upper_limit']))
        # Generate the second number
        question_dictionary['second_number'] = randint(int(generated_basic_arithmatic_operation['config']['second_number_lower_limit']),
        int(generated_basic_arithmatic_operation['config']['second_number_upper_limit']))
        question_dictionary['operator'] = generated_basic_arithmatic_operation['operator']
        # Calculate questions
        if generated_basic_arithmatic_operation['operator'] == "+":
            question_dictionary['answer'] =  question_dictionary['first_number'] + question_dictionary['second_number']
        elif generated_basic_arithmatic_operation['operator'] == "-":
            question_dictionary['answer'] =  question_dictionary['first_number'] - question_dictionary['second_number']
        elif generated_basic_arithmatic_operation['operator'] == "x":
            question_dictionary['answer'] =  question_dictionary['first_number'] * question_dictionary['second_number']
        elif generated_basic_arithmatic_operation['operator'] == "/":
            # Prevent Divide by zero error
            if question_dictionary['second_number'] == 0:
                question_dictionary['second_number'] = 1
            question_dictionary['answer'] =  question_dictionary['first_number'] // question_dictionary['second_number']
        else:
            user_message = "{} is invalid Math operator; Valid operators are {}.".format(generated_basic_arithmatic_operation['operator'],utilities.get_value_by_entityKind_and_key(env['config_entityKind'],"valid_basic_arithmatic_operations_list")['config_value'])
            generated_basic_arithmatic_operation['message'] = user_message
            generated_basic_arithmatic_operation['validOutputReturned'] = False
            return
        
        question_dictionary['text'] = "{} {} {} =".format(question_dictionary['first_number'],question_dictionary['operator'],question_dictionary['second_number'])
        generated_basic_arithmatic_operation['questions'].append(question_dictionary)

def update_datastore_basic_arithmatic_operations(input_basic_arithematic_operation):
    print("Entering update_datastore_basic_arithmatic_operations...")
    # Update Datastore Entity
    id = input_basic_arithematic_operation['datastore_id']
    updated_entity = {
    "last_modified_timestamp": datetime.datetime.now(),
    "questions": input_basic_arithematic_operation['questions']
    }
    # Get entityKind config from Datastore
    entityKind = utilities.get_value_by_entityKind_and_key(env['config_entityKind'],datastore_kind_basic_arithematic_operations_key)['config_value']
    status = datastoreoperations.update_datastore_entity(entityKind,id,updated_entity)
    return status