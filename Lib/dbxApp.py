# Demo program to sync a local file with dropbox through dropbox API
# Program can back up local files and view files on local and dropbox.

# Research references:
# https://www.geeksforgeeks.org/how-to-automate-the-storage-using-dropbox-api-in-python/
# https://github.com/dropbox/dropbox-sdk-python/blob/master/example/updown.py
# https://medium.com/codex/chunked-uploads-with-binary-files-in-python-f0c48e373a91
# https://riptutorial.com/dropbox-api/example/1927/uploading-a-file-using-the-dropbox-python-sdk
# https://stackoverflow.com/questions/33825908/dropbox-api-v2-uploading-files
# https://www.dropbox.com/developers/documentation/http/documentation
# https://practicaldatascience.co.uk/data-science/how-to-use-the-dropbox-api-with-python
# https://dropbox-sdk-python.readthedocs.io/en/latest/api/file_requests.html
# https://www.dropbox.com/developers/documentation/python#tutorial
# https://docs.python.org/3/library/argparse.html

# First time working with the API, had major issues trying to find a way to format the local
# files in a way that dropbox API would accept. A lot of online tutorials use deprecated
# methods from Dropbox API v1.0.
# Finally found that argeparse was the answer for me, had to research the module and had a lot
# of trial and error before getting a basic working API 2.0 query setup.
# Wanted to implement a lot more functionality and a more sophisticated syncing method that
# could check files for date edited to find the newest version before updating but ran out
# of time.

# Importing modules
from __future__ import print_function
import argparse
import os
import dropbox
import sys


# Function to run menu options and return user choice.
def menu():

    print("Options:\n1) Backup Local Files\n2) View Local Files\n3) View Dropbox Files\n4) Exit")

    while True:
        menu_choice = str(input("Select option by entering corresponding number: "))

        # Checking if valid integer.
        try:
            menu_choice = int(menu_choice)

        except ValueError:
            print("You have not entered a valid menu option.")
            continue

        # Checking if valid option.
        if menu_choice == 1 or menu_choice == 2 or menu_choice == 3 or menu_choice == 4:
            break

        else:
            print("You have not entered a valid menu option.")

    return menu_choice


# Helper function to ask yes/no questions.
def yes_no():

    result = True  # Return result as bool value.

    while True:
        choice = (input("(Y/n)? ")).lower()

        if choice == "y":
            result = True
            break

        elif choice == "n":
            result = False
            break

        else:
            print("You did not enter a valid response, please try again.")

    return result


# Function to establish a connection with dropbox token.
def dropbox_connect(TOKEN):

    try:
        connection = dropbox.Dropbox(TOKEN)
        print("Dropbox connection successful.")

    except Exception:
        print("Error while trying to connect to Dropbox account.")

    return connection


# Function that reads files in local folder.
def read_local_files(root_dir):

    local_files = []

    try:
        for root, dirs, files in os.walk(root_dir):
            for name in files:
                local_files.append(name)

    except Exception as e:
        print("Error reading local directory.\n" + str(e))

    return local_files


# Function that reads dropbox files and returns a list of metadata dictionaries.
def read_dropbox(connection, folder):

    # Connecting to dropbox and listing files.
    try:
        files = connection.files_list_folder(folder).entries

        dropbox_files = []

        # Iterating over each file and creating object instance with metadata as
        # properties in dictionary format stored in list.
        for file in files:
            if isinstance(file, dropbox.files.FileMetadata):
                metadata = {
                    "name": file.name,
                    "path_display": file.path_display,
                    "client_modified": file.client_modified,
                    "server_modified": file.server_modified
                }
                dropbox_files.append(metadata)

    except Exception as e:
        print("Error getting list of files from Dropbox:\n" + str(e))

    return dropbox_files


# Function that backs up local files to dropbox.
# If file names are identical user will be prompted to proceed with overwrite or not.
def local_backup(connection, name, folder, sub_folder, file):

    # Adjusting characters in string format.
    path = "/{}/{}/{}".format(folder, sub_folder.replace(os.path.sep, "/"), file)
    while "//" in path:
        path = path.replace("//", "/")

    # Assigning backup mode as overwrite.
    mode = dropbox.files.WriteMode.overwrite

    # Reading file data.
    with open(name, "rb") as f:
        data = f.read()

    result = None

    # Creating upload query.
    try:
        result = connection.files_upload(data, path, mode)

    except Exception as e:
        print("Error moving files to cloud.\n" + str(e))

    return result


# Auto generated token from dropbox.
# Need to research, understand and implement 0Auth.
TOKEN = """sl.BMDHK-SWVSqg8g9DC0PHQebTiYHc0-p36b-hpENYMwNOwI_kIHvyndA6gV44mBmkbOhAUUrfhzPcFKMbBXD3LHsJxWptyrEtiGHaGiIlAHCOj40kxMXUxBoqsYv7NyJketWwm5-RxtA"""

# NOTE: Adjust the local directory path for new user.
parser = argparse.ArgumentParser(description="Sync ~\\IdeaProjects\\MyDropboxFolder to Dropbox")
parser.add_argument("folder", nargs="?", default="")
parser.add_argument("root_dir", nargs="?", default="~\\IdeaProjects\\MyDropboxFolder", help="Local directory to upload")


def main():

    # Running function to establish connection with Dropbox API.
    connection = dropbox_connect(TOKEN)

    # Initialising argument parser for dropbox API queries.
    args = parser.parse_args()
    folder = args.folder  # Initializing dropbox location.
    root_dir = os.path.expanduser(args.root_dir)  # Initializing local directory.

    # Checking if local directory exists, if not program will exit.
    if not os.path.exists(root_dir):
        print(root_dir, "does not exist on your computer.")
        sys.exit()

    # loop to allow user multiple menu options
    while True:

        # Running menu function.
        menu_choice = menu()

        # Option 1: Backup local files.
        if menu_choice == 1:

            print("Dropbox upload in progress.")

            # Reading files in Dropbox.
            dropbox_files = read_dropbox(connection, folder)

            # Walking through files on local directory.
            for root, dirs, files in os.walk(root_dir):

                # Checking for sub folders in root directory.
                sub_folder = root[len(root_dir):].strip(os.path.sep)

                # Iterating through files and generating correct path as name.
                for file in files:
                    name = os.path.join(root, file)

                    # Checking dropbox files for duplicates.
                    for i in dropbox_files:
                        query = i.get("name")  # Getting object file name.

                        # If duplicate exits overwrite permission is requested.
                        if file in query:
                            print("File name: {} already in use, do you wish to overwrite? ".format(query), end="")
                            choice = yes_no()

                            if choice is True:

                                # Upload function is called.
                                try:
                                    print("Uploading {}".format(file))
                                    local_backup(connection, name, folder, sub_folder, file)

                                except Exception as e:
                                    print("Error uploading file to dropbox." + str(e))

                        # Unique files are uploaded without prompt.
                        else:
                            print("Uploading {}".format(file))
                            local_backup(connection, name, folder, sub_folder, file)

            print("Finished upload.")

        # Option 2: View local files.
        if menu_choice == 2:
            local_files = read_local_files(root_dir)

            for file in local_files:
                print(file)

        # Option 3: View dropbox files.
        if menu_choice == 3:
            dropbox_files = read_dropbox(connection, folder)

            for file in dropbox_files:
                print(file.get("name"))

        # Option 4: Exit program.
        if menu_choice == 4:
            sys.exit()

# Running main function.
if __name__ == "__main__":
    main()
