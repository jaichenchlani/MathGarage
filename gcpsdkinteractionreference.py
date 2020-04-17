from google.cloud import storage
from google.cloud import datastore

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

def create_datastore_entity(entityKind,entityObject):
    # Create, populate and persist an entity with keyID passed as argument
    client = datastore.Client()
    key = client.key(entityKind)
    entity = datastore.Entity(key=key)
    entity.update(entityObject)
    client.put(entity)