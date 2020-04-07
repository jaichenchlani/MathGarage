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
