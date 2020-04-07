from utilities import identify_valid_items_in_list
from sequencepuzzlegenerator import generate_sequence_puzzle
from linearequationsgenerator import generate_linear_equations

# Test only. Comment out for Production
difficultyLevel = { 
    "supereasy": 1, 
    "easy": 1, 
    "medium": 1, 
    "hard": 1, 
    "superhard": 1
    }
print("difficultyLevel:{},{}\n\n".format(difficultyLevel, type(difficultyLevel)))

puzzle = generate_sequence_puzzle(difficultyLevel)
print("\nMissing Elements:{}".format(puzzle['config']['missing_elements_count']))
print("Puzzle:{}\n".format(puzzle['question']))


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