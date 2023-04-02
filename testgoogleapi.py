from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
# Try to load saved client credentials
gauth.LoadCredentialsFile("mycreds.txt")
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("mycreds.txt")

drive = GoogleDrive(gauth)

# Define the query to list all files
query = "'root' in parents and trashed=false"

# Get the list of all files in the root directory
file_list = drive.ListFile({'q': query}).GetList()

# Print the list of files
if not file_list:
    print('No files found.')
else:
    print('Files:')
    for file in file_list:
        print(f'{file["title"]} ({file["id"]})')