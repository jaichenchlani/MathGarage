import datastoreoperations, utilities, config
import inspect, logging,sys
from decimal import Decimal

# Load Environment
env = config.get_environment_from_env_file()

def generate_user_dashboard(request):
    # Standard Logging
    username = request['username']
    logger = logging.getLogger( __name__ )
    module = logger.name
    function = inspect.stack()[0][3]
    print("Function:{}.{}; Argument1:request:{};".format(module,function,username))

    # Declare the output dictionary
    generated_user_dashboard = declare_output_dictionary(username)

    # Get the defined puzzle_categories
    puzzle_categories = utilities.get_value_by_entityKind_and_key(env['config_entityKind'],"puzzle_categories")['config_value']
    
    # Build metrics for each puzzle category
    # puzzle_category = "basic_arithematic_operations"
    puzzle_category = puzzle_categories[0]
    propertyKey = "username"
    propertyValue = username
    entityList = datastoreoperations.get_datastore_entity_by_property(puzzle_category,propertyKey,propertyValue)
    metrics = build_basic_arithematic_operations_metrics(puzzle_category, entityList)
    generated_user_dashboard['metrics_basic_arithematic_operations'] = metrics
    
    # puzzle_category = "linear_equations"
    puzzle_category = puzzle_categories[1]
    propertyKey = "username"
    propertyValue = username
    entityList = datastoreoperations.get_datastore_entity_by_property(puzzle_category,propertyKey,propertyValue)
    metrics = build_linear_equations_metrics(puzzle_category, entityList)
    generated_user_dashboard['metrics_linear_equations'] = metrics

    # puzzle_category = "sequence puzzles"
    puzzle_category = puzzle_categories[2]
    propertyKey = "username"
    propertyValue = username
    entityList = datastoreoperations.get_datastore_entity_by_property(puzzle_category,propertyKey,propertyValue)
    metrics = build_sequence_puzzles_metrics(puzzle_category, entityList)
    generated_user_dashboard['metrics_sequence_puzzles'] = metrics

    # Build a list of common metrics applicable to all puzzle types.
    # This is to help with front display in a ng-repeat table
    build_metrics_applicable_to_all_puzzle_types(generated_user_dashboard)
    # generated_user_dashboard['metrics_applicable_to_all'] = metrics

    return generated_user_dashboard

def declare_output_dictionary(username):
    print("Entering declare_output_dictionary...")
    generated_user_dashboard = {}
    generated_user_dashboard['username'] = username
    generated_user_dashboard['metrics_basic_arithematic_operations'] = {}
    generated_user_dashboard['metrics_linear_equations'] = {}
    generated_user_dashboard['metrics_sequence_puzzles'] = {}
    generated_user_dashboard['metrics_applicable_to_all_header'] = {}
    generated_user_dashboard['metrics_applicable_to_all'] = []
    generated_user_dashboard['message'] = "All metrics generated successfully."
    generated_user_dashboard['validOutputReturned'] = True
    generated_user_dashboard['showUserHelp'] = utilities.get_value_by_entityKind_and_key(env['config_entityKind'],"showUserHelp")['config_value']
    return generated_user_dashboard

