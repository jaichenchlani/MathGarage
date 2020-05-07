import datastoreoperations, utilities, config
import datetime

# Load Environment
env = config.get_environment_from_env_file()

def get_multiplication_facts(str_table_of, str_limit):

    print("Start - Entering get_multiplication_facts...")
    generated_multiplication_facts = {}
    warning_counter = 0

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
    # Get entityKind config from Datastore
    entityKind = utilities.get_value_by_entityKind_and_key(env['config_entityKind'],"datastore_kind_multiplication_facts")['config_value']
    insert_response = utilities.insert_in_datastore_and_get_id(entityKind,generated_multiplication_facts)
    if not insert_response['validOutputReturned']:
        # Error creating datastore entity
        generated_multiplication_facts['validOutputReturned'] = False
        generated_multiplication_facts['message'] = insert_response['message']
    else:
        pass
        print("Persisted generated_linear_equations object in Datastore...")
        # Update the Datastore ID in the Output Dictionary
        generated_multiplication_facts['datastore_id'] = insert_response['id']

    # Return the generated Output Dictionary to the caller.
    print("End - Returning to caller.")
    return generated_multiplication_facts

def declare_output_dictionary(operation_request):
    print("Entering declare_output_dictionary...")
    
    generated_multiplication_facts = {}
    generated_multiplication_facts['datastore_id'] = ""
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