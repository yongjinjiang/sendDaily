# import smtplib
# from email.mime.text import MIMEText

# # Set up your email details
# sender_email = "yjjiangphysics@gmail.com"
# receiver_email = "jhuimin1950@gmail.com"
# password = "ecTjA9(00_!)))"

# # Create the email content
# subject = "Daily Email"
# body = "This is your daily email!"

# msg = MIMEText(body)
# msg["Subject"] = subject
# msg["From"] = sender_email
# msg["To"] = receiver_email

# # Send the email
# try:
#     with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
#         server.login(sender_email, password)
#         server.sendmail(sender_email, receiver_email, msg.as_string())
#     print("Email sent successfully")
# except Exception as e:
#     print(f"Failed to send email: {e}")

import os.path
import base64

from google.auth.transport.requests import Request

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os.path
