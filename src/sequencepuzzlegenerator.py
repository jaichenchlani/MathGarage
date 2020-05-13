from random import randint
import datastoreoperations, utilities, config
import datetime

# Load Environment
env = config.get_environment_from_env_file()

def generate_sequence_puzzle(requestData):
    print("Start - Entering generate_sequence_puzzle...")

    difficultyLevel = requestData['difficultyLevel']
    # Declare the output dictionary
    generated_sequence_puzzle = declare_output_dictionary(requestData)

    # Read config file and and load the random selected puzzle type 
    selected_random_puzzle = select_random_sequence_puzzle(difficultyLevel,generated_sequence_puzzle)
    # print("Selected Puzzle Configuration:{}".format(selected_random_puzzle))

    # Process only when there is a valid puzzle selected from Config.
    if not selected_random_puzzle:
        # No valid config. Cannot move forward.
        return generated_sequence_puzzle
    
    # Apply Business Rules on Configuration Values.
    # And, if all good, go ahead with generating the puzzle progression
    if not is_valid_configuration(selected_random_puzzle, generated_sequence_puzzle):
        # Not a valid config. Cannot move forward.
        return generated_sequence_puzzle

    # All good. Go ahead and process.
    process_request(generated_sequence_puzzle)
    
    # Insert the generated Output Dictionary in Datastore
    # Get entityKind config from Datastore
    entityKind = utilities.get_value_by_entityKind_and_key(env['config_entityKind'],"datastore_kind_sequence_puzzles")['config_value']
    insert_response = utilities.insert_in_datastore_and_get_id(entityKind,generated_sequence_puzzle)
    if not insert_response['validOutputReturned']:
        # Error creating datastore entity
        generated_sequence_puzzle['validOutputReturned'] = False
        generated_sequence_puzzle['message'] = insert_response['message']
    else:
        pass
        print("Persisted generated_linear_equations object in Datastore...")
        # Update the Datastore ID in the Output Dictionary
        generated_sequence_puzzle['datastore_id'] = insert_response['id']

    # Return the generated Output Dictionary to the caller.
    print("End - Returning to caller.")
    return generated_sequence_puzzle


# Apply Business Rules on Configuration Values
def is_valid_configuration(selected_random_puzzle,generated_sequence_puzzle):
    print("Entering is_valid_configuration...")

    # Size should be a minimum of 4
    if int(selected_random_puzzle['size']) < 4:
        generated_sequence_puzzle['message'] = "Config Error: Size Count cannot less than 4."
        return False

    # Missing Elements Count cannot be zero.
    if int(selected_random_puzzle['missing_elements_count']) == 0:
        generated_sequence_puzzle['message'] = "Config Error: Missing Elements Count cannot be Zero."
        return False

    # Missing Elements Count shuld be less than half of the Sequence Size
    if int(selected_random_puzzle['missing_elements_count']) >= int(selected_random_puzzle['size']) // 2:
        generated_sequence_puzzle['message'] = "Config Error: Missing Elements Count cannot be greater than half of Size."
        return False

    # All business rules okay. 
    return True


def process_request(generated_sequence_puzzle):
    print("Entering process_request...")
    print("Generating {} Sequence...".format(generated_sequence_puzzle['config']['type']))
    
    # Get the first element of the sequence based on the lower and the upper limits from Config
    firstElement = randint(int(generated_sequence_puzzle['config']['first_element_lower_limit']),
    int(generated_sequence_puzzle['config']['first_element_upper_limit']))
    # if the random firstElement turns out to be 0, hard code it to 1(any other for that matter).
    if firstElement == 0:
        firstElement = 1
    # print("firstElement:{},{}".format(firstElement, type(firstElement)))
    generated_sequence_puzzle['first_element'] = firstElement

    # Generate the hop ranging from negative hop limit to possitive hop limit
    hop = randint(-int(generated_sequence_puzzle['config']['hop_limit']),
    int(generated_sequence_puzzle['config']['hop_limit']))
    # if the random hop turns out to be 0, 1 or -1 , hard code it to 2(any other for that matter).
    if hop in (-1, 0, 1):
        hop = 2
    # print("hop:{},{}".format(hop, type(hop)))
    generated_sequence_puzzle['hop'] = hop

    # Generate the answer list
    generate_answer_list(generated_sequence_puzzle,firstElement,hop)

    # Generate the question list
    generate_question_list(generated_sequence_puzzle)

