from mathfunctions import isEven, isPrime, isPositive, getFactors, getBinary, getPrimeFactors
from config import read_configurations_from_config_file
from datastoreoperations import create_datastore_entity, update_datastore_entity
import datetime

# Load Defaults from Config
envVariables = read_configurations_from_config_file()
entityKind = envVariables['datastore_kind_number_wiki']

def get_number_wiki(n):
    print("Start - Entering get_number_wiki...")

    # Declare the output dictionary
    number_wiki = declare_output_dictionary()

    # Call the Math Functions to populate output dictionary
    number_wiki['isEven'] = isEven(n)
    number_wiki['isPrime'] = isPrime(n)
    number_wiki['getFactors'] = getFactors(n)
    number_wiki['getPrimeFactors'] = getPrimeFactors(n)

    # Insert the generated Output Dictionary in Datastore
    datastore_entity = create_datastore_entity(entityKind,number_wiki)
    print("Persisted number_wiki object in Datastore...")

    # Update the Datastore ID in the Output Dictionary
    # Return the generated Output Dictionary to the caller.
    number_wiki['datastore_id'] = datastore_entity.key.id
    print("End - Returning to caller.")
    
    return number_wiki


def declare_output_dictionary():
    number_wiki = {}
    number_wiki['datastore_id'] = 0
    number_wiki['user'] = "Guest"
    number_wiki['create_timestamp'] = datetime.datetime.now()
    number_wiki['last_modified_timestamp'] = datetime.datetime.now()
    number_wiki['isEven'] = {}
    number_wiki['isPrime'] = {}
    number_wiki['getFactors'] = {}
    number_wiki['getPrimeFactors'] = {}
    number_wiki['message'] = ""
    number_wiki['validOutputReturned'] = True
    number_wiki['showUserHelp'] = envVariables['showUserHelp']
    return number_wiki