def build_basic_arithematic_operations_metrics(puzzle_category, entityList,):
    # Standard Logging
    logger = logging.getLogger( __name__ )
    module = logger.name
    function = inspect.stack()[0][3]
    print("Function:{}.{}; Argument1:puzzle_category:{}; Argument2:entityList;".format(module,function,puzzle_category))
    # Initialize Variables
    # This will hold the calculated metrics.
    metrics = initialize_basic_arithematic_operations_metrics()

    # Process metrics applicable to basic_arithematic_operations
    counter = 1
    for entity in entityList['entityList']:
        # Overall Metrics (Total time is in Hours, while Average time is in Seconds)
        metrics['count_questions_attempted'] += entity['number_of_questions']
        metrics['total_time_spent'] += round(entity['timeTaken']/60,2)

        # Metrics by Difficulty Level
        metrics['count_by_difficulty_level'][entity['config']['difficulty_level']] += entity['number_of_questions']
        metrics['total_time_spent_by_difficulty_level'][entity['config']['difficulty_level']] += round(entity['timeTaken']/60,2)
        
        # Metrics by Operator
        metrics['count_by_operator'][entity['operator']] += entity['number_of_questions']
        metrics['total_time_spent_by_operator'][entity['operator']] += round(entity['timeTaken']/60,2)

        # Question level metrics
        for question in entity['questions']:
            # print(question)
            if question['is_user_answer_correct']:
                metrics['count_by_result']['correct'] += 1
            else:
                metrics['count_by_result']['incorrect'] += 1
        # Distribute the total time taken proportionately by result
        temp = metrics['total_time_spent']*metrics['count_by_result']['correct']/metrics['count_questions_attempted']
        metrics['total_time_spent_by_result']['correct'] +=round(temp,2)
        temp = metrics['total_time_spent']*metrics['count_by_result']['incorrect']/metrics['count_questions_attempted']
        metrics['total_time_spent_by_result']['incorrect'] += round(temp,2)

        counter += 1

    # Calculate Averages (Average time is in Seconds, while Total time is in Hours)
    # Overall
    count = metrics['count_questions_attempted']
    timeTaken = metrics['total_time_spent']*60
    metrics['average_time_per_question'] = calculate_average(puzzle_category, count, timeTaken)
    # By Result
    count = 0
    timeTaken = 0
    for key,value in metrics['average_time_spent_by_result'].items():
        count = metrics['count_by_result'][key]
        timeTaken = metrics['total_time_spent_by_result'][key]
        averageTimeTaken = calculate_average(puzzle_category, count, timeTaken)
        metrics['average_time_spent_by_result'][key] = averageTimeTaken
    # By Difficulty Level
    count = 0
    timeTaken = 0
    for key,value in metrics['average_time_spent_by_difficulty_level'].items():
        count = metrics['count_by_difficulty_level'][key]
        timeTaken = metrics['total_time_spent_by_difficulty_level'][key]
        averageTimeTaken = calculate_average(puzzle_category, count, timeTaken)
        metrics['average_time_spent_by_difficulty_level'][key] = averageTimeTaken
    # By Operator
    count = 0
    timeTaken = 0
    for key,value in metrics['average_time_spent_by_operator'].items():
        count = metrics['count_by_operator'][key]
        timeTaken = metrics['total_time_spent_by_operator'][key]
        averageTimeTaken = calculate_average(puzzle_category, count, timeTaken)
        metrics['average_time_spent_by_operator'][key] = averageTimeTaken
    
    # Calculate Perdentage Score
    temp = metrics['count_by_result']['correct'] * 100/ metrics['count_questions_attempted']
    metrics['percentage_score'] = round(temp,2)

    return metrics

def build_linear_equations_metrics(puzzle_category, entityList):
    # Standard Logging
    logger = logging.getLogger( __name__ )
    module = logger.name
    function = inspect.stack()[0][3]
    print("Function:{}.{}; Argument1:puzzle_category:{}; Argument2:entityList;".format(module,function,puzzle_category))

    # Initialize Variables
    # This will hold the calculated metrics.
    metrics = initialize_linear_equations_metrics()

    # Process metrics applicable to linear equations
    counter = 1
    for entity in entityList['entityList']:
        # Overall Metrics (Total time is in Hours, while Average time is in Seconds)
        metrics['count_questions_attempted'] += entity['config']['number_of_variables']
        metrics['total_time_spent'] += round(entity['timeTaken']/60,2)

        # Metrics by Difficulty Level
        metrics['count_by_difficulty_level'][entity['config']['difficulty_level']] += entity['config']['number_of_variables']
        metrics['total_time_spent_by_difficulty_level'][entity['config']['difficulty_level']] += round(entity['timeTaken']/60,2)
        
        # Metrics by Number of Variables
        metrics['count_by_number_of_variables'][str(entity['config']['number_of_variables'])] += entity['config']['number_of_variables']
        metrics['total_time_spent_by_number_of_variables'][str(entity['config']['number_of_variables'])] += round(entity['timeTaken']/60,2)

        # Question level metrics
        for answer in entity['answer']:
            if answer['isUserAnswerCorrect']:
                metrics['count_by_result']['correct'] += 1
            else:
                metrics['count_by_result']['incorrect'] += 1
        # Distribute the total time taken proportionately by result
        temp = metrics['total_time_spent']*metrics['count_by_result']['correct']/metrics['count_questions_attempted']
        metrics['total_time_spent_by_result']['correct'] += round(temp,2)
        temp = metrics['total_time_spent']*metrics['count_by_result']['incorrect']/metrics['count_questions_attempted']
        metrics['total_time_spent_by_result']['incorrect'] += round(temp,2)

        counter += 1

    # Calculate Averages (Average time is in Seconds, while Total time is in Hours)
    # Overall
    count = metrics['count_questions_attempted']
    timeTaken = metrics['total_time_spent']*60
    metrics['average_time_per_question'] = calculate_average(puzzle_category, count, timeTaken)
    
    # By Result
    count = 0
    timeTaken = 0
    for key,value in metrics['average_time_spent_by_result'].items():
        count = metrics['count_by_result'][key]
        timeTaken = metrics['total_time_spent_by_result'][key]
        averageTimeTaken = calculate_average(puzzle_category, count, timeTaken)
        metrics['average_time_spent_by_result'][key] = averageTimeTaken
    # By Difficulty Level
    count = 0
    timeTaken = 0
    for key,value in metrics['average_time_spent_by_difficulty_level'].items():
        count = metrics['count_by_difficulty_level'][key]
        timeTaken = metrics['total_time_spent_by_difficulty_level'][key]
        averageTimeTaken = calculate_average(puzzle_category, count, timeTaken)
        metrics['average_time_spent_by_difficulty_level'][key] = averageTimeTaken
    # By Number of Variables
    count = 0
    timeTaken = 0
    for key,value in metrics['average_time_spent_by_number_of_variables'].items():
        count = metrics['count_by_number_of_variables'][key]
        timeTaken = metrics['total_time_spent_by_number_of_variables'][key]
        averageTimeTaken = calculate_average(puzzle_category, count, timeTaken)
        metrics['average_time_spent_by_number_of_variables'][key] = averageTimeTaken
    
    # Calculate Perdentage Score
    temp = metrics['count_by_result']['correct'] * 100/ metrics['count_questions_attempted']
    metrics['percentage_score'] = round(temp,2)

    return metrics

