import os
from dotenv import load_dotenv
from sdk.api.exceptions import APIKeyError, HunterAPIError, ValidationError
from sdk.storage.memory_storage import MemoryStorage
from sdk.services.email_service import EmailVerificationService
from sdk.api.hunter_client import HunterAPIClient


def main() -> None:
    """Run the example."""
    # Load environment variables from .env file
    load_dotenv()

    # get api key from env
    api_key = os.environ.get("HUNTER_API_KEY", "")
    if not api_key:
        raise APIKeyError("Please set the HUNTER_API_KEY environment variable")
    
    # initiate api client and data storage
    api_client = HunterAPIClient(api_key=api_key)
    storage = MemoryStorage()

    # set up service
    email_service = EmailVerificationService(api_client=api_client, storage=storage)

    # test email address
    email = "example@example.com"
    try:
        result = email_service.verify_email(email)
        print("\nEmail Validation Results:")
        print("-" * 50)
        print(f"Email: {result.email}")
        print(f"Domain: {result.domain}")
        print(f"Status: {result.status}")
        print(f"Score: {result.score}")
        print(f"Disposable: {'Yes' if result.is_disposable else 'No'}")
        print(f"Webmail: {'Yes' if result.is_webmail else 'No'}")
        print(f"Deliverable: {'Yes' if result.is_deliverable else 'No' if result.is_deliverable is False else 'Unknown'}")
        print("-" * 50)
    
    except ValidationError as ex:
        print(f"Validation error: {ex}")
    except HunterAPIError as ex:
        print(f"API error: {ex}")
        if ex.status_code:
            print(f"Status code: {ex.status_code}")
    except Exception as ex:
        print(f"Unexpected error: {ex}")


if __name__ == "__main__":
    main()