# forage
 
# Summary
 Python SDK client for the Hunter.io API with in-memory storage capabilities.

## Features

- Email verification using Hunter.io API
- In-memory storage with CRUD operations
- Type-safe implementation with mypy support
- Async support for better performance
- Rate limiting and retry mechanisms
- TTL-based caching
- Comprehensive error handling

## Installation

1. Clone the repository:
   git clone <repository-url>
 

2. Create a virtual environment:
   ```bash
   # On Windows:
   python -m venv venv
   venv\Scripts\activate

   # On Linux/MacOS:
   python3 -m venv venv
   source venv/bin/activate
 

3. Install dependencies:

   pip install -r requirements.txt


4. Create a `.env` file with your Hunter.io API key:


# Verify email
result = service.verify_email("example@domain.com")
print(f"Email verification result: {result}")
```

### Advanced Usage with Configuration

```python
from sdk import Config, EmailVerificationService, HunterAPIClient, TTLStorage

### Running the Example

1. Make sure your virtual environment is activated
2. Set your Hunter.io API key in the `.env` file
3. Run the example:

   python main.py
 
## Development

### Running Tests

# Run tests with coverage report
python -m pytest tests/ --cov=sdk -v

# Run tests without coverage
python -m pytest tests/ -v


### Code Quality Checks

```bash
# Run type checking
mypy sdk/

# Run linting
flake8 sdk/

# Format code
black sdk/
isort sdk/


## Configuration

You can customize the SDK behavior through configuration:

```python
from sdk import Config

config = Config(
    api=APIConfig(
        timeout=60.0,
        max_retries=5,
    ),
    rate_limit=RateLimitConfig(
        max_requests=200,
        time_window=60,
    ),
    storage=StorageConfig(
        ttl=7200,  # 2 hours
    ),
)