def build_sequence_puzzles_metrics(puzzle_category, entityList):
    # Standard Logging
    logger = logging.getLogger( __name__ )
    module = logger.name
    function = inspect.stack()[0][3]
    print("Function:{}.{}; Argument1:puzzle_category:{}; Argument2:entityList;".format(module,function,puzzle_category))

    # Initialize Variables
    # This will hold the calculated metrics.
    metrics = initialize_sequence_puzzles_metrics()

    # Process metrics applicable to sequence puzzles
    counter = 1
    for entity in entityList['entityList']:
        # Overall Metrics (Total time is in Hours, while Average time is in Seconds)
        metrics['count_questions_attempted'] += int(entity['config']['missing_elements_count'])
        metrics['total_time_spent'] += round(entity['timeTaken']/60,2)

        # Metrics by Difficulty Level
        metrics['count_by_difficulty_level'][entity['config']['difficulty_level']] += int(entity['config']['missing_elements_count'])
        metrics['total_time_spent_by_difficulty_level'][entity['config']['difficulty_level']] += round(entity['timeTaken']/60,2)
        
        # Metrics by Number of Missing Elements
        metrics['count_by_number_of_missing_elements'][str(entity['config']['missing_elements_count'])] += int(entity['config']['missing_elements_count'])
        metrics['total_time_spent_by_number_of_missing_elements'][str(entity['config']['missing_elements_count'])] += round(entity['timeTaken']/60,2)

        # Question level metrics
        for missing_element in entity['missing_elements']:
            if missing_element['isUserAnswerCorrect']:
                metrics['count_by_result']['correct'] += 1
            else:
                metrics['count_by_result']['incorrect'] += 1
        # Distribute the total time taken proportionately by result
        temp = metrics['total_time_spent']*metrics['count_by_result']['correct']/metrics['count_questions_attempted']
        metrics['total_time_spent_by_result']['correct'] += round(temp,2)
        temp = metrics['total_time_spent']*metrics['count_by_result']['incorrect']/metrics['count_questions_attempted']
        metrics['total_time_spent_by_result']['incorrect'] += round(temp,2)

        counter += 1

    # Calculate Averages (Average time is in Seconds, while Total time is in Hours)
    # Overall
    count = metrics['count_questions_attempted']
    timeTaken = metrics['total_time_spent']*60
    metrics['average_time_per_question'] = calculate_average(puzzle_category, count, timeTaken)

    # By Result
    count = 0
    timeTaken = 0
    for key,value in metrics['average_time_spent_by_result'].items():
        count = metrics['count_by_result'][key]
        timeTaken = metrics['total_time_spent_by_result'][key]
        averageTimeTaken = calculate_average(puzzle_category, count, timeTaken)
        metrics['average_time_spent_by_result'][key] = averageTimeTaken
    # By Difficulty Level
    count = 0
    timeTaken = 0
    for key,value in metrics['average_time_spent_by_difficulty_level'].items():
        count = metrics['count_by_difficulty_level'][key]
        timeTaken = metrics['total_time_spent_by_difficulty_level'][key]
        averageTimeTaken = calculate_average(puzzle_category, count, timeTaken)
        metrics['average_time_spent_by_difficulty_level'][key] = averageTimeTaken
    # By Number of Missing Elements
    count = 0
    timeTaken = 0
    for key,value in metrics['average_time_spent_by_number_of_missing_elements'].items():
        count = metrics['count_by_number_of_missing_elements'][key]
        timeTaken = metrics['total_time_spent_by_number_of_missing_elements'][key]
        averageTimeTaken = calculate_average(puzzle_category, count, timeTaken)
        metrics['average_time_spent_by_number_of_missing_elements'][key] = averageTimeTaken

    # Calculate Perdentage Score
    temp = metrics['count_by_result']['correct'] * 100/ metrics['count_questions_attempted']
    metrics['percentage_score'] = round(temp,2)
    return metrics

