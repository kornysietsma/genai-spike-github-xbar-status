#!/usr/bin/env python3
"""Tests for GitHub authentication module."""

import os
from unittest.mock import patch, Mock
import pytest
from github import Github, BadCredentialsException

# Import the module to be tested
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from github_auth import (
    InvalidTokenError,
    MissingTokenError,
    NetworkError,
    create_github_client,
    get_authenticated_client,
)


class TestCreateGithubClient:
    def test_create_client_with_valid_token(self):
        token = "test_token_123"
        client = create_github_client(token)
        assert isinstance(client, Github)
    
    @patch('github_auth.Github')
    def test_create_client_handles_network_error(self, mock_github):
        mock_github.side_effect = Exception("Network error")
        with pytest.raises(NetworkError) as exc_info:
            create_github_client("test_token")
        assert "Failed to create GitHub client" in str(exc_info.value)


class TestGetAuthenticatedClient:
    @patch.dict(os.environ, {"GITHUB_TOKEN": "test_token_123"})
    @patch('github_auth.create_github_client')
    def test_get_client_with_env_token(self, mock_create):
        mock_client = Mock()
        mock_user = Mock()
        mock_user.login = "testuser"
        mock_client.get_user.return_value = mock_user
        mock_create.return_value = mock_client
        
        client = get_authenticated_client()
        assert client == mock_client
        mock_create.assert_called_once_with("test_token_123")
    
    @patch.dict(os.environ, {}, clear=True)
    def test_get_client_without_token(self):
        # Ensure GITHUB_TOKEN is not set
        if "GITHUB_TOKEN" in os.environ:
            del os.environ["GITHUB_TOKEN"]
        
        with pytest.raises(MissingTokenError) as exc_info:
            get_authenticated_client()
        assert "GITHUB_TOKEN environment variable not set" in str(exc_info.value)
    
    @patch.dict(os.environ, {"GITHUB_TOKEN": "invalid"})
    def test_get_client_with_invalid_token(self):
        with pytest.raises(InvalidTokenError):
            get_authenticated_client()
    
    @patch.dict(os.environ, {"GITHUB_TOKEN": "test_token_123"})
    @patch('github_auth.create_github_client')
    def test_get_client_verifies_authentication(self, mock_create):
        mock_client = Mock()
        mock_user = Mock()
        mock_user.login = "testuser"
        mock_client.get_user.return_value = mock_user
        mock_create.return_value = mock_client
        
        client = get_authenticated_client()
        assert client == mock_client
        mock_client.get_user.assert_called_once()
    
    @patch.dict(os.environ, {"GITHUB_TOKEN": "test_token_123"})
    @patch('github_auth.create_github_client')
    def test_get_client_handles_bad_credentials(self, mock_create):
        mock_client = Mock()
        mock_client.get_user.side_effect = BadCredentialsException(401, {"message": "Bad credentials"}, {})
        mock_create.return_value = mock_client
        
        with pytest.raises(InvalidTokenError) as exc_info:
            get_authenticated_client()
        assert "Invalid GitHub token" in str(exc_info.value)
        assert "permission" in str(exc_info.value).lower()
    
    @patch.dict(os.environ, {"GITHUB_TOKEN": "test_token_123"})
    @patch('github_auth.create_github_client')
    def test_get_client_handles_network_error(self, mock_create):
        mock_client = Mock()
        mock_client.get_user.side_effect = Exception("Connection refused")
        mock_create.return_value = mock_client
        
        with pytest.raises(NetworkError) as exc_info:
            get_authenticated_client()
        assert "Network error" in str(exc_info.value)