def generate_answer_list(generated_sequence_puzzle,firstElement,hop):
    print("Entering generate_answer_list...")
    # First Element of the sequence will always be firstElement
    generated_sequence_puzzle['answer'].append(firstElement)
    
    # Populate the logic/rationale.
    answer_logic = {}
    answer_logic['index'] = 1
    answer_logic['element'] = firstElement
    answer_logic['remarks'] = "Random."
    generated_sequence_puzzle['answer_logic'].append(answer_logic)

    # lastElement will be needed in the for loops below to help populate the logic/rationale.
    lastElement = firstElement

    iteration = 1
    if generated_sequence_puzzle['config']['type'] == "arithematic":
        for item in range(2,int(generated_sequence_puzzle['config']['size'])+1):
            nextElement = generated_sequence_puzzle['answer'][-1] + hop
            generated_sequence_puzzle['answer'].append(nextElement)
            # Populate the logic/rationale.
            answer_logic = {}
            answer_logic['index'] = iteration+1
            answer_logic['element'] = nextElement
            answer_logic['remarks'] = "{} + {}".format(lastElement,hop)
            generated_sequence_puzzle['answer_logic'].append(answer_logic)
            lastElement = nextElement
            iteration += 1
        generated_sequence_puzzle['message'] = "Simple Arithematic Progression starting {} with a hop of {}.".format(firstElement,hop)
    
    elif generated_sequence_puzzle['config']['type'] == "geometric":
        for item in range(2,int(generated_sequence_puzzle['config']['size'])+1):
            nextElement = generated_sequence_puzzle['answer'][-1] * hop
            generated_sequence_puzzle['answer'].append(nextElement)
            # Populate the logic/rationale.
            answer_logic = {}
            answer_logic['index'] = iteration+1
            answer_logic['element'] = nextElement
            answer_logic['remarks'] = "{} x {}".format(lastElement,hop)
            generated_sequence_puzzle['answer_logic'].append(answer_logic)
            lastElement = nextElement
            iteration += 1
        generated_sequence_puzzle['message'] = "Simple Geometric Progression starting {} with a hop of {}.".format(firstElement,hop)
    
    elif generated_sequence_puzzle['config']['type'] == "hybrid1-arithematic":
        for item in range(2,int(generated_sequence_puzzle['config']['size'])+1):
            nextElement = generated_sequence_puzzle['answer'][-1] + hop + iteration
            generated_sequence_puzzle['answer'].append(nextElement)
            # Populate the logic/rationale.
            answer_logic = {}
            answer_logic['index'] = iteration+1
            answer_logic['element'] = nextElement
            answer_logic['remarks'] = "{} + {} + {}".format(lastElement,hop, iteration)
            generated_sequence_puzzle['answer_logic'].append(answer_logic)
            lastElement = nextElement
            iteration += 1
        generated_sequence_puzzle['message'] = "Arithematic Progression starting {} with a hop of {} and an additional iteration hop.".format(firstElement,hop)
    
    elif generated_sequence_puzzle['config']['type'] == "hybrid2-arithematic":
        for item in range(2,int(generated_sequence_puzzle['config']['size'])+1):
            nextElement = generated_sequence_puzzle['answer'][-1] + hop + iteration*2
            generated_sequence_puzzle['answer'].append(nextElement)
            # Populate the logic/rationale.
            answer_logic = {}
            answer_logic['index'] = iteration+1
            answer_logic['element'] = nextElement
            answer_logic['remarks'] = "{} + {} + ({}x2)".format(lastElement,hop, iteration)
            generated_sequence_puzzle['answer_logic'].append(answer_logic)
            lastElement = nextElement
            iteration += 1
        generated_sequence_puzzle['message'] = "Arithematic Progression starting {} with a hop of {} and an additional iteration*2 hop.".format(firstElement,hop)
    
    elif generated_sequence_puzzle['config']['type'] == "hybrid3-arithematic":
        for item in range(2,int(generated_sequence_puzzle['config']['size'])+1):
            nextElement = generated_sequence_puzzle['answer'][-1] + hop + iteration*3
            generated_sequence_puzzle['answer'].append(nextElement)
            # Populate the logic/rationale.
            answer_logic = {}
            answer_logic['index'] = iteration+1
            answer_logic['element'] = nextElement
            answer_logic['remarks'] = "{} + {} + ({}x3)".format(lastElement,hop, iteration)
            generated_sequence_puzzle['answer_logic'].append(answer_logic)
            lastElement = nextElement
            iteration += 1
        generated_sequence_puzzle['message'] = "Arithematic Progression starting {} with a hop of {} and an additional iteration*3 hop.".format(firstElement,hop)
    
    elif generated_sequence_puzzle['config']['type'] == "hybrid4-arithematic":
        for item in range(2,int(generated_sequence_puzzle['config']['size'])+1):
            nextElement = generated_sequence_puzzle['answer'][-1] + hop + iteration*4
            generated_sequence_puzzle['answer'].append(nextElement)
            # Populate the logic/rationale.
            answer_logic = {}
            answer_logic['index'] = iteration+1
            answer_logic['element'] = nextElement
            answer_logic['remarks'] = "{} + {} + ({}x3)".format(lastElement,hop, iteration)
            generated_sequence_puzzle['answer_logic'].append(answer_logic)
            lastElement = nextElement
            iteration += 1
        generated_sequence_puzzle['message'] = "Arithematic Progression starting {} with a hop of {} and an additional iteration*4 hop.".format(firstElement,hop)
    
    else:
        generated_sequence_puzzle['validOutputReturned'] = False
        generated_sequence_puzzle['message'] = "Invalid Puzzle Type. Cannot generate sequence."

