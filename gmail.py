import smtplib, imaplib, email
from email.message import EmailMessage
from config import read_configurations_from_config_file
# from login import decrypt_password
import utilities

# Load Defaults from Config
envVariables = read_configurations_from_config_file()
admin_email_id = envVariables['admin_email_id']
USERNAME = admin_email_id
gmail_smtp = envVariables['gmail_smtp']

def send_email(emailTo, emailCC, emailSubject, emailBody):
    print("Entering send_email...")
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
        server = smtplib.SMTP(gmail_smtp)
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
        PASSWORD = utilities.get_password_from_password_vault(admin_email_id)
        server.login(USERNAME, PASSWORD)
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
        server.sendmail(USERNAME,emailTo,message.as_string())
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
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    PASSWORD = utilities.get_password_from_password_vault(admin_email_id)
    mail.login(USERNAME, PASSWORD)
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