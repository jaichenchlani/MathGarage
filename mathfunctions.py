import math

def changeBase(n, base):
    # print("Entering getBinary...")
    baseReference = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    response = {
        "result": 0,
        "message": "",
        "validOutputReturned": True
    }

    if not isInteger(n):
        # Invalid Input, Return error message and indicator.
        response = {
            "message": "Invalid input. Input number must be a positive integer.",
            "validOutputReturned": False
            }
    elif not isInteger(base):
        response = {
            "message": "Invalid input. Input base must be a positive integer between 2 and 36.",
            "validOutputReturned": False
            }
    elif base < 2 or base > 36:
        response = {
            "message": "Invalid input. Input base must be a positive integer between 2 and 36.",
            "validOutputReturned": False
            }
    elif n == 0 or n == 1:
        response['result'] = n
    elif not isPositive(n)['result']:
        # Invalid Input, Return error message and indicator.    
            response = {
                "message": "Invalid input. Cannot process a negative number.",
                "validOutputReturned": False
            }
    else:
        answer = ""
        counter = 1
        keepgoing = True
        originalNumber = n

        while (keepgoing):
            index = n % base
            # answer += str(n % base)
            answer += baseReference[index]
            # print("KeepGoing:{}; Counter:{}; N:{}; Answer:{}".format(keepgoing,counter,n,answer))
            n = n//base
            if (n < base):
                keepgoing = False
                answer += str(n)
                # print("KeepGoing:{}; Counter:{}; N:{}; Answer:{}".format(keepgoing,counter,n,answer))
            counter = counter + 1
        
        # Reverse the answer string and store in response dictionary
        # Remove the trailing zero, if any
        if answer[-1] == "0":
            response['result'] = answer[-2::-1]
        else:
            response['result'] = answer[::-1]        
    
    return response


def isPrime(n):
    # print("Entering isPrime...")
    # Initialize Response Dictionary
    response = {
        "result": False,
        "message": "",
        "validOutputReturned": True
    }
    # Call the factors function to get factors
    factors = getFactors(n)
    # Populate the isPrime Response dictionary using the values returned from getFactors
    response = {
        "result": factors['isPrime'],
        "message": factors['message'],
        "validOutputReturned": factors['validOutputReturned']
        }
    # Update the message with additional information for Composite i.e. non-Prime numbers
    if not factors['isPrime']:
        response['message'] = "Divisible by {}".format(str(factors['factors'][1:-1]))
    
    return response

def isEven(n):
    # print("Entering isEven...")
    # Initialize Response Dictionary
    response = {
        "result": False,
        "message": "",
        "validOutputReturned": True
    }
    # Validate the input argument to be a valid integer
    if isInteger(n):
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
            "factorsCount": 1,
            "isPrime": False,
            "factors": [],
            "message": "",
            "validOutputReturned": True
    }
    if not isInteger(n):
        # Invalid Input, Return error message and indicator.
        response['message'] = "Invalid input. Input must be a positive integer."
        response['validOutputReturned'] = False
        return response
    
    if n == 0:
        # Invalid Input, Return error message and indicator.
        response['message'] = "Invalid input. Zero has infinite factors. Cannot populate factors list."
        response['validOutputReturned'] = False
        return response

    if not isPositive(n)['result']:
        # Invalid Input, Return error message and indicator.    
        response['message'] = "Invalid input. Cannot process a negative number."
        response['validOutputReturned'] = False
        return response
    
    # All good. Go ahead with processing.
    if n == 1:
        # Special Processing for 1
        factorsSet.add(n)
    else:
        # The number itself is always a factor
        factorsSet.add(n)
        # Input is a Valid and Positive Integer. Go ahead.
        # Special Processing for 1
        keepGoing = True
        # Determine the half mark
        halfMark = n // 2
        # Start processing from the half mark
        currentNumberBeingTested = halfMark
        while(keepGoing):
            # print("Iteration # {}; Processing {}.".format(iteration,currentNumberBeingTested))
            try:
                if n % currentNumberBeingTested == 0:
                    # currentNumberBeingTested is a factor
                    factorsSet.add(currentNumberBeingTested)
                    # Recursive call to get the factors of currentNumberBeingTested
                    factorsSet.update(getFactors(currentNumberBeingTested)['factors'])
                    currentNumberBeingTested -= 1
                    iteration =+ 1
                else:
                    # Decrement halfMark by 1 and come back in the while loop
                    currentNumberBeingTested -= 1
                    # iteration =+ 1
            except ZeroDivisionError:
                keepGoing = False

    # Sort the factors Set in Ascending order, and store in the list in Response. 
    response['factors'] = sorted(factorsSet)
    response['factorsCount'] = len(response['factors'])
    # Determine whether the number is Prime, based on # of factors
    if response['factorsCount'] <= 2:
        response['isPrime'] = True
    else:
        response['isPrime'] = False

    return response

