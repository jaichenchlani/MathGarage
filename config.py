import json

# Load Configurations
def read_configurations_from_config_file():
    print("Entering read_configurations_from_config_file...")
    with open('keys/config.json') as config_json_data_file:
        envVariables = json.load(config_json_data_file)
    return envVariables

# Load Environment
def get_environment_from_env_file():
    print("Entering get_environment_from_env_file...")
    with open('keys/env.json') as env_file:
        env = json.load(env_file)
    return env



