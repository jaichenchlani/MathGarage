from random import randint
import datastoreoperations, utilities, config
import datetime

# Load Environment
env = config.get_environment_from_env_file()

def generate_linear_equations(requestData):
    print("Start - Entering generate_linear_equations...")

    # Declare the output dictionary
    generated_linear_equations = declare_output_dictionary()

    # Read config file and and load the random selected puzzle type 
    select_random_equation_config(requestData,generated_linear_equations)
    
    # Process only when there is a valid puzzle selected from Config.
    if generated_linear_equations['config']:
        # Apply Business Rules on Configuration Values.
        # And, if all good, go ahead with generating the puzzle progression
        if is_valid_configuration(generated_linear_equations):
            process_request(generated_linear_equations)
    else:
        # No puzzle selected. Cannot move forward.
        pass

    # Insert the generated Output Dictionary in Datastore
    entityKind = utilities.get_value_by_entityKind_and_key(env['config_entityKind'],"datastore_kind_linear_equations")['config_value']
    insert_response = utilities.insert_in_datastore_and_get_id(entityKind,generated_linear_equations)
    if not insert_response['validOutputReturned']:
        # Error creating datastore entity
        generated_linear_equations['validOutputReturned'] = False
        generated_linear_equations['message'] = insert_response['message']
    else:
        pass
        print("Persisted generated_linear_equations object in Datastore...")
        # Update the Datastore ID in the Output Dictionary
        generated_linear_equations['datastore_id'] = insert_response['id']

    # Return the generated Output Dictionary to the caller.
    print("End - Returning to caller.")
    return generated_linear_equations


def select_random_equation_config(requestData,generated_linear_equations):
    print("Entering select_random_equation_config...")
    print("requestData:{},{}".format(requestData, type(requestData)))
    # difficultyLevel = requestData['difficultyLevel']
    # variableCount = requestData['variableCount']

    # All(i.e. all Difficulty Levels) Valid Equation Configurations from Config
    allEquationConfigurations = utilities.get_value_by_entityKind_and_key(env['config_entityKind'],"linear_equation_configurations")['config_value']
    # print("allEquationConfigurations:{},{}".format(allEquationConfigurations, type(allEquationConfigurations)))
    # print("Total Equation Configurations: {}".format(len(allEquationConfigurations)))

    # Shortlist the valid puzzle configurations based on difficulty level
    # validEquationConfigurations = identify_valid_items_in_list(allEquationConfigurations,difficultyLevel)
    validEquationConfigurations = identify_valid_equation_configs(allEquationConfigurations,requestData)
    # print("Valid Equation Configurations: {}".format(len(validEquationConfigurations)))


    # Select a random equation type
    selected_random_equation_config = {}
    total_types_of_valid_equations = len(validEquationConfigurations)

    if total_types_of_valid_equations > 0:
        random_index = randint(0,total_types_of_valid_equations-1)
        selected_random_equation_config = validEquationConfigurations[random_index]
        generated_linear_equations['config'] = selected_random_equation_config
    else:
        generated_linear_equations['validOutputReturned'] = False
        generated_linear_equations['message'] = "No valid equation configurations found for selected Difficulty Levels."

def declare_output_dictionary():
    generated_linear_equations = {}
    generated_linear_equations['datastore_id'] = 0
    generated_linear_equations['user'] = "Guest"
    generated_linear_equations['create_timestamp'] = datetime.datetime.now()
    generated_linear_equations['last_modified_timestamp'] = datetime.datetime.now()
    generated_linear_equations['config'] = {}
    generated_linear_equations['multipliers'] = []
    generated_linear_equations['equations'] = []
    generated_linear_equations['question'] = []
    generated_linear_equations['answer'] = []
    generated_linear_equations['message'] = ""
    generated_linear_equations['validOutputReturned'] = True
    generated_linear_equations['showUserHelp'] = utilities.get_value_by_entityKind_and_key(env['config_entityKind'],"showUserHelp")['config_value']

    return generated_linear_equations

