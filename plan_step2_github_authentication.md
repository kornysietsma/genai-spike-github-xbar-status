# Plan for Step 2: GitHub Authentication Module

## Overview
Create a robust GitHub authentication module that handles token retrieval and GitHub client initialization with proper error handling.

## Requirements from Spec
- Use GitHub API v3 with personal access token
- Token stored in environment variable (GITHUB_TOKEN)
- Provide clear error messages when authentication fails
- Support both xbar and CLI modes

## Implementation Plan

### 1. Create GitHub Authentication Module
Create a new module `github_auth.py` that provides:
- Function to validate GitHub token format
- Function to create authenticated GitHub client
- Custom exception classes for authentication errors
- Proper error messages for different failure scenarios

### 2. Update Main Script
Modify `github_status_xbar.py` to:
- Use the new authentication module
- Handle authentication errors appropriately in both modes
- Remove placeholder messages and implement actual GitHub connection

### 3. Test Coverage
Write comprehensive tests for:
- Token validation
- GitHub client creation with valid token
- Error handling for missing token
- Error handling for invalid token
- Error handling for network issues
- Mock GitHub API responses

### 4. Error Messages
Implement clear, actionable error messages:
- Missing token: Instructions on how to set GITHUB_TOKEN
- Invalid token: Instructions on creating a new token
- Network error: Suggest checking internet connection
- Permission error: List required token scopes

## Technical Details

### Module Structure
```python
# github_auth.py
class AuthenticationError(Exception): ...
class InvalidTokenError(AuthenticationError): ...
class MissingTokenError(AuthenticationError): ...

def validate_token(token: str) -> bool: ...
def create_github_client(token: str) -> Github: ...
def get_authenticated_client() -> Github: ...
```

### Token Scopes Required
The GitHub token needs these scopes:
- `repo` - Full control of private repositories
- `notifications` - Access notifications

### Testing Strategy
1. Write tests first (TDD approach)
2. Use unittest.mock for GitHub API mocking
3. Test both success and failure paths
4. Ensure 100% code coverage for authentication module

## Implementation Steps
1. Write tests for authentication module
2. Implement authentication module to pass tests
3. Update main script to use authentication
4. Update CLI error handling
5. Update xbar widget error display
6. Run all tests to ensure nothing breaks