from google.auth import exceptions
from google.oauth2 import service_account
import google.auth.transport.requests

CREDENTIALS_PATH = "listin-438620-86c639f67114.json"
SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]

def test_service_account_credentials():
    try:
        creds = service_account.Credentials.from_service_account_file(
            CREDENTIALS_PATH, scopes=SCOPES
        )
        request = google.auth.transport.requests.Request()
        creds.refresh(request)
        print("✅ Credentials are valid and active.")
        print(f"Service account email: {creds.service_account_email}")
        print(f"Project ID: {creds.project_id}")
    except FileNotFoundError:
        print(f"❌ Credential file not found: {CREDENTIALS_PATH}")
    except exceptions.RefreshError as e:
        print(f"❌ Credentials are invalid or lack required API access.\nDetails: {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    test_service_account_credentials()
