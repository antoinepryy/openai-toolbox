import openai
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# Load environment variables
API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = os.getenv("ASSISTANT_ID", "asst_8EmgqyYscdsMm1zZVAUnXiSu")
VECTOR_STORE_ID = os.getenv("VECTOR_STORE_ID", "vs_abc123")

if not API_KEY:
    raise ValueError("API Key not found. Please ensure OPENAI_API_KEY is set in the .env file.")

# Initialize OpenAI client
openai.api_key = API_KEY
client = openai.Client()

def upload_file():
    filename = input("Enter the filename to upload: ")
    try:
        with open(filename, "rb") as file:
            response = client.files.create(file=file, purpose="assistants")
            print(response)
            print(f"File uploaded successfully: {response.filename} [{response.id}]")
    except FileNotFoundError:
        print("File not found. Please make sure the filename and path are correct.")

def list_files():
    response = client.files.list(purpose="assistants")
    if len(response.data) == 0:
        print("No files found.")
        return
    for file in response.data:
        created_date = datetime.datetime.utcfromtimestamp(file.created_at).strftime('%Y-%m-%d')
        print(f"{file.filename} [{file.id}], Created: {created_date}")

def list_and_delete_file():
    while True:
        response = client.files.list(purpose="assistants")
        files = list(response.data)
        if len(files) == 0:
            print("No files found.")
            return
        for i, file in enumerate(files, start=1):
            created_date = datetime.datetime.utcfromtimestamp(file.created_at).strftime('%Y-%m-%d')
            print(f"[{i}] {file.filename} [{file.id}], Created: {created_date}")
        choice = input("Enter a file number to delete, or any other input to return to menu: ")
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(files):
            return
        selected_file = files[int(choice) - 1]
        client.files.delete(selected_file.id)
        print(f"File deleted: {selected_file.filename}")

def delete_all_files():
    confirmation = input("This will delete all OpenAI files with purpose 'assistants'.\n Type 'YES' to confirm: ")
    if confirmation == "YES":
        response = client.files.list(purpose="assistants")
        for file in response.data:
            client.files.delete(file.id)
        print("All files with purpose 'assistants' have been deleted.")
    else:
        print("Operation cancelled.")

# New function to list vector store files
def list_vector_store():
    try:
        # List all available vector stores
        vector_stores = client.beta.vector_stores.list()
        if len(vector_stores.data) == 0:
            print("No vector stores available.")
            return

        # Display all vector store IDs to the user with enumeration
        print("Available vector stores:")
        for i, vs in enumerate(vector_stores.data, start=1):
            created_date = datetime.datetime.fromtimestamp(vs.created_at, tz=datetime.UTC).strftime('%Y-%m-%d')
            print(f"[{i}] Vector Store: {vs.id}, Name: {vs.name or 'None'}, Created: {created_date}")

    except Exception as e:
        print(f"Error listing vector store files: {e}")


def delete_all_vector_store():
    try:
        # List all available vector stores
        vector_stores = client.beta.vector_stores.list()

        if not vector_stores.data:
            print("No vector stores available.")
            return

        # Display all vector store IDs to the user with enumeration
        print("Available vector stores:")
        for i, vs in enumerate(vector_stores.data, start=1):
            created_date = datetime.datetime.fromtimestamp(vs.created_at, tz=datetime.timezone.utc).strftime('%Y-%m-%d')
            print(f"[{i}] Vector Store: {vs.id}, Name: {vs.name or 'None'}, Created: {created_date}")

        # Confirm deletion of all vector stores
        confirmation = input("Are you sure you want to delete all files in all vector stores? Type 'YES' to confirm: ")
        if confirmation != "YES":
            print("Operation cancelled.")
            return

        # Iterate over all vector stores and delete them
        for vs in vector_stores.data:
            vector_store_id = vs.id
            print(f"Processing vector store: {vs.id} - {vs.name or 'None'}")

            client.beta.vector_stores.delete(vector_store_id=vector_store_id)
            print(f"Vector store '{vs.name or 'None'}' has been deleted.")

        print("All vector stores have been deleted successfully.")

    except Exception as e:
        print(f"Error deleting vector store files: {e}")

def main():
    while True:
        print("\n== Assistants and Vector Store File Utility ==")
        print("[1] Upload file")
        print("[2] List all files")
        print("[3] List all and delete one of your choice")
        print("[4] Delete all assistant files (confirmation required)")
        print("[5] List vector store files")
        print("[6] Delete a vector store file")
        print("[9] Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            upload_file()
        elif choice == "2":
            list_files()
        elif choice == "3":
            list_and_delete_file()
        elif choice == "4":
            delete_all_files()
        elif choice == "5":
            list_vector_store()
        elif choice == "6":
            delete_all_vector_store()
        elif choice == "9":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
