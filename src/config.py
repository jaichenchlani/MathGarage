import json

# Load Configurations
def read_configurations_from_config_file():
    print("Entering read_configurations_from_config_file...")
    env = get_environment_from_env_file()
    with open(env['config_json']) as config_json_file:
        envVariables = json.load(config_json_file)
    return envVariables

# Load Environment
def get_environment_from_env_file():
    print("Entering get_environment_from_env_file...")
    env = {}

    with open('../keys/env.json') as env_file:
        config = json.load(env_file)

    # Suffix the environment name ("prod", "sandbox" etc)
    env_suffix = config['environment']
    path = config['path']
    
    # Set the Project ID
    if env_suffix == "prod":
        env['project_id'] = config['variables_prefix']['project_id']
    else:
        env['project_id'] = "{}-{}".format(config['variables_prefix']['project_id'],env_suffix)

    # Set the Credential Key File
    parseFileName = config['variables_prefix']['credential_key_file'].split('.')
    filename = parseFileName[0]
    extension = parseFileName[1]
    env['credential_key_file'] = "{}{}-{}.{}".format(path,filename,env_suffix,extension)

    # Set the Config JSON File
    parseFileName = config['variables_prefix']['config_json'].split('.')
    filename = parseFileName[0]
    extension = parseFileName[1]
    env['config_json'] = "{}{}-{}.{}".format(path,filename,env_suffix,extension)

    # Set the config_entityKind
    env['config_entityKind'] = "{}-{}".format(config['variables_prefix']['config_entityKind'],env_suffix)

    return env