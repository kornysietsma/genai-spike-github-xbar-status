#!/usr/bin/env python3

import pytest
from unittest.mock import Mock
from github_issue_fetcher import fetch_issues


class TestFetchIssues:
    def test_fetch_issues_filters_dependabot(self):
        # Mock GitHub client
        client = Mock()
        user = Mock()
        user.login = "testuser"
        client.get_user.return_value = user
        
        # Create mock issues - one from dependabot, one from regular user
        dependabot_issue = Mock()
        dependabot_issue.id = 1
        dependabot_issue.user = Mock()
        dependabot_issue.user.login = "dependabot[bot]"
        
        regular_issue = Mock()
        regular_issue.id = 2
        regular_issue.user = Mock()
        regular_issue.user.login = "regularuser"
        
        client.search_issues.return_value = [dependabot_issue, regular_issue]
        
        # Fetch issues
        issues = fetch_issues(client)
        
        # Should only include the regular user issue
        assert len(issues) == 1
        assert issues[0].id == 2
    
    def test_fetch_issues_deduplicates(self):
        # Mock GitHub client
        client = Mock()
        user = Mock()
        user.login = "testuser"
        client.get_user.return_value = user
        
        # Create a mock issue that appears in multiple searches
        issue = Mock()
        issue.id = 123
        issue.user = Mock()
        issue.user.login = "someuser"
        
        # Return the same issue for all queries
        client.search_issues.return_value = [issue]
        
        # Fetch issues
        issues = fetch_issues(client)
        
        # Should only include the issue once despite multiple queries
        assert len(issues) == 1
        assert issues[0].id == 123
        
        # Verify all 3 queries were made
        assert client.search_issues.call_count == 3
    
    def test_fetch_issues_only_returns_open(self):
        # Mock GitHub client  
        client = Mock()
        user = Mock()
        user.login = "testuser"
        client.get_user.return_value = user
        
        # The query should include "is:open"
        client.search_issues.return_value = []
        
        fetch_issues(client)
        
        # Check that all queries included "is:open"
        for call in client.search_issues.call_args_list:
            query = call[1]['query']
            assert "is:open" in query