def generate_question_list(generated_sequence_puzzle):
    print("Entering generate_question_list...")
    # Identify the missing elements list based on Size and Mising Elements count defined in Config
    missing_elements_list = identify_missing_elements_positions(generated_sequence_puzzle['config']['size'],
    int(generated_sequence_puzzle['config']['missing_elements_count']))

    # Loop through the Answer Set and replace the Missing Elements positions with '?'
    elementPositionNumber = 1
    for questionElement in generated_sequence_puzzle['answer'][:]:
        missing_elements = {}
        if elementPositionNumber in missing_elements_list:
            generated_sequence_puzzle['question'].append('?')
            missing_elements['user_answer'] = "?"
            missing_elements['system_answer'] = generated_sequence_puzzle['answer'][elementPositionNumber-1]
            missing_elements['isUserAnswerCorrect'] = 0
            generated_sequence_puzzle['missing_elements'].append(missing_elements)
        else:
            generated_sequence_puzzle['question'].append(generated_sequence_puzzle['answer'][elementPositionNumber-1])
        elementPositionNumber += 1


def identify_missing_elements_positions(size,count):
    print("Entering identify_missing_elements_positions...")
    missing_elements_list = []
    whileIteration = 1
    keepGoing = True

    while (keepGoing):
        # print("whileIteration:{},{}".format(whileIteration, type(whileIteration)))
        firstMissingElementPosition = randint(1,int(size))
        missing_elements_list.append(firstMissingElementPosition)
        # Add the position only if it's not already there.
        missing_elements_list.append(firstMissingElementPosition) if firstMissingElementPosition not in missing_elements_list else None
        if len(missing_elements_list) >= count:
            keepGoing = False
        whileIteration += 1

    return missing_elements_list


