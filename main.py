import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/admin.directory.user']

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    users = listAccounts()
    return render_template('index.html', users=users)

def listAccounts():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('admin', 'directory_v1', credentials=creds)

    # Call the Admin SDK Directory API
    results = service.users().list(customer='my_customer', maxResults=100,
                                   orderBy='email').execute()
    users = results.get('users', [])

    if not users:
        output = 'No users in the domain.'
    else:
        output = []
        for user in users:
            line = []
            line.append(user['name']['fullName'])
            line.append(user['primaryEmail'])
            output.append(line)

    return output


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
