from mathfunctions import isEven, isPrime, isPositive, getFactors, changeBase, getPrimeFactors
import datastoreoperations, utilities, config
import datetime

# Load Environment
env = config.get_environment_from_env_file()

def get_number_wiki(n):
    print("Start - Entering get_number_wiki...")

    # Declare the output dictionary
    number_wiki = declare_output_dictionary(n)

    # Process request to populate the results dictionary
    process_request(number_wiki)

    # Get entityKind config from Datastore
    entityKind = utilities.get_value_by_entityKind_and_key(env['config_entityKind'],"datastore_kind_number_wiki")['config_value']
    
    # Insert the generated Output Dictionary in Datastore
    insert_response = utilities.insert_in_datastore_and_get_id(entityKind,number_wiki)
    if not insert_response['validOutputReturned']:
        # Error creating datastore entity
        number_wiki['validOutputReturned'] = False
        number_wiki['message'] = insert_response['message']
    else:
        pass
        print("Persisted generated_linear_equations object in Datastore...")
        # Update the Datastore ID in the Output Dictionary
        number_wiki['datastore_id'] = insert_response['id']

    # Return the generated Output Dictionary to the caller.
    print("End - Returning to caller.")
    return number_wiki

def declare_output_dictionary(n):
    print("Entering declare_output_dictionary...")
    number_wiki = {}
    number_wiki['datastore_id'] = 0
    number_wiki['user'] = "Guest"
    number_wiki['create_timestamp'] = datetime.datetime.now()
    number_wiki['last_modified_timestamp'] = datetime.datetime.now()
    number_wiki['n'] = n
    number_wiki['wiki_list'] = []
    number_wiki['message'] = ""
    number_wiki['validOutputReturned'] = True
    number_wiki['showUserHelp'] = utilities.get_value_by_entityKind_and_key(env['config_entityKind'],"showUserHelp")['config_value']
    return number_wiki

def process_request(number_wiki):
    print("Entering process_request...")
    # Declare the blank wikiList dictionary
    wikiList = []
    wikiListItem = {"key": "", "value": ""}

    # Even/Odd Processing
    wikiListItem = {"key": "Even/Odd", "value": ""}
    checkEven = isEven(number_wiki['n'])
    if not checkEven['validOutputReturned']:
        wikiListItem['value'] = checkEven['message']
    else:
        # Valid result returned. Process.
        if isEven(number_wiki['n'])['result']:
            wikiListItem['value'] = "Even"
        else:
            wikiListItem['value'] = "Odd"
    
    # Append the Even/Odd element to the list
    wikiList.append(wikiListItem)

    # Divisors and Prime/Composite processing
    wikiListItem = {"key": "", "value": ""}
    divisors = getFactors(number_wiki['n'])
    if not divisors['validOutputReturned']:
        wikiListItem = {"key": "Divisors", "value": divisors['message']}
    else:
        # Valid result returned. Process.
        # Prime/Composite processing
        if divisors['isPrime']:
            wikiListItem['Prime/Composite'] = "Prime"
            wikiListItem = {"key": "Prime/Composite", "value": "Prime"}
        else:
            wikiListItem['Prime/Composite'] = "Composite"
            wikiListItem = {"key": "Prime/Composite", "value": "Composite"}
        # Append the Prime/Composite element to the list
        wikiList.append(wikiListItem)
        # Process Divisors
        # Create a temporary list with all elements in the list converted to string.
        strList = [str(element) for element in divisors['factors']]
        # Convert the temporary list into a comma separated string.
        wikiListItem = {"key": "Divisors", "value": ",".join(strList)}
        # Append the Divisors element to the list
        wikiList.append(wikiListItem)

    # Prime Factors processing
    wikiListItem = {"key": "Prime Factors", "value": ""}
    primeFactors = getPrimeFactors(number_wiki['n'])
    if not primeFactors['validOutputReturned']:
        wikiListItem['value'] = primeFactors['message']
    else:
        # Create a temporary list with all elements in the list converted to string.
        strList = [str(element) for element in primeFactors['primeFactors']]
        # Convert the temporary list into a comma separated string.
        wikiListItem['value'] = ",".join(strList)
    # Append the Prime Factors element to the list
    wikiList.append(wikiListItem)

    # Get changeBaseConfig config from Datastore
    changeBaseConfig = utilities.get_value_by_entityKind_and_key(env['config_entityKind'],"change_base_config")['config_value']

    # Change Base Processing for bases defined in Config
    for (key,value) in changeBaseConfig.items():
        wikiListItem = {"key": key, "value": ""}    
        newBaseNumber = changeBase(number_wiki['n'],value)
        if not newBaseNumber['validOutputReturned']:
            wikiListItem['value'] = newBaseNumber['message']
        else:
            wikiListItem['value'] = newBaseNumber['result']
        # Append the Binary element to the list
        wikiList.append(wikiListItem)

    # Update the response dictionary wiki_list with wikiList
    number_wiki['wiki_list'] = wikiList
