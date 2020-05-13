import smtplib, imaplib, email, config
from email.message import EmailMessage
import utilities

# Load Environment
env = config.get_environment_from_env_file()

def send_email(emailTo, emailCC, emailSubject, emailBody):
    print("Entering send_email...")
    # Get the email attributes from Config
    email_attributes = utilities.get_value_by_entityKind_and_key(env['config_entityKind'],"email_attributes")['config_value']
    # Initialize the response dictionary
    response = {
        "result": True,
        "message": "Email sent."
    }
    message = EmailMessage()
    message['Subject'] = emailSubject
    message['To'] = emailTo
    message['CC'] = emailCC
    message.set_content(emailBody)

    # Establish connection
    try:  
        server = smtplib.SMTP(email_attributes['gmail_smtp'])
        server.ehlo()
        server.starttls()
        server.ehlo()
        print("Connection established.")
    except Exception as e: 
        errorMessage = "Exception ocurred while establishing connection with the server."
        errorMessage = "{0} Stacktrace: {1}".format(errorMessage,e)
        print(errorMessage)
        response = {
            "result": False,
            "message": errorMessage
        }
        return response

    # Connection established successfully. Log in to the email account.
    try:
        # Get password from password vault
        password = utilities.get_password_from_password_vault(email_attributes['admin_email_id'])
        server.login(email_attributes['admin_email_id'], password)
        print("Logged in.")
    except Exception as e: 
        errorMessage = "Exception ocurred while logging in."
        errorMessage = "{0} Stacktrace: {1}".format(errorMessage,e)
        print(errorMessage)
        response = {
            "result": False,
            "message": errorMessage
        }
        server.quit()
        return response

    # Logged in successfully. Send email now.
    try:  
        server.sendmail(email_attributes['admin_email_id'],emailTo,message.as_string())
        print("Email sent.")
    except Exception as e: 
        errorMessage = "Exception ocurred while sending email."
        errorMessage = "{0} Stacktrace: {1}".format(errorMessage,e)
        print(errorMessage)
        response = {
            "result": False,
            "message": errorMessage
        }
        server.quit()
        return response
    
    # All good. Close connection and return response. 
    server.quit()
    return response

def read_email():
    print("Entering read_email...")
    # Get the email attributes from Config
    email_attributes = utilities.get_value_by_entityKind_and_key(env['config_entityKind'],"email_attributes")['config_value']
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    password = utilities.get_password_from_password_vault(email_attributes['admin_email_id'])
    mail.login(email_attributes['admin_email_id'], password)
    folders = mail.list()[1]
    mail.select("Shopping")
    result, data = mail.uid('search', None, "ALL")
    item_list = data[0].split()
    for item in item_list:
        print("Value: {}, Type:{}".format(item,type(item)))

    most_recent_email = item_list[-1]
    oldest_email = item_list[0]

    print(most_recent_email)
    print(oldest_email)

    result2, email_data = mail.uid('fetch', most_recent_email, '(RFC822)')
    raw_email = email_data[0][1].decode("utf-8")
    email_message = email.message_from_string(raw_email)

    print(email_message['From'])
    print(email_message['To'])
    print(email_message['Subject'])