def build_metrics_applicable_to_all_puzzle_types(generated_user_dashboard):
    # Standard Logging
    logger = logging.getLogger( __name__ )
    module = logger.name
    function = inspect.stack()[0][3]
    print("Function:{}.{}; Argument1:generated_user_dashboard dictionary.".format(function,module))

    # Header
    header = {
        "metric_number": "Metric #",
        "metric": "Metric",
        "puzzle_1": "Basic Arithematic Operations",
        "puzzle_2": "Linear Equations",
        "puzzle_3": "Sequence Puzzles"
    }
    generated_user_dashboard['metrics_applicable_to_all_header'] = header

    # Initialize Variables
    # This will hold the calculated metrics.
    metrics = []

    # Number of questions attempted
    count_questions_attempted = {
        "metric": "Questions Attempted",
        "basic_arithematic_operations": generated_user_dashboard['metrics_basic_arithematic_operations']['count_questions_attempted'],
        "linear_equations": generated_user_dashboard['metrics_linear_equations']['count_questions_attempted'],
        "sequence_puzzles": generated_user_dashboard['metrics_sequence_puzzles']['count_questions_attempted']
    }
    metrics.append(count_questions_attempted)

    # Correct Answers
    count_by_result_correct = {
        "metric": "Correct Answers",
        "basic_arithematic_operations": generated_user_dashboard['metrics_basic_arithematic_operations']['count_by_result']['correct'],
        "linear_equations": generated_user_dashboard['metrics_linear_equations']['count_by_result']['correct'],
        "sequence_puzzles": generated_user_dashboard['metrics_sequence_puzzles']['count_by_result']['correct']
    }
    metrics.append(count_by_result_correct)

    # Incorrect Answers
    count_by_result_incorrect = {
        "metric": "Incorrect Answers",
        "basic_arithematic_operations": generated_user_dashboard['metrics_basic_arithematic_operations']['count_by_result']['incorrect'],
        "linear_equations": generated_user_dashboard['metrics_linear_equations']['count_by_result']['incorrect'],
        "sequence_puzzles": generated_user_dashboard['metrics_sequence_puzzles']['count_by_result']['incorrect']
    }
    metrics.append(count_by_result_incorrect)

    # Total Time Spent
    total_time_spent = {
        "metric": "Total Time Spent(Hours)",
        "basic_arithematic_operations": generated_user_dashboard['metrics_basic_arithematic_operations']['total_time_spent'],
        "linear_equations": generated_user_dashboard['metrics_linear_equations']['total_time_spent'],
        "sequence_puzzles": generated_user_dashboard['metrics_sequence_puzzles']['total_time_spent']
    }
    metrics.append(total_time_spent)

    # Average time spent per question
    average_time_per_question = {
        "metric": "Average Time Spent per Question(Secs)",
        "basic_arithematic_operations": generated_user_dashboard['metrics_basic_arithematic_operations']['average_time_per_question'],
        "linear_equations": generated_user_dashboard['metrics_linear_equations']['average_time_per_question'],
        "sequence_puzzles": generated_user_dashboard['metrics_sequence_puzzles']['average_time_per_question']
    }
    metrics.append(average_time_per_question)

    # Percentage Score
    percentage_score = {
        "metric": "Score(%)",
        "basic_arithematic_operations": generated_user_dashboard['metrics_basic_arithematic_operations']['percentage_score'],
        "linear_equations": generated_user_dashboard['metrics_linear_equations']['percentage_score'],
        "sequence_puzzles": generated_user_dashboard['metrics_sequence_puzzles']['percentage_score']
    }
    metrics.append(percentage_score)

    # Total Time Spent on Correct Questions
    total_time_spent_correct = {
        "metric": "Total Time Spent - Correct Answers(Hours)",
        "basic_arithematic_operations": generated_user_dashboard['metrics_basic_arithematic_operations']['total_time_spent_by_result']['correct'],
        "linear_equations": generated_user_dashboard['metrics_linear_equations']['total_time_spent_by_result']['correct'],
        "sequence_puzzles": generated_user_dashboard['metrics_sequence_puzzles']['total_time_spent_by_result']['correct']
    }
    metrics.append(total_time_spent_correct)

    # Total Time Spent on Incorrect Questions
    total_time_spent_incorrect = {
        "metric": "Total Time Spent - Incorrect Answers(Hours)",
        "basic_arithematic_operations": generated_user_dashboard['metrics_basic_arithematic_operations']['total_time_spent_by_result']['incorrect'],
        "linear_equations": generated_user_dashboard['metrics_linear_equations']['total_time_spent_by_result']['incorrect'],
        "sequence_puzzles": generated_user_dashboard['metrics_sequence_puzzles']['total_time_spent_by_result']['incorrect']
    }
    metrics.append(total_time_spent_incorrect)

    # Average Time Spent on Correct Questions
    average_time_spent_correct = {
        "metric": "Average Time Spent - Correct Answers(Secs)",
        "basic_arithematic_operations": generated_user_dashboard['metrics_basic_arithematic_operations']['average_time_spent_by_result']['correct'],
        "linear_equations": generated_user_dashboard['metrics_linear_equations']['average_time_spent_by_result']['correct'],
        "sequence_puzzles": generated_user_dashboard['metrics_sequence_puzzles']['average_time_spent_by_result']['correct']
    }
    metrics.append(average_time_spent_correct)

    # Total Time Spent on Incorrect Questions
    total_time_spent_incorrect = {
        "metric": "Average Time Spent - Incorrect Answers(Secs)",
        "basic_arithematic_operations": generated_user_dashboard['metrics_basic_arithematic_operations']['average_time_spent_by_result']['incorrect'],
        "linear_equations": generated_user_dashboard['metrics_linear_equations']['average_time_spent_by_result']['incorrect'],
        "sequence_puzzles": generated_user_dashboard['metrics_sequence_puzzles']['average_time_spent_by_result']['incorrect']
    }
    metrics.append(total_time_spent_incorrect)

    # Difficulty Level Super Easy Questions
    count_by_difficulty_level_supereasy = {
        "metric": "Super Easy Questions",
        "basic_arithematic_operations": generated_user_dashboard['metrics_basic_arithematic_operations']['count_by_difficulty_level']['supereasy'],
        "linear_equations": generated_user_dashboard['metrics_linear_equations']['count_by_difficulty_level']['supereasy'],
        "sequence_puzzles": generated_user_dashboard['metrics_sequence_puzzles']['count_by_difficulty_level']['supereasy']
    }
    metrics.append(count_by_difficulty_level_supereasy)
    # Total Time Spent on Difficulty Level Super Easy
    total_time_spent_by_difficulty_level_supereasy = {
        "metric": "Super Easy - Total Time Spent",
        "basic_arithematic_operations": generated_user_dashboard['metrics_basic_arithematic_operations']['total_time_spent_by_difficulty_level']['supereasy'],
        "linear_equations": generated_user_dashboard['metrics_linear_equations']['total_time_spent_by_difficulty_level']['supereasy'],
        "sequence_puzzles": generated_user_dashboard['metrics_sequence_puzzles']['total_time_spent_by_difficulty_level']['supereasy']
    }
    metrics.append(total_time_spent_by_difficulty_level_supereasy)
    # Average Time Spent on Difficulty Level Super Easy
    average_time_spent_by_difficulty_level_supereasy = {
        "metric": "Super Easy - Average Time Spent",
        "basic_arithematic_operations": generated_user_dashboard['metrics_basic_arithematic_operations']['average_time_spent_by_difficulty_level']['supereasy'],
        "linear_equations": generated_user_dashboard['metrics_linear_equations']['average_time_spent_by_difficulty_level']['supereasy'],
        "sequence_puzzles": generated_user_dashboard['metrics_sequence_puzzles']['average_time_spent_by_difficulty_level']['supereasy']
    }
    metrics.append(average_time_spent_by_difficulty_level_supereasy)

    # Difficulty Level Easy Questions
    count_by_difficulty_level_easy = {
        "metric": "Easy Questions",
        "basic_arithematic_operations": generated_user_dashboard['metrics_basic_arithematic_operations']['count_by_difficulty_level']['easy'],
        "linear_equations": generated_user_dashboard['metrics_linear_equations']['count_by_difficulty_level']['easy'],
        "sequence_puzzles": generated_user_dashboard['metrics_sequence_puzzles']['count_by_difficulty_level']['easy']
    }
    metrics.append(count_by_difficulty_level_easy)
    # Total Time Spent on Difficulty Level Easy
    total_time_spent_by_difficulty_level_easy = {
        "metric": "Easy - Total Time Spent",
        "basic_arithematic_operations": generated_user_dashboard['metrics_basic_arithematic_operations']['total_time_spent_by_difficulty_level']['easy'],
        "linear_equations": generated_user_dashboard['metrics_linear_equations']['total_time_spent_by_difficulty_level']['easy'],
        "sequence_puzzles": generated_user_dashboard['metrics_sequence_puzzles']['total_time_spent_by_difficulty_level']['easy']
    }
    metrics.append(total_time_spent_by_difficulty_level_easy)
    # Average Time Spent on Difficulty Level Easy
    average_time_spent_by_difficulty_level_easy = {
        "metric": "Easy - Average Time Spent",
        "basic_arithematic_operations": generated_user_dashboard['metrics_basic_arithematic_operations']['average_time_spent_by_difficulty_level']['easy'],
        "linear_equations": generated_user_dashboard['metrics_linear_equations']['average_time_spent_by_difficulty_level']['easy'],
        "sequence_puzzles": generated_user_dashboard['metrics_sequence_puzzles']['average_time_spent_by_difficulty_level']['easy']
    }
    metrics.append(average_time_spent_by_difficulty_level_easy)

    # Difficulty Level Medium Questions
    count_by_difficulty_level_medium = {
        "metric": "Medium Questions",
        "basic_arithematic_operations": generated_user_dashboard['metrics_basic_arithematic_operations']['count_by_difficulty_level']['medium'],
        "linear_equations": generated_user_dashboard['metrics_linear_equations']['count_by_difficulty_level']['medium'],
        "sequence_puzzles": generated_user_dashboard['metrics_sequence_puzzles']['count_by_difficulty_level']['medium']
    }
    metrics.append(count_by_difficulty_level_medium)
    # Total Time Spent on Difficulty Level Medium
    total_time_spent_by_difficulty_level_medium = {
        "metric": "Medium - Total Time Spent",
        "basic_arithematic_operations": generated_user_dashboard['metrics_basic_arithematic_operations']['total_time_spent_by_difficulty_level']['medium'],
        "linear_equations": generated_user_dashboard['metrics_linear_equations']['total_time_spent_by_difficulty_level']['medium'],
        "sequence_puzzles": generated_user_dashboard['metrics_sequence_puzzles']['total_time_spent_by_difficulty_level']['medium']
    }
    metrics.append(total_time_spent_by_difficulty_level_medium)
    # Average Time Spent on Difficulty Level Medium
    average_time_spent_by_difficulty_level_medium = {
        "metric": "Medium - Average Time Spent",
        "basic_arithematic_operations": generated_user_dashboard['metrics_basic_arithematic_operations']['average_time_spent_by_difficulty_level']['medium'],
        "linear_equations": generated_user_dashboard['metrics_linear_equations']['average_time_spent_by_difficulty_level']['medium'],
        "sequence_puzzles": generated_user_dashboard['metrics_sequence_puzzles']['average_time_spent_by_difficulty_level']['medium']
    }
    metrics.append(average_time_spent_by_difficulty_level_medium)

    # Difficulty Level Hard Questions
    count_by_difficulty_level_hard = {
        "metric": "Hard Questions",
        "basic_arithematic_operations": generated_user_dashboard['metrics_basic_arithematic_operations']['count_by_difficulty_level']['hard'],
        "linear_equations": generated_user_dashboard['metrics_linear_equations']['count_by_difficulty_level']['hard'],
        "sequence_puzzles": generated_user_dashboard['metrics_sequence_puzzles']['count_by_difficulty_level']['hard']
    }
    metrics.append(count_by_difficulty_level_hard)
    # Total Time Spent on Difficulty Level Hard
    total_time_spent_by_difficulty_level_hard = {
        "metric": "Hard - Total Time Spent",
        "basic_arithematic_operations": generated_user_dashboard['metrics_basic_arithematic_operations']['total_time_spent_by_difficulty_level']['hard'],
        "linear_equations": generated_user_dashboard['metrics_linear_equations']['total_time_spent_by_difficulty_level']['hard'],
        "sequence_puzzles": generated_user_dashboard['metrics_sequence_puzzles']['total_time_spent_by_difficulty_level']['hard']
    }
    metrics.append(total_time_spent_by_difficulty_level_hard)
    # Average Time Spent on Difficulty Level Hard
    average_time_spent_by_difficulty_level_hard = {
        "metric": "Hard - Average Time Spent",
        "basic_arithematic_operations": generated_user_dashboard['metrics_basic_arithematic_operations']['average_time_spent_by_difficulty_level']['hard'],
        "linear_equations": generated_user_dashboard['metrics_linear_equations']['average_time_spent_by_difficulty_level']['hard'],
        "sequence_puzzles": generated_user_dashboard['metrics_sequence_puzzles']['average_time_spent_by_difficulty_level']['hard']
    }
    metrics.append(average_time_spent_by_difficulty_level_hard)

    # Difficulty Level Super Hard Questions
    count_by_difficulty_level_superhard = {
        "metric": "Super Hard Questions",
        "basic_arithematic_operations": generated_user_dashboard['metrics_basic_arithematic_operations']['count_by_difficulty_level']['superhard'],
        "linear_equations": generated_user_dashboard['metrics_linear_equations']['count_by_difficulty_level']['superhard'],
        "sequence_puzzles": generated_user_dashboard['metrics_sequence_puzzles']['count_by_difficulty_level']['superhard']
    }
    metrics.append(count_by_difficulty_level_superhard)
    # Total Time Spent on Difficulty Level Super Hard
    total_time_spent_by_difficulty_level_superhard = {
        "metric": "Super Hard - Total Time Spent",
        "basic_arithematic_operations": generated_user_dashboard['metrics_basic_arithematic_operations']['total_time_spent_by_difficulty_level']['superhard'],
        "linear_equations": generated_user_dashboard['metrics_linear_equations']['total_time_spent_by_difficulty_level']['superhard'],
        "sequence_puzzles": generated_user_dashboard['metrics_sequence_puzzles']['total_time_spent_by_difficulty_level']['superhard']
    }
    metrics.append(total_time_spent_by_difficulty_level_superhard)
    # Average Time Spent on Difficulty Level Super Hard
    average_time_spent_by_difficulty_level_superhard = {
        "metric": "Super Hard - Average Time Spent",
        "basic_arithematic_operations": generated_user_dashboard['metrics_basic_arithematic_operations']['average_time_spent_by_difficulty_level']['superhard'],
        "linear_equations": generated_user_dashboard['metrics_linear_equations']['average_time_spent_by_difficulty_level']['superhard'],
        "sequence_puzzles": generated_user_dashboard['metrics_sequence_puzzles']['average_time_spent_by_difficulty_level']['superhard']
    }
    metrics.append(average_time_spent_by_difficulty_level_superhard)

    # Populate the response dictionary with the metrics built
    generated_user_dashboard['metrics_applicable_to_all'] = metrics

