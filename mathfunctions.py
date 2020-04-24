from utilities import is_valid_integer

def convert_decimal_to_binary(strInput):
    print("Entering convert_decimal_to_binary...")
    
    # print("strInput:{}; Type of strInput:{}".format(strInput,type(strInput)))

    output_dict = {}
    output_dict['answer'] = 0
    output_dict['error'] = ""

    try:
        n = int(strInput)
    except Exception as e:
        output_dict['error'] = "Error. Cannot convert a String to Binary."
        return output_dict

    answer = ""
    counter = 1
    keepgoing = True
    originalNumber = n

    if (n < 0):
        output_dict['error'] = "Error. Cannot convert a negative number to Binary."
        return output_dict
    if (n == 0 or n == 1):
        output_dict['answer'] = n
        print(output_dict)
        return output_dict

    while (keepgoing):
        answer += str(n % 2)
        # print("KeepGoing:{}; Counter:{}; N:{}; Answer:{}".format(keepgoing,counter,n,answer))
        
        n = n//2

        if (n == 1):
            keepgoing = False
            answer += "1"
            # print("KeepGoing:{}; Counter:{}; N:{}; Answer:{}".format(keepgoing,counter,n,answer))
        
        counter = counter + 1
        
    output_dict['answer'] = answer[::-1]
    print(output_dict)
    return output_dict


def isPrime(n):
    print("Entering isPrime...")
    pass

def isEven(n):
    print("Entering isEven...")
    # Initialize Response Dictionary
    response = {
        "result": False,
        "message": "",
        "validOutputReturned": True
    }
    # Validate the input argument to be a valid integer
    if is_valid_integer(n):
        if n % 2 == 0:
            # Valid Input, Positive Result.
            response = {
                "result": True,
                "message": "Input is an Even number.",
                "validOutputReturned": True
            }
        else:
            # Valid Input, Negative Result.
            response = {
                "result": False,
                "message": "Input is an Odd number.",
                "validOutputReturned": True
            }
    else:
        # Invalid Input, Default Negative Result and return error message and indicator.
        response = {
                "result": False,
                "message": "Invalid input. Cannot calculate.",
                "validOutputReturned": False
            }
    return response

def getFactors(n):
    # print("Entering getFactors...")
    factorsSet = set()
    response = {
            "factors": [],
            "message": "",
            "validOutputReturned": True
    }
    if is_valid_integer(n):
        if isPositive(n)['result']:
            # The number itself is always a factor
            factorsSet.add(n)
            # Input is a Valid and Positive Integer. Go ahead.
            # Special Processing for 1
            if (n == 1):
                # 1 is the only factor. Don't do anything. Exit.
                keepGoing = False
            else:
                # iteration = 1
                keepGoing = True
                # Determine the half mark
                halfMark = n // 2
                # Start processing from the half mark
                currentNumberBeingTested = halfMark
                while(keepGoing):
                    # print("Iteration # {}; Processing {}.".format(iteration,currentNumberBeingTested))
                    try:
                        if n % currentNumberBeingTested == 0:
                            # print("C")
                            # currentNumberBeingTested is a factor
                            factorsSet.add(currentNumberBeingTested)
                            # Recursive call to get the factors of currentNumberBeingTested
                            factorsSet.update(getFactors(currentNumberBeingTested)['factors'])
                            currentNumberBeingTested -= 1
                            iteration =+ 1
                        else:
                            # print("D")
                            # Decrement halfMark by 1 and come back in the while loop
                            currentNumberBeingTested -= 1
                            # iteration =+ 1
                    except ZeroDivisionError:
                        keepGoing = False
        else:
            # print("E")
            # Invalid Input, Return error message and indicator.    
            response = {
                "message": "Invalid input. Cannot get factors for a negative number.",
                "validOutputReturned": False
            }
    else:
        # Invalid Input, Return error message and indicator.
        response = {
            "message": "Invalid input. Input must be a positive integer.",
            "validOutputReturned": False
            }
    response['factors'] = sorted(factorsSet)

    return response

def isPositive(n):
    # Initialize Response Dictionary
    response = {
        "result": False,
        "message": "",
        "validOutputReturned": True
    }
    # Validate the input argument to be a valid integer
    if is_valid_integer(n):
        if n > 0:
            # Valid Input, Positive Result.
            response = {
                "result": True,
                "message": "Input is a Positive number.",
                "validOutputReturned": True
            }
        elif n == 0:
            # Valid Input, Negative Result.
            response = {
                "result": False,
                "message": "Zero is neither positive nor negative.",
                "validOutputReturned": True
            }
        else:
            # Valid Input, Negative Result.
            response = {
                "result": False,
                "message": "Input is a Negative number.",
                "validOutputReturned": True
            }
    else:
        # Invalid Input, Default Negative Result and return error message and indicator.
        response = {
                "result": False,
                "message": "Invalid input. Cannot calculate.",
                "validOutputReturned": False
            }
    return response