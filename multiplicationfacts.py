from config import read_configurations_from_config_file

def get_multiplication_facts(str_table_of, str_limit):

    print("Entering get_multiplication_facts...")
    output_dict = {}
    warning_counter = 0

    # Load Defaults from Config
    envVariables = read_configurations_from_config_file()

    default_table_of = envVariables['multiplication_facts_table_of']
    default_limit = envVariables['multiplication_facts_limit']

    # Perform Validations

    try:
        table_of = int(str_table_of)
    except ValueError:
        # Set the default
        user_message = "Invalid table_of value; Resetting to Default value of {}.".format(default_table_of)
        print(user_message)
        warning_counter = warning_counter + 1
        user_message_key = "Warning" + " " + str(warning_counter)
        output_dict[user_message_key] = user_message
        table_of = default_table_of

    try:
        limit = int(str_limit)
    except ValueError:
        # Set the default
        user_message = "Invalid limit value; Resetting to Default value of {}.".format(default_limit)
        print(user_message)
        warning_counter = warning_counter + 1
        user_message_key = "Warning" + " " + str(warning_counter)
        output_dict[user_message_key] = user_message
        limit = default_limit

    output_dict["tableof"] = table_of
    output_dict["limit"] = limit

    output_value = {}

    for i in range(1, limit+1):
        output_value[i] = table_of*i

    output_dict["result"] = output_value


    user_message = "Final Output: {}".format(output_dict)
    print(user_message)

    return output_dict