def calculate_average(puzzle_category, count, timeTaken):
    # Standard Logging
    logger = logging.getLogger( __name__ )
    module = logger.name
    function = inspect.stack()[0][3]
    print("Function:{}.{}; Argument1:puzzle_category:{}; Argument3:Count:{}; Argument4:timeTaken:{}".format(module,function,puzzle_category, count, timeTaken))
    try:
        averageTime = timeTaken / count
        averageTime = round(averageTime,2)
    except Exception as e:
        # Error performing the DB operation
        errorMessage = "Error calculating average time spent for Puzzle Category {} Count {} and timeTaken {}.".format(puzzle_category,count,timeTaken)
        errorMessage = "{0} Stacktrace: {1}".format(errorMessage,e)
        print(errorMessage)
        return 0
    else:
        return averageTime

def initialize_basic_arithematic_operations_metrics():
    # Standard Logging
    logger = logging.getLogger( __name__ )
    module = logger.name
    function = inspect.stack()[0][3]
    print("Function:{}.{};".format(module,function))
    metrics = {
        "count_questions_attempted": 0,
        "total_time_spent": 0,
        "average_time_per_question": 0,
        "count_by_result": {
            "correct": 0,
            "incorrect": 0
        },
        "total_time_spent_by_result": {
            "correct": 0,
            "incorrect": 0
        },
        "average_time_spent_by_result": {
            "correct": 0,
            "incorrect": 0
        },
        "percentage_score": 0,
        "count_by_difficulty_level": {
            "supereasy": 0, 
            "easy": 0, 
            "medium": 0, 
            "hard": 0, 
            "superhard": 0
        },
        "total_time_spent_by_difficulty_level": {
            "supereasy": 0, 
            "easy": 0, 
            "medium": 0, 
            "hard": 0, 
            "superhard": 0
        },
        "average_time_spent_by_difficulty_level": {
            "supereasy": 0, 
            "easy": 0, 
            "medium": 0, 
            "hard": 0, 
            "superhard": 0
        },
        "count_by_operator": {
            "+": 0, 
            "-": 0, 
            "x": 0, 
            "/": 0
        },
        "total_time_spent_by_operator": {
            "+": 0, 
            "-": 0, 
            "x": 0, 
            "/": 0
        },
        "average_time_spent_by_operator": {
            "+": 0, 
            "-": 0, 
            "x": 0, 
            "/": 0
        }
    }
    return metrics

