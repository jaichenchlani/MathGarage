from config import read_configurations_from_config_file
from random import randint
from utilities import identify_valid_items_in_list, is_valid_integer

def generate_basic_arithmatic_operations(operation_request):
    print("Entering generate_basic_arithmatic_operation...")

    # Declare the output dictionary
    generated_basic_arithmatic_operation = declare_output_dictionary(operation_request)

    # Apply Business Rules on Operation Request.
    # And, if all good, go ahead with generating the puzzle progression
    if is_valid_configuration(generated_basic_arithmatic_operation):
        generate_basic_arithmatic_operation(generated_basic_arithmatic_operation)

    print(generated_basic_arithmatic_operation)
    return generated_basic_arithmatic_operation

def declare_output_dictionary(operation_request):
    print("Entering declare_output_dictionary...")
    
    generated_basic_arithmatic_operation = {}
    
    generated_basic_arithmatic_operation['request'] = operation_request
    generated_basic_arithmatic_operation['questions'] = []
    generated_basic_arithmatic_operation['message'] = ""
    generated_basic_arithmatic_operation['validOutputReturned'] = True
    
    return generated_basic_arithmatic_operation

def is_valid_configuration(generated_basic_arithmatic_operation):
    print("Entering is_valid_configuration...")
    # Load Defaults from Config
    envVariables = read_configurations_from_config_file()

    # Validate the request operations against the allowed operations in Config
    requested_operation = generated_basic_arithmatic_operation['request']['operator']
    valid_operations = envVariables['valid_basic_arithmatic_operations_list']
    if requested_operation not in valid_operations:
        user_message = "{} is invalid Math operator; Valid operators are {}.".format(requested_operation,valid_operations)
        generated_basic_arithmatic_operation['message'] = user_message
        generated_basic_arithmatic_operation['validOutputReturned'] = False
        return False

    # Validate first_number_lower_limit to be an Integer
    # validate_all_numbers_in_operation_request(generated_basic_arithmatic_operation)
    number_validation_list = []
    number_validation_list.append(generated_basic_arithmatic_operation['request']['first_number_lower_limit'])
    number_validation_list.append(generated_basic_arithmatic_operation['request']['first_number_upper_limit'])
    number_validation_list.append(generated_basic_arithmatic_operation['request']['second_number_lower_limit'])
    number_validation_list.append(generated_basic_arithmatic_operation['request']['second_number_upper_limit'])
    number_validation_list.append(generated_basic_arithmatic_operation['request']['number_of_questions'])
    # Run each number through a for loop and call the Utilities function to validate
    for temp_str_variable in number_validation_list:
        if not is_valid_integer(temp_str_variable):
            user_message = "{} is invalid; Only integer values are allowed.".format(temp_str_variable)
            generated_basic_arithmatic_operation['message'] = user_message
            generated_basic_arithmatic_operation['validOutputReturned'] = False
            return False    

    number_of_questions = int(generated_basic_arithmatic_operation['request']['number_of_questions'])
    if number_of_questions < 1:
        user_message = "{} is invalid; Number of questions should be >= 1.".format(number_of_questions)
        generated_basic_arithmatic_operation['message'] = user_message
        generated_basic_arithmatic_operation['validOutputReturned'] = False
        return False    

    return True

def generate_basic_arithmatic_operation(generated_basic_arithmatic_operation):
    print("Entering generate_basic_arithmatic_operation...")
    number_of_questions = generated_basic_arithmatic_operation['request']['number_of_questions']
    for i in range(0,number_of_questions):
        # Initialize the questions Dictionary
        question_dictionary = {
        "first_number": 0,
        "second_number": 0,
        "operator": "",
        "answer": 0,
        "user_answer": 0,
        "is_user_answer_correct": 0
        }
        # Generate the first number
        question_dictionary['first_number'] = randint(int(generated_basic_arithmatic_operation['request']['first_number_lower_limit']),
        int(generated_basic_arithmatic_operation['request']['first_number_upper_limit']))
        # Generate the second number
        question_dictionary['second_number'] = randint(int(generated_basic_arithmatic_operation['request']['second_number_lower_limit']),
        int(generated_basic_arithmatic_operation['request']['second_number_upper_limit']))
        question_dictionary['operator'] = generated_basic_arithmatic_operation['request']['operator']
        # Calculate questions
        if generated_basic_arithmatic_operation['request']['operator'] == "+":
            question_dictionary['answer'] =  question_dictionary['first_number'] + question_dictionary['second_number']
        elif generated_basic_arithmatic_operation['request']['operator'] == "-":
            question_dictionary['answer'] =  question_dictionary['first_number'] - question_dictionary['second_number']
        elif generated_basic_arithmatic_operation['request']['operator'] == "x":
            question_dictionary['answer'] =  question_dictionary['first_number'] * question_dictionary['second_number']
        elif generated_basic_arithmatic_operation['request']['operator'] == "/":
            # Prevent Divide by zero error
            if question_dictionary['second_number'] == 0:
                question_dictionary['second_number'] = 1
            question_dictionary['answer'] =  question_dictionary['first_number'] // question_dictionary['second_number']
        else:
            user_message = "{} is invalid Math operator; Valid operators are {}.".format(requested_operation,valid_operations)
            generated_basic_arithmatic_operation['message'] = user_message
            generated_basic_arithmatic_operation['validOutputReturned'] = False
            return
        generated_basic_arithmatic_operation['questions'].append(question_dictionary)