def select_random_sequence_puzzle(difficultyLevel,generated_sequence_puzzle):
    print("Entering select_random_sequence_puzzle...")
    # print("difficultyLevel:{},{}".format(difficultyLevel, type(difficultyLevel)))
    
    # All(i.e. all Difficulty Levels) Valid Puzzle Configurations from Config
    allPuzzleConfigurations = utilities.get_value_by_entityKind_and_key(env['config_entityKind'],"puzzle_configurations")['config_value']
    # print("allPuzzleConfigurations:{},{}".format(allPuzzleConfigurations, type(allPuzzleConfigurations)))
    # print("Total Puzzle Configurations: {}".format(len(allPuzzleConfigurations)))

    # Shortlist the valid puzzle configurations based on difficulty level
    validPuzzleConfigurations = utilities.identify_valid_items_in_list(allPuzzleConfigurations,difficultyLevel)
    # print("Valid Puzzle Configurations: {}".format(len(validPuzzleConfigurations)))

    # Select a random puzzle type
    selected_random_puzzle = {}
    total_types_of_valid_puzzles = len(validPuzzleConfigurations)

    if total_types_of_valid_puzzles > 0:
        random_index = randint(0,total_types_of_valid_puzzles-1)
        selected_random_puzzle = validPuzzleConfigurations[random_index]
        generated_sequence_puzzle['config'] = selected_random_puzzle
    else:
        generated_sequence_puzzle['validOutputReturned'] = False
        generated_sequence_puzzle['message'] = "No valid puzzle configurations found for selected Difficulty Levels."

    return selected_random_puzzle

def declare_output_dictionary(requestData):
    generated_sequence_puzzle = {}
    generated_sequence_puzzle['datastore_id'] = 0
    if requestData['username']:
        generated_sequence_puzzle['username'] = requestData['username']
    else:
        generated_sequence_puzzle['username'] = "guest"
    generated_sequence_puzzle['userAnswerCorrect'] = False
    generated_sequence_puzzle['timeTaken'] = 0
    generated_sequence_puzzle['create_timestamp'] = datetime.datetime.now()
    generated_sequence_puzzle['last_modified_timestamp'] = datetime.datetime.now()
    generated_sequence_puzzle['config'] = {}
    generated_sequence_puzzle['first_element'] = 0
    generated_sequence_puzzle['hop'] = 0
    generated_sequence_puzzle['question'] = []
    generated_sequence_puzzle['answer'] = []
    generated_sequence_puzzle['missing_elements'] = []
    generated_sequence_puzzle['answer_logic'] = []
    generated_sequence_puzzle['message'] = ""
    generated_sequence_puzzle['validOutputReturned'] = True
    generated_sequence_puzzle['showUserHelp'] = utilities.get_value_by_entityKind_and_key(env['config_entityKind'],"showUserHelp")['config_value']

    return generated_sequence_puzzle

def update_datastore_sequence_puzzles(input_sequence_puzzles):
    print("Entering update_datastore_sequence_puzzles...")
    # Update Datastore Entity
    id = input_sequence_puzzles['datastore_id']
    updated_entity = {
    "last_modified_timestamp": datetime.datetime.now(),
    "missing_elements": input_sequence_puzzles['missing_elements'],
    "timeTaken": input_sequence_puzzles['timeTaken'],
    "userAnswerCorrect": input_sequence_puzzles['userAnswerCorrect']
    }
    # Get entityKind config from Datastore
    entityKind = utilities.get_value_by_entityKind_and_key(env['config_entityKind'],"datastore_kind_sequence_puzzles")['config_value']
    status = datastoreoperations.update_datastore_entity(entityKind,id,updated_entity)
    return status


