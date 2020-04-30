from google.cloud import storage
from google.cloud import datastore, kms_v1
import os
from config import read_configurations_from_config_file

# Load Defaults from Config
envVariables = read_configurations_from_config_file()
credential_key_file = envVariables['credential_key_file']
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_key_file

def get_buckets():
    # Instantiates a client
    storage_client = storage.Client()

    # # The name for the new bucket
    # bucket_name = "my-new-bucket"

    # # Creates the new bucket
    # bucket = storage_client.create_bucket(bucket_name)
    # print("Bucket {} created.".format(bucket.name))


     # Make an authenticated API request to get all the buckets
    buckets = list(storage_client.list_buckets())
    print(buckets)

def get_keyrings(project_id, location):
    
    client = kms_v1.KeyManagementServiceClient()
    parent = client.location_path(project_id,location)
    key_rings = client.list_key_rings(parent)
    print("key_rings:{},{}".format(key_rings,type(key_rings)))
    key_rings_list = list(key_rings)
    print("key_rings_list:{},{}".format(key_rings_list,type(key_rings_list)))
    for key_ring in key_rings_list:
        print("key_ring:{},{}".format(key_ring,type(key_ring)))
    
    # crypto_keys = client.list_crypto_keys(parent)
    # print("crypto_keys:{},{}".format(crypto_keys,type(crypto_keys)))
    # crypto_keys_list = list(crypto_keys)
    # print("crypto_keys_list:{},{}".format(crypto_keys_list,type(crypto_keys_list)))
    # # for crypto_key in crypto_keys_list:
    # #     print("crypto_key:{},{}".format(crypto_key,type(crypto_key)))

def  encrypt_symmetric(project_id, location_id, key_ring_id, crypto_key_id, plaintext):
    # Creates an API client for the KMS API.
    client = kms_v1.KeyManagementServiceClient()

    # The resource name of the CryptoKey.
    name = client.crypto_key_path(project_id, location_id, key_ring_id, crypto_key_id)
    # print("name:{},{}".format(name,type(name)))

    # Use the KMS API to encrypt the data.
    response = client.encrypt(name, plaintext)
    return response.ciphertext

def decrypt_symmetric(project_id, location_id, key_ring_id, crypto_key_id,
                      ciphertext):
    """Decrypts input ciphertext using the provided symmetric CryptoKey."""

    # Creates an API client for the KMS API.
    client = kms_v1.KeyManagementServiceClient()

    # The resource name of the CryptoKey.
    name = client.crypto_key_path(project_id, location_id, key_ring_id, crypto_key_id)

    # Use the KMS API to decrypt the data.
    response = client.decrypt(name, ciphertext)
    return response.plaintext
    






    
