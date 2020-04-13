def login(login_credentials):
    print("Entering login..")

    # Declare the output dictionary
    login_output = declare_output_dictionary(login_credentials)

    login_output['message'] = "User Logged In"

    return login_output

def declare_output_dictionary(login_credentials):
    login_output = {}
    
    login_output['login_credentials'] = login_credentials
    login_output['message'] = ""
    login_output['validOutputReturned'] = True

    return login_output

