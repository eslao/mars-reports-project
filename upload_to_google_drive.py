# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

#!/usr/bin/python

import os
import httplib2
import pprint

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow

from os import listdir, getcwd
from os.path import isfile, join

# <codecell>

# Copy your credentials from the console
CLIENT_ID = '528918718964-mao4dfhi6o9ipdp8c0uq5i01skck1dti.apps.googleusercontent.com'
CLIENT_SECRET = 'O3WMYTMIEbSGZHjoRKUOZ3qj'

# Check https://developers.google.com/drive/scopes for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

# Redirect URI for installed apps
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

# Path to the file to upload
#FILENAME = 'document.txt'

# <codecell>

# Run through the OAuth flow and retrieve credentials
flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, REDIRECT_URI)
authorize_url = flow.step1_get_authorize_url()
print 'Go to the following link in your browser: ' + authorize_url
code = raw_input('Enter verification code: ').strip()
credentials = flow.step2_exchange(code)

# <codecell>

# Create an httplib2.Http object and authorize it with our credentials
http = httplib2.Http()
http = credentials.authorize(http)

drive_service = build('drive', 'v2', http=http)

# build list of files in directory
files_to_upload = [ f for f in listdir(os.getcwd()) if isfile(join(os.getcwd(),f)) ]

# dictionary of files uploaded
file_dict = {}

#upload each file in list
for FILENAME in files_to_upload:
    # Insert a file
    media_body = MediaFileUpload(FILENAME, mimetype='text/plain', resumable=True)
    filename_sans_extension = os.path.splitext(FILENAME)[0]
    body = {
      'title': filename_sans_extension,
      'description': filename_sans_extension,
      #'mimeType': 'text/plain'
    }
    file = drive_service.files().insert(body=body, media_body=media_body).execute()
    # pprint.pprint(file)
    file_id = file['id']
    # print file_id
    url = file['alternateLink']
    name = filename_sans_extension
    file_dict[filename_sans_extension] = url
    
wiki_table = ['||column 1||column 2||']
for report_file in file_dict:
    #print '|' + report_file + '|' + file_dict[report_file] + '|'
    wiki_table += ['|' + report_file + '|' + file_dict[report_file] + '|']
for table_row in wiki_table:
    print table_row
    

# <codecell>


