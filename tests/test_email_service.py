import pytest
from unittest.mock import MagicMock, patch

from sdk.api.exceptions import ValidationError
from sdk.domain.models import EmailVerificationResult
from sdk.services.email_service import EmailVerificationService


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    return MagicMock()


@pytest.fixture
def mock_storage():
    """Create a mock storage."""
    return MagicMock()


@pytest.fixture
def service(mock_api_client, mock_storage):
    """Create an email verification service instance."""
    return EmailVerificationService(
        api_client=mock_api_client,
        storage=mock_storage,
    )


def test_validate_email_valid(service):
    """Test email validation with valid email."""
    service._validate_email("test@example.com")
    # Should not raise any exception


def test_validate_email_invalid(service):
    """Test email validation with invalid email."""
    with pytest.raises(ValidationError):
        service._validate_email("invalid-email")


def test_verify_email_cached(service, mock_storage):
    """Test email verification with cached result."""
    email = "test@example.com"
    cached_result = EmailVerificationResult(
        email=email,
        score=0.8,
        status="valid",
        domain="example.com",
        is_disposable=False,
        is_webmail=False,
        is_deliverable=True,
    )
    mock_storage.get.return_value = cached_result

    result = service.verify_email(email)
    assert result == cached_result
    mock_storage.get.assert_called_once_with(email)
    service._api_client.verify_email.assert_not_called()


def test_verify_email_new(service, mock_api_client, mock_storage):
    """Test email verification with new email."""
    email = "test@example.com"
    api_result = {
        "email": email,
        "score": 0.8,
        "status": "valid",
        "domain": "example.com",
        "disposable": False,
        "webmail": False,
        "deliverable": True,
    }
    mock_storage.get.return_value = None
    mock_api_client.verify_email.return_value = api_result

    result = service.verify_email(email)
    assert result.email == email
    assert result.score == 0.8
    assert result.status == "valid"
    assert result.domain == "example.com"
    assert not result.is_disposable
    assert not result.is_webmail
    assert result.is_deliverable
    mock_storage.save.assert_called_once_with(email, result)


def test_get_verification_result(service, mock_storage):
    """Test retrieving verification result."""
    email = "test@example.com"
    expected_result = EmailVerificationResult(
        email=email,
        score=0.8,
        status="valid",
        domain="example.com",
        is_disposable=False,
        is_webmail=False,
        is_deliverable=True,
    )
    mock_storage.get.return_value = expected_result

    result = service.get_verification_result(email)
    assert result == expected_result
    mock_storage.get.assert_called_once_with(email) 