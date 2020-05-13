from google.cloud import pubsub_v1
import os, datetime
import utilities, config

# Load Environment
env = config.get_environment_from_env_file()

# Create the datastore client to be used by all functions
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = env['credential_key_file']

def initialize_config(pubsub_config):
    print("Entering initialize_config...")
    project_id = env['project_id']
    pubsub_config['topic_name'] = "projects/{}/topics/{}".format(project_id,pubsub_config['topic'])
    pubsub_config['publisher'] = pubsub_v1.PublisherClient()

def create_topic(topic):
    print("Entering post_topic...")
    # Initialize PubSub Config
    pubsub_config = {
        "topic": topic,
        "topic_name": None,
        "publisher": None
    }
    initialize_config(pubsub_config)
    # Initialize the response dictionary
    response = {
        "topic": None,
        "message": "Topic creation successful.",
        "validOutputReturned": True
    }
    try:
        # Use the PubSub API to create the topic.
        topic = pubsub_config['publisher'].create_topic(pubsub_config['topic_name'])
    except Exception as e:
        # Error performing the PubSub operation
        errorMessage = "Error creating PubSub topic."
        errorMessage = "{0} Stacktrace: {1}".format(errorMessage,e)
        print(errorMessage)
        response['message'] = errorMessage
        response['validOutputReturned'] = False

    response['topic'] = topic
    return response

def publish_message_to_topic(message,topic):
    print("Entering publish_message_to_topic...")
    # Initialize PubSub Config
    pubsub_config = {
        "topic": topic,
        "topic_name": None,
        "publisher": None
    }
    initialize_config(pubsub_config)
    # Initialize the response dictionary
    response = {
        "topic_message": None,
        "result": True,
        "message": "Message published.",
        "validOutputReturned": True
    }
    try:
        # Use the PubSub API to publish the message.
        topic_message = pubsub_config['publisher'].publish(pubsub_config['topic_name'], message, spam='eggs')
    except Exception as e:
        # Error performing the PubSub operation
        errorMessage = "Error publishing message to topic {}.".format(topic)
        errorMessage = "{0} Stacktrace: {1}".format(errorMessage,e)
        print(errorMessage)
        response['message'] = errorMessage
        response['validOutputReturned'] = False
    
    response['topic_message'] = topic_message
    return response

def subscribe_topic(topic):
    print("Entering subscribe_topic...")
    # Initialize PubSub Config
    pubsub_config = {
        "topic": topic,
        "topic_name": None,
        "publisher": None
    }
    # Initialize the response dictionary
    response = {
        "topic_message": None,
        "result": True,
        "message": "Message published.",
        "validOutputReturned": True
    }
    # YET TO COMPLETE....