def initialize_linear_equations_metrics():
    # Standard Logging
    logger = logging.getLogger( __name__ )
    module = logger.name
    function = inspect.stack()[0][3]
    print("Function:{}.{};".format(module,function))
    metrics = {
        "count_questions_attempted": 0,
        "total_time_spent": 0,
        "average_time_per_question": 0,
        "count_by_result": {
            "correct": 0,
            "incorrect": 0
        },
        "total_time_spent_by_result": {
            "correct": 0,
            "incorrect": 0
        },
        "average_time_spent_by_result": {
            "correct": 0,
            "incorrect": 0
        },
        "percentage_score": 0,
        "count_by_difficulty_level": {
            "supereasy": 0, 
            "easy": 0, 
            "medium": 0, 
            "hard": 0, 
            "superhard": 0
        },
        "total_time_spent_by_difficulty_level": {
            "supereasy": 0, 
            "easy": 0, 
            "medium": 0, 
            "hard": 0, 
            "superhard": 0
        },
        "average_time_spent_by_difficulty_level": {
            "supereasy": 0, 
            "easy": 0, 
            "medium": 0, 
            "hard": 0, 
            "superhard": 0
        },
        "count_by_number_of_variables": {
            "1": 0, 
            "2": 0, 
            "3": 0, 
            "4": 0,
            "5": 0, 
            "6": 0, 
            "7": 0, 
            "8": 0,
            "9": 0, 
            "10": 0
        },
        "total_time_spent_by_number_of_variables": {
            "1": 0, 
            "2": 0, 
            "3": 0, 
            "4": 0,
            "5": 0, 
            "6": 0, 
            "7": 0, 
            "8": 0,
            "9": 0, 
            "10": 0
        },
        "average_time_spent_by_number_of_variables": {
            "1": 0, 
            "2": 0, 
            "3": 0, 
            "4": 0,
            "5": 0, 
            "6": 0, 
            "7": 0, 
            "8": 0,
            "9": 0, 
            "10": 0
        }
    }
    return metrics