def isPositive(n):
    # print("Entering isPositive...")
    # Initialize Response Dictionary
    response = {
        "result": False,
        "message": "",
        "validOutputReturned": True
    }
    # Validate the input argument to be a valid integer
    if isInteger(n):
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

# Validate whether the passed string is a valid integer, and return a boolean result
def isInteger(str_number):
    # print("Entering isInteger...")
    try:
        temp_int_variable = int(str_number)
    except ValueError:
        return False

    return True

def getPrimeFactors(n):
    # print("Entering getPrimeFactors...")
    # Initialize Response Dictionary
    primeFactors = []
    response = {
        "factorsCount": 1,
        "primeFactors": [],
        "isPrime": False,
        "message": "",
        "validOutputReturned": True
    }
    # Call the factors function to get factors
    factors = getFactors(n)
    
    if not factors['validOutputReturned']:
        # Not a valid response from getFactors
        response = {
            "primeFactors": [],
            "message": factors['message'],
            "validOutputReturned": False
        }
    elif n == 0:
        # Special handling for 0
        primeFactors = factors['factors']
        response = {
            "message": factors['message'],
            "validOutputReturned": True
        }
    elif n == 1:
        # Special handling for 1
        primeFactors = factors['factors']
        response = {
            "message": factors['message'],
            "validOutputReturned": True
        }
    elif factors['isPrime']:
        # If the number is Prime, then the only Prime Factor is the number itself.
        primeFactors.append(n)
        response = {
            "primeFactors": primeFactors,
            "message": "",
            "validOutputReturned": True
        }
    else:
        # Loop through the factors list to get the highest Prime Factor
        keepGoing = True
        # Declare an iterationFactors variable to hold the currently processing factors list
        # This will get updated in every iteration by deviding the original number (n) by the last found prime factor
        iterationFactors = factors
        # Start with the original number
        iterationNumber = n
        # Keep track of number of iterations.
        iteration = 1
        # The while loop continues until you hit a Prime iterationNumber
        while(keepGoing):
            # print("Iteration # {}; Processing {}.".format(iteration,iterationNumber))
            highestPrimeFactor = 0
            # Iterate through the factors list except for first(1) and last(the number itself)
            for factor in iterationFactors['factors'][1:-1]:
                # print("factor:{}".format(factor))
                if isPrime(factor)['result']:
                    highestPrimeFactor = factor
            # Append the highest prime factor in the response list
            # print("highestPrimeFactor:{}".format(highestPrimeFactor))
            primeFactors.append(highestPrimeFactor)
            # Update the iteration variables
            iterationNumber = int(iterationNumber / highestPrimeFactor)
            iterationFactors = getFactors(iterationNumber)
            # print("iterationNumber:{}".format(iterationNumber))
            # print("iterationFactors:{}".format(iterationFactors))
            if not iterationFactors['validOutputReturned']:
                # Not a valid response from getFactors
                response = {
                    "primeFactors": [],
                    "message": iterationFactors['message'],
                    "validOutputReturned": False
                }
            elif iterationFactors['isPrime']:
                # Prime iterationNumber. Processing completed. End the while loop.
                primeFactors.append(iterationNumber)
                keepGoing = False
            else:
                # iterationNumber is NOT Prime. Repeat the while loop.
                iteration += 1
    # Update the primeFactors list in ascending order in the Response dictionary
    primeFactors.sort()
    response['primeFactors'] = primeFactors
    response['factorsCount'] = len(response['primeFactors'])
    # Determine whether the number is Prime, based on # of factors
    if response['factorsCount'] == 1:
        response['isPrime'] = True
    else:
        response['isPrime'] = False

    return response