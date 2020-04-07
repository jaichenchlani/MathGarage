import json
import logging

# Load Configurations
def read_configurations_from_config_file():
    with open('config.json') as config_json_data_file:
        envVariables = json.load(config_json_data_file)
    
    return envVariables