def is_valid_configuration(generated_linear_equations):
    print("Entering is_valid_configuration...")

     # Number of variables configuration should be greater than 0.
    if (int(generated_linear_equations['config']['number_of_variables']) < 1):
        generated_linear_equations['message'] = "Config Error: Number of variables configuration should be greater than 0."
        generated_linear_equations['validOutputReturned'] = False
        return False

    # Number of variables and the number of items in the Variables list should be equal
    if (int(generated_linear_equations['config']['number_of_variables']) != 
    len(generated_linear_equations['config']['variables'])):
        generated_linear_equations['message'] = "Config Error: Number of variables should be equal to the number of items declared in the variables list."
        generated_linear_equations['validOutputReturned'] = False
        return False

    # All business rules okay. 
    return True

def process_request(generated_linear_equations):
    print("Entering process_request...")
    variable_count = int(generated_linear_equations['config']['number_of_variables']) 
    # Generating 1 variable linear equation
    if variable_count == 1:
        multipliers_count = 2
    else:
        multipliers_count = variable_count ** 2
    
    multipliers = []
    for i in range(1, multipliers_count+1):
        random_index = randint(int(generated_linear_equations['config']['multiplier_limits']['lower']),
        int(generated_linear_equations['config']['multiplier_limits']['upper']))
        # Don't allow a zero in multipliers
        # if (variable_count == 1 and random_index == 0):
        if random_index == 0:
            random_index = 1
        multipliers.append(random_index)    
    generated_linear_equations['multipliers'] = multipliers
    # print("multipliers:{},{}".format(multipliers, type(multipliers)))

    # answers as dictionary.
    answer = []
    for i in range(1,variable_count+1):
        answer_dictionary = {
        "variable": "",
        "system_answer": 0,
        "user_answer": "?",
        "isUserAnswerCorrect": 0
        }
        random_index = randint(int(generated_linear_equations['config']['variable_limits']['lower']),
        int(generated_linear_equations['config']['variable_limits']['upper']))
        answer_dictionary['variable'] = generated_linear_equations['config']['variables'][i-1]
        answer_dictionary['system_answer'] = random_index
        answer.append(answer_dictionary)
        
    generated_linear_equations['answer'] = answer
    # print("answer_dictionary:{},{}".format(answer_dictionary, type(answer_dictionary)))
    # print("answer_list:{},{}".format(answer_list, type(answer_list)))

    # Generate equations and answers
    # Number of linear equations will always be equal to the number of variables.
    equation_count = variable_count
    
    # Loop through the multiplier counts and answers to form the equations
    
    # Initialize the last index upper limit to be equal to the equation count. 
    # This will be used in the for loop below to calculate index lower and upper bounds
    last_index_upper_bound = 0

    for equation_number in range(1,equation_count+1):
        # print("Outer For Loop...")
        # print("equation_number:{},{}".format(equation_number, type(equation_number)))
        # Example:In a 3 variable equation, below is how the logic will work
        # Multipliers: [-4, 1, 1, 3, -2, 0, 2, 2, 3]
        # answer_list: [5, 3, -1]
        # Iteration 1: index_lower_bound = 0; index_upper_bound = 3
        # Iteration 2: index_lower_bound = 3; index_upper_bound = 6
        # Iteration 3: index_lower_bound = 6; index_upper_bound = 9
        if variable_count == 1:
            index_upper_bound = equation_count * equation_number + 1
        else:    
            index_upper_bound = equation_count * equation_number
        index_lower_bound = last_index_upper_bound
        # print("index_lower_bound:{},{}".format(index_lower_bound, type(index_lower_bound)))
        # print("index_upper_bound:{},{}".format(index_upper_bound, type(index_upper_bound)))
        # print("last_index_upper_bound:{},{}".format(last_index_upper_bound, type(last_index_upper_bound)))
        last_index_upper_bound = index_upper_bound
        
        # Loop through the lower and upper bounds to form the 
        # equation LHS(Left Hand Side) and RHS(Right Hand Side)
        # -4x + 1y + 1z = -18
        # 3x - 2y + 0z = 9
        # 2x + 2y + 3z = 13
        # equation['equationLHS'] = ""
        # equation['equationRHS'] = 0
        # Initialize the equation LHS and RHS and the loop control variables
        equation = {"equationLHS": "", "equationRHS": 0}
        answer_list_index = 0
        variables_list_index = 0
        firstIteration = True
        lastIteration = False
        firstExpression = True
        for index in range(index_lower_bound,index_upper_bound):
            # print("Inner For Loop...")
            # print("index:{},{}".format(index, type(index)))
        
            # Identify First Iteration
            if answer_list_index == 0:
                firstIteration = True
            else:
                firstIteration = False

            # Special handling for last(2nd is the last) iteration of 1 variable equation
            if not firstIteration and variable_count == 1:
                oneVariable2ndIterationSpecialHandling = True
            else:
                oneVariable2ndIterationSpecialHandling = False

            # Identify Last Iteration
            if variable_count == 1:
                if answer_list_index == equation_count:
                    lastIteration = True
                else:
                    lastIteration = False
            else:
                if answer_list_index == (equation_count - 1):
                    lastIteration = True
                else:
                    lastIteration = False  

            # print("firstIteration:{},{}".format(firstIteration, type(firstIteration)))
            # print("lastIteration:{},{}".format(lastIteration, type(lastIteration)))
            # print("oneVariable2ndIterationSpecialHandling:{},{}".format(oneVariable2ndIterationSpecialHandling, type(oneVariable2ndIterationSpecialHandling)))

            # Calculate RHS. Easy
            # First 3 items in Multipliers * all 3 items in answer list
            if oneVariable2ndIterationSpecialHandling:
                equation['equationRHS'] += int(multipliers[index])
            else:
                # equation['equationRHS'] += int(multipliers[index]) * int(answer_list[answer_list_index])
                equation['equationRHS'] += int(multipliers[index]) * int(generated_linear_equations['answer'][answer_list_index]['system_answer'])
            
            # Form LHS i.e. the equation "1x + 2y +3z = n". Complicated.
            if firstIteration or firstExpression:
                if int(multipliers[index]) < 0:
                    equation['equationLHS'] += "-"
            
            if oneVariable2ndIterationSpecialHandling:
                if abs(int(multipliers[index])) != 0:
                    equation['equationLHS'] += str(abs(int(multipliers[index]))) 
                    firstExpression = False
            else:
                if abs(int(multipliers[index])) == 1:
                    equation['equationLHS'] += str(generated_linear_equations['config']['variables'][variables_list_index])
                    firstExpression = False
                elif int(multipliers[index]) != 0:
                    equation['equationLHS'] += str(abs(int(multipliers[index])))
                    equation['equationLHS'] += str(generated_linear_equations['config']['variables'][variables_list_index])
                    firstExpression = False
                else:
                    pass
            
            # Determine the +/- sign between the equations, only for iterations other than the last one.
            if not lastIteration and not firstExpression:
                # Not last iteration. Append the RHS with the appropriate sign, based on NEXT multiplier's sign
                if int(multipliers[index+1]) < 0:
                    equation['equationLHS'] += " - "
                elif int(multipliers[index+1]) > 0:
                    equation['equationLHS'] += " + "
                else:
                    pass
            else:
                # Last iteration
                pass

            answer_list_index += 1
            variables_list_index += 1
        
        # print(equation)
        equation_text = "{} = {}".format(equation['equationLHS'],equation['equationRHS'])
        generated_linear_equations['equations'].append(equation)
        generated_linear_equations['question'].append(equation_text)

    return generated_linear_equations

def identify_valid_equation_configs(allItemsInList,requestData):
    difficultyLevel = requestData['difficultyLevel']
    variableCount = requestData['variableCount']
    print("variableCount:{},{}".format(variableCount, type(variableCount)))
    validEquationConfigs = []
    for config in allItemsInList:
        if variableCount[config['variable_count']] == 1:
            if difficultyLevel[config['difficulty_level']] == 1:
                if int(config['active']):
                    validEquationConfigs.append(config)
    return validEquationConfigs

def update_datastore_linear_equations(input_linear_equations):
    print("Entering update_datastore_linear_equations...")
    # Update Datastore Entity
    id = input_linear_equations['datastore_id']
    updated_entity = {
    "last_modified_timestamp": datetime.datetime.now(),
    "answer": input_linear_equations['answer']
    }
    # Get entityKind config from Datastore
    entityKind = utilities.get_value_by_entityKind_and_key(env['config_entityKind'],"datastore_kind_linear_equations")['config_value']
    status = datastoreoperations.update_datastore_entity(entityKind,id,updated_entity)
    return status