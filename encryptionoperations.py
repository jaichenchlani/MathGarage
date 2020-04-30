from google.cloud import kms_v1
from config import read_configurations_from_config_file
import traceback, sys

# Load Defaults from Config
envVariables = read_configurations_from_config_file()
password_encryption_codes = envVariables['password_encryption_codes']
project_id = password_encryption_codes['project_id']
location_id = password_encryption_codes['location_id']
key_ring_id = password_encryption_codes['key_ring_id']
crypto_key_id = password_encryption_codes['crypto_key_id']
# Create an API client for the KMS API.
client = kms_v1.KeyManagementServiceClient()
# The resource name of the CryptoKey.
crypto_key_name = client.crypto_key_path(project_id, location_id, key_ring_id, crypto_key_id)
exc_traceback = sys.exc_info()

def  encrypt_symmetric(plaintext):
    print("Entering encrypt_symmetric...")
    # Initialize the response dictionary
    response = {
        "result": True,
        "message": "Encryption successful.",
        "validOutputReturned": True,
        "ciphertext": None
    }
    try:
        # Use the KMS API to encrypt the data.
        encryption = client.encrypt(crypto_key_name, plaintext.encode())
    except:
        # Error performing the KMS operation
        response['message'] = "Error performing encryption."
        response['validOutputReturned'] = False
    
    # All good. Return the encrypted value
    response['ciphertext'] = encryption.ciphertext
    return response

def decrypt_symmetric(ciphertext):
    print("Entering decrypt_symmetric...")
    # Initialize the response dictionary
    response = {
        "result": True,
        "message": "Decryption successful.",
        "validOutputReturned": True,
        "plaintext": None
    }
    try:
        # Use the KMS API to decrypt the data.
        decryption = client.decrypt(crypto_key_name, ciphertext)
    except:
        # Error performing the KMS operation
        response['message'] = "Error performing decryption."
        response['validOutputReturned'] = False
    
    # All good. Return the encrypted value
    response['plaintext'] = decryption.plaintext.decode()
    return response
