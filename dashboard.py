import datastoreoperations, utilities, config
import inspect, logging,sys
from decimal import Decimal

# Load Environment
env = config.get_environment_from_env_file()

def generate_user_dashboard(username):
    # Standard Logging
    logger = logging.getLogger( __name__ )
    module = logger.name
    function = inspect.stack()[0][3]
    print("Function:{}.{}; Argument1:username:{};".format(module,function,username))

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

    return generated_user_dashboard

def declare_output_dictionary(username):
    print("Entering declare_output_dictionary...")
    generated_user_dashboard = {}
    generated_user_dashboard['username'] = username
    generated_user_dashboard['metrics_basic_arithematic_operations'] = {}
    generated_user_dashboard['metrics_linear_equations'] = {}
    generated_user_dashboard['metrics_sequence_puzzles'] = {}
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

    # "puzzle_categories": ["basic_arithematic_operations","linear_equations","sequence_puzzles"],
    # Process metrics applicable to basic_arithematic_operations
    counter = 1
    if puzzle_category == "basic_arithematic_operations":
        for entity in entityList['entityList']:
            # Overall Metrics
            metrics['count_questions_attempted'] += entity['number_of_questions']
            metrics['total_time_spent'] = round(entity['timeTaken'],2)

            # Metrics by Difficulty Level
            metrics['count_by_difficulty_level'][entity['config']['difficulty_level']] += entity['number_of_questions']
            metrics['total_time_spent_by_difficulty_level'][entity['config']['difficulty_level']] += round(entity['timeTaken'],2)
            
            # Metrics by Operator
            metrics['count_by_operator'][entity['operator']] += entity['number_of_questions']
            metrics['total_time_spent_by_operator'][entity['operator']] += round(entity['timeTaken'],2)

            # Question level metrics
            for question in entity['questions']:
                # print(question)
                if question['is_user_answer_correct']:
                    metrics['count_by_result']['correct'] += 1
                else:
                    metrics['count_by_result']['incorrect'] += 1
            # Distribute the total time taken proportionately by result
            temp = metrics['total_time_spent']*metrics['count_by_result']['correct']/metrics['count_questions_attempted']
            metrics['total_time_spent_by_result']['correct'] = round(temp,2)
            temp = metrics['total_time_spent']*metrics['count_by_result']['incorrect']/metrics['count_questions_attempted']
            metrics['total_time_spent_by_result']['incorrect'] = round(temp,2)

            counter += 1

        # Calculate Averages
        # Overall
        count = metrics['count_questions_attempted']
        timeTaken = metrics['total_time_spent']
        metrics['average_time_per_question'] = calculate_average(puzzle_category, entity['datastore_id'], count, timeTaken)
        # By Difficulty Level
        count = metrics['count_by_difficulty_level'][entity['config']['difficulty_level']]
        timeTaken = metrics['total_time_spent_by_difficulty_level'][entity['config']['difficulty_level']]
        metrics['average_time_spent_by_difficulty_level'][entity['config']['difficulty_level']] = calculate_average(puzzle_category, entity['datastore_id'], count, timeTaken)
        # By Operator
        count = metrics['count_by_operator'][entity['operator']]
        timeTaken = metrics['total_time_spent_by_operator'][entity['operator']]
        metrics['average_time_spent_by_operator'][entity['operator']] = calculate_average(puzzle_category, entity['datastore_id'], count, timeTaken)
        # By Result
        count = metrics['count_by_result']['correct']
        timeTaken = metrics['total_time_spent_by_result']['correct']
        metrics['total_time_spent_by_result']['correct'] = calculate_average(puzzle_category, entity['datastore_id'], count, timeTaken)
        count = metrics['count_by_result']['incorrect']
        timeTaken = metrics['total_time_spent_by_result']['incorrect']
        metrics['total_time_spent_by_result']['incorrect'] = calculate_average(puzzle_category, entity['datastore_id'], count, timeTaken)

    return metrics

def build_linear_equations_metrics(puzzle_category, entityList):
    # Standard Logging
    logger = logging.getLogger( __name__ )
    module = logger.name
    function = inspect.stack()[0][3]
    print("Function:{}.{}; Argument1:puzzle_category:{}; Argument2:entityList;".format(module,function,puzzle_category))
    return metrics

def build_sequence_puzzles_metrics(puzzle_category, entityList):
    # Standard Logging
    logger = logging.getLogger( __name__ )
    module = logger.name
    function = inspect.stack()[0][3]
    print("Function:{}.{}; Argument1:puzzle_category:{}; Argument2:entityList;".format(module,function,puzzle_category))
    return metrics

def calculate_average(puzzle_category, datastore_id, count, timeTaken):
    # Standard Logging
    logger = logging.getLogger( __name__ )
    module = logger.name
    function = inspect.stack()[0][3]
    print("Function:{}.{}; Argument1:puzzle_category:{}; Argument2:Datastore ID:{}; Argument3:Count:{}; Argument4:timeTaken:{}".format(module,function,puzzle_category, datastore_id, count, timeTaken))
    try:
        averageTime = timeTaken / count
        averageTime = round(averageTime,2)
    except Exception as e:
        # Error performing the DB operation
        errorMessage = "Error calculating average time spent for Puzzle Category {} Datastore ID {}.".format(puzzle_category,datastore_id)
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