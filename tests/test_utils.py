#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pytest>=7.0.0",
#     "PyGithub>=2.1.0",
#     "swiftbarmenu>=0.1.0",
#     "click>=8.1.0",
# ]
# ///

import os
import sys
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import pytest

# Add parent directory to path to import the main script
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from github_status_xbar import (
    format_time_ago,
    truncate_text,
    get_github_token,
    is_xbar_environment,
    GITHUB_TOKEN_ENV,
)


class TestFormatTimeAgo:
    
    def test_now(self):
        now = datetime.now(timezone.utc)
        assert format_time_ago(now) == "now"
    
    def test_minutes_only(self):
        now = datetime.now(timezone.utc)
        past = now - timedelta(minutes=30)
        assert format_time_ago(past) == "30m"
        
        past = now - timedelta(minutes=1)
        assert format_time_ago(past) == "1m"
    
    def test_hours_and_minutes(self):
        now = datetime.now(timezone.utc)
        past = now - timedelta(hours=1, minutes=30)
        assert format_time_ago(past) == "1h30m"
        
        past = now - timedelta(hours=5, minutes=45)
        assert format_time_ago(past) == "5h45m"
    
    def test_hours_only(self):
        now = datetime.now(timezone.utc)
        past = now - timedelta(hours=2)
        assert format_time_ago(past) == "2h"
    
    def test_days_and_hours(self):
        now = datetime.now(timezone.utc)
        past = now - timedelta(days=1, hours=5)
        assert format_time_ago(past) == "1d5h"
        
        past = now - timedelta(days=3, hours=12)
        assert format_time_ago(past) == "3d12h"
    
    def test_days_only(self):
        now = datetime.now(timezone.utc)
        past = now - timedelta(days=2)
        assert format_time_ago(past) == "2d"
    
    def test_future_timestamp(self):
        now = datetime.now(timezone.utc)
        future = now + timedelta(hours=1)
        assert format_time_ago(future) == "future"


class TestTruncateText:
    
    def test_short_text(self):
        text = "Short text"
        assert truncate_text(text) == text
        assert truncate_text(text, max_length=20) == text
    
    def test_exact_length(self):
        text = "A" * 50
        assert truncate_text(text) == text
        assert truncate_text(text, max_length=50) == text
    
    def test_long_text(self):
        text = "This is a very long text that should be truncated with ellipsis"
        result = truncate_text(text, max_length=20)
        assert result == "This is a very lo..."
        assert len(result) == 20
    
    def test_custom_length(self):
        text = "This is a test string for truncation"
        result = truncate_text(text, max_length=10)
        assert result == "This is..."
        assert len(result) == 10


class TestEnvironmentDetection:
    
    def test_get_github_token_present(self):
        with patch.dict(os.environ, {GITHUB_TOKEN_ENV: "test_token"}):
            assert get_github_token() == "test_token"
    
    def test_get_github_token_missing(self):
        with patch.dict(os.environ, {}, clear=True):
            assert get_github_token() is None
    
    def test_is_xbar_environment_swiftbar(self):
        with patch.dict(os.environ, {"SWIFTBAR": "1"}):
            assert is_xbar_environment() is True
    
    def test_is_xbar_environment_bitbar(self):
        with patch.dict(os.environ, {"BITBAR": "1"}):
            assert is_xbar_environment() is True
    
    def test_is_xbar_environment_neither(self):
        with patch.dict(os.environ, {}, clear=True):
            assert is_xbar_environment() is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])