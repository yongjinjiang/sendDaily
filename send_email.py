from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os.path
from dotenv import load_dotenv
import os

# Check if running in GitHub Actions
if not os.getenv("GITHUB_ACTIONS"):
    # Load environment variables from .env file if not running in GitHub Actions
    print("Running locally. Loading environment variables from .env file.")
    load_dotenv()
else:
    print("Running in GitHub Actions. Skipping .env loading.")


def authenticate_gmail():
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def create_message(sender, to, subject, message_text):
    from email.mime.text import MIMEText
    import base64
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()
    return {'raw': raw}

def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except Exception as error:
        print('An error occurred: %s' % error)

if __name__ == '__main__':
    # Authenticate and create the Gmail API service
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)

    # Read email addresses from environment variables
    sender_email = os.getenv("SENDER_EMAIL")
    recipient_email = os.getenv("RECIPIENT_EMAIL")

    # Check if the environment variables are set
    if not sender_email or not recipient_email:
        raise ValueError("SENDER_EMAIL or RECIPIENT_EMAIL is not set in the environment.")



    # Create the email content
    subject = "Daily Email"
    body = "This is your daily email!"

    # Create and send the email
    message = create_message(sender_email, recipient_email, subject, body)
    send_message(service, 'me', message)