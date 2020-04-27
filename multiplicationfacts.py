from config import read_configurations_from_config_file
from utilities import identify_valid_items_in_list
from datastoreoperations import create_datastore_entity, update_datastore_entity
import datetime

def get_multiplication_facts(str_table_of, str_limit):

    print("Start - Entering get_multiplication_facts...")
    generated_multiplication_facts = {}
    warning_counter = 0

    # Load Defaults from Config
    envVariables = read_configurations_from_config_file()

    default_table_of = envVariables['multiplication_facts_table_of']
    default_limit = envVariables['multiplication_facts_limit']

    operation_request = {
        "tableof": str_table_of,
        "limit": str_limit
    }
    # Declare the output dictionary
    generated_multiplication_facts = declare_output_dictionary(operation_request)

    # Apply Business Rules on Operation Request.
    # And, if all good, go ahead with generating the Multiplication Facts
    if is_valid_request(generated_multiplication_facts):
        tableof = generated_multiplication_facts['request']['tableof']
        limit = generated_multiplication_facts['request']['limit']
        generated_multiplication_facts["result"] = [tableof*i for i in range(1, limit+1)]

    # Insert the generated Output Dictionary in Datastore
    create_datastore_entity("multiplication_facts",generated_multiplication_facts)
    print("Persisted generated_multiplication_facts object in Datastore...")

    # Return the generated Output Dictionary to the caller.
    print("End - Returning to caller.")
    return generated_multiplication_facts

def declare_output_dictionary(operation_request):
    print("Entering declare_output_dictionary...")
    
    generated_multiplication_facts = {}
    generated_multiplication_facts['user'] = "Guest"
    generated_multiplication_facts['create_timestamp'] = datetime.datetime.now()
    generated_multiplication_facts['last_modified_timestamp'] = datetime.datetime.now()
    generated_multiplication_facts["request"] = operation_request
    generated_multiplication_facts['result'] = []
    generated_multiplication_facts['message'] = ""
    generated_multiplication_facts['validOutputReturned'] = True

    return generated_multiplication_facts

def is_valid_request(generated_multiplication_facts):
    print("Entering is_valid_request...")
    try:
        table_of = int(generated_multiplication_facts['request']['tableof'])
    except ValueError:
        user_message = "Invalid table_of value {}.".format(generated_multiplication_facts['request']['tableof'])
        generated_multiplication_facts['message'] = user_message
        generated_multiplication_facts['validOutputReturned'] = False
        return False


    try:
        limit = int(generated_multiplication_facts['request']['limit'])
    except ValueError:
        # Set the default
        user_message = "Invalid limit value {}.".format(generated_multiplication_facts['request']['limit'])
        generated_multiplication_facts['message'] = user_message
        generated_multiplication_facts['validOutputReturned'] = False
        return False

    return True