def initialize_sequence_puzzles_metrics():
    # Standard Logging
    logger = logging.getLogger( __name__ )
    module = logger.name
    function = inspect.stack()[0][3]
    print("Function:{}.{};".format(module,function))
    metrics = {
        "count_questions_attempted": 0,
        "total_time_spent": 0,
        "average_time_per_question": 0,
        "count_by_result": {
            "correct": 0,
            "incorrect": 0
        },
        "total_time_spent_by_result": {
            "correct": 0,
            "incorrect": 0
        },
        "average_time_spent_by_result": {
            "correct": 0,
            "incorrect": 0
        },
        "percentage_score": 0,
        "count_by_difficulty_level": {
            "supereasy": 0, 
            "easy": 0, 
            "medium": 0, 
            "hard": 0, 
            "superhard": 0
        },
        "total_time_spent_by_difficulty_level": {
            "supereasy": 0, 
            "easy": 0, 
            "medium": 0, 
            "hard": 0, 
            "superhard": 0
        },
        "average_time_spent_by_difficulty_level": {
            "supereasy": 0, 
            "easy": 0, 
            "medium": 0, 
            "hard": 0, 
            "superhard": 0
        },
        "count_by_number_of_missing_elements": {
            "1": 0, 
            "2": 0, 
            "3": 0
        },
        "total_time_spent_by_number_of_missing_elements": {
            "1": 0, 
            "2": 0, 
            "3": 0
        },
        "average_time_spent_by_number_of_missing_elements": {
            "1": 0, 
            "2": 0, 
            "3": 0
        }
    }
    return metrics