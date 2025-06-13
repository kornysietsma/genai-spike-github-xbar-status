#!/usr/bin/env python3
"""GitHub authentication module for the activity monitor."""

import os
from github import Github, BadCredentialsException


class AuthenticationError(Exception):
    """Base exception for authentication errors."""
    pass


class InvalidTokenError(AuthenticationError):
    """Raised when the GitHub token is invalid or has incorrect format."""
    pass


class MissingTokenError(AuthenticationError):
    """Raised when the GitHub token is not found."""
    pass


class NetworkError(AuthenticationError):
    """Raised when network-related errors occur."""
    pass




def create_github_client(token: str) -> Github:
    """Create an authenticated GitHub client.
    
    Args:
        token: GitHub personal access token
        
    Returns:
        Authenticated Github client instance
        
    Raises:
        NetworkError: If client creation fails
    """
    try:
        return Github(token)
    except Exception as e:
        raise NetworkError(f"Failed to create GitHub client: {str(e)}")


def get_authenticated_client() -> Github:
    """Get an authenticated GitHub client using environment token.
    
    Returns:
        Authenticated and verified Github client instance
        
    Raises:
        MissingTokenError: If GITHUB_TOKEN env var is not set
        InvalidTokenError: If token is invalid or lacks permissions
        NetworkError: If network connection fails
    """
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise MissingTokenError(
            "GITHUB_TOKEN environment variable not set. "
            "Please set it with a GitHub personal access token. "
            "Create one at: https://github.com/settings/tokens"
        )
    
    client = create_github_client(token)
    
    # Verify the token works by making a simple API call
    try:
        user = client.get_user()
        # Force the API call by accessing a property
        _ = user.login
    except BadCredentialsException:
        raise InvalidTokenError(
            "Invalid GitHub token. Please check that your token is valid "
            "and has the required permissions (repo, notifications). "
            "Create a new token at: https://github.com/settings/tokens"
        )
    except Exception as e:
        raise NetworkError(
            f"Network error while verifying GitHub credentials: {str(e)}. "
            "Please check your internet connection."
        )
    
    return client