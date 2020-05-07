from google.cloud import kms_v1
import utilities, config
import sys

# Load Environment
env = config.get_environment_from_env_file()

def initialize_config(kms_config):
    password_encryption_codes = utilities.get_value_by_entityKind_and_key(env['config_entityKind'],"password_encryption_codes")['config_value']
    project_id = password_encryption_codes['project_id']
    location_id = password_encryption_codes['location_id']
    key_ring_id = password_encryption_codes['key_ring_id']
    crypto_key_id = password_encryption_codes['crypto_key_id']
    # Create an API client for the KMS API.
    kms_config['client'] = kms_v1.KeyManagementServiceClient()
    # The resource name of the CryptoKey.
    kms_config['crypto_key_name'] = kms_config['client'].crypto_key_path(project_id, location_id, key_ring_id, crypto_key_id)

def  encrypt_symmetric(plaintext):
    print("Entering encrypt_symmetric...")
    # Initialize Config
    kms_config = {
        "client": None,
        "crypto_key_name": None
    }
    initialize_config(kms_config)
    # Initialize the response dictionary
    response = {
        "result": True,
        "message": "Encryption successful.",
        "validOutputReturned": True,
        "ciphertext": None
    }
    try:
        # Use the KMS API to encrypt the data.
        encryption = kms_config['client'].encrypt(kms_config['crypto_key_name'], plaintext.encode())
    except Exception as e:
        # Error performing the KMS operation
        errorMessage = "Error performing encryption."
        errorMessage = "{0} Stacktrace: {1}".format(errorMessage,e)
        print(errorMessage)
        response['message'] = errorMessage
        response['validOutputReturned'] = False
    
    # All good. Return the encrypted value
    response['ciphertext'] = encryption.ciphertext
    return response

def decrypt_symmetric(ciphertext):
    print("Entering decrypt_symmetric...")
    # Initialize Config
    kms_config = {
        "client": None,
        "crypto_key_name": None
    }
    initialize_config(kms_config)
    # Initialize the response dictionary
    response = {
        "result": True,
        "message": "Decryption successful.",
        "validOutputReturned": True,
        "plaintext": None
    }
    try:
        # Use the KMS API to decrypt the data.
        decryption = kms_config['client'].decrypt(kms_config['crypto_key_name'], ciphertext)
        print(decryption)
    except Exception as e:
        # Error performing the KMS operation
        errorMessage = "Error performing decryption."
        errorMessage = "{0} Stacktrace: {1}".format(errorMessage,e)
        print(errorMessage)
        response['message'] = errorMessage
        response['validOutputReturned'] = False
    
    # All good. Return the encrypted value
    response['plaintext'] = decryption.plaintext.decode()
    return response
