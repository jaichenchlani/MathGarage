from utilities import identify_valid_items_in_list
from sequencepuzzlegenerator import generate_sequence_puzzle
from linearequationsgenerator import generate_linear_equations
from basicarithmaticoperations import generate_basic_arithmatic_operations
from login import login

# Test only. Comment out for Production
difficultyLevel = { 
    "supereasy": 1, 
    "easy": 1, 
    "medium": 1, 
    "hard": 1, 
    "superhard": 1
    }
print("difficultyLevel:{},{}\n\n".format(difficultyLevel, type(difficultyLevel)))

# Test Sequence Puzzle Generator
# puzzle = generate_sequence_puzzle(difficultyLevel)
# print("\nMissing Elements:{}".format(puzzle['config']['missing_elements_count']))
# print("Puzzle:{}\n".format(puzzle['question']))

# Test Linear Equations Generator
# for i in range(1,10):
#     print("Iteration # {}:".format(i))
#     result = generate_linear_equations(difficultyLevel)
#     print("\n")
#     print("Difficulty Level: {}".format(result['config']['difficulty_level']))
#     print("Configuration: {}".format(result['config']['description']))
#     for count, equation in enumerate(result['question'], start=1):
#         print("Equation # {}: {}".format(count, equation))
#     print("Answer: {}\n".format(result['answer']))
#     print("\n")

# Test Basick Arithematic Operations
operation_request = {
    "operator": "x",
    "first_number_lower_limit": -99,
    "first_number_upper_limit": 99,
    "second_number_lower_limit": -9,
    "second_number_upper_limit": 9,
    "number_of_questions": 56
}

response = generate_basic_arithmatic_operations(operation_request)
for question in response['questions']:
    print("{} {} {} = {}".format(question['first_number'],question['operator'],question['second_number'],question['answer']))
    
# Test Login
# google_user = {
#     "name": "Jai Chenchlani",
#     "email": "jaichenchlani@gmail.com"
# }
# store_sign_in_info(google_user)