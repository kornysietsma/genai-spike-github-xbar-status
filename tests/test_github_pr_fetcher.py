#!/usr/bin/env python3

import pytest
from unittest.mock import Mock, MagicMock
from github_pr_fetcher import fetch_pull_requests


class TestFetchPullRequests:
    def test_fetch_prs_filters_drafts(self):
        # Mock GitHub client
        client = Mock()
        user = Mock()
        user.login = "testuser"
        client.get_user.return_value = user
        
        # Create mock PRs - one draft, one ready
        draft_pr = Mock()
        draft_pr.id = 1
        draft_pr.draft = True
        draft_pr.user = Mock()
        draft_pr.user.login = "someuser"
        
        ready_pr = Mock()
        ready_pr.id = 2
        ready_pr.draft = False
        ready_pr.user = Mock()
        ready_pr.user.login = "anotheruser"
        
        # Mock search results
        search_result_draft = Mock()
        search_result_draft.as_pull_request.return_value = draft_pr
        
        search_result_ready = Mock()
        search_result_ready.as_pull_request.return_value = ready_pr
        
        client.search_issues.return_value = [search_result_draft, search_result_ready]
        
        # Fetch PRs
        prs = fetch_pull_requests(client)
        
        # Should only include the ready PR
        assert len(prs) == 1
        assert prs[0].id == 2
    
    def test_fetch_prs_filters_dependabot(self):
        # Mock GitHub client
        client = Mock()
        user = Mock()
        user.login = "testuser"
        client.get_user.return_value = user
        
        # Create mock PRs - one from dependabot, one from regular user
        dependabot_pr = Mock()
        dependabot_pr.id = 1
        dependabot_pr.draft = False
        dependabot_pr.user = Mock()
        dependabot_pr.user.login = "dependabot[bot]"
        
        regular_pr = Mock()
        regular_pr.id = 2
        regular_pr.draft = False
        regular_pr.user = Mock()
        regular_pr.user.login = "regularuser"
        
        # Mock search results
        search_result_bot = Mock()
        search_result_bot.as_pull_request.return_value = dependabot_pr
        
        search_result_regular = Mock()
        search_result_regular.as_pull_request.return_value = regular_pr
        
        client.search_issues.return_value = [search_result_bot, search_result_regular]
        
        # Fetch PRs
        prs = fetch_pull_requests(client)
        
        # Should only include the regular user PR
        assert len(prs) == 1
        assert prs[0].id == 2
    
    def test_fetch_prs_deduplicates(self):
        # Mock GitHub client
        client = Mock()
        user = Mock()
        user.login = "testuser"
        client.get_user.return_value = user
        
        # Create a mock PR that appears in multiple searches
        pr = Mock()
        pr.id = 123
        pr.draft = False
        pr.user = Mock()
        pr.user.login = "someuser"
        
        # Mock search result
        search_result = Mock()
        search_result.as_pull_request.return_value = pr
        
        # Return the same PR for all queries
        client.search_issues.return_value = [search_result]
        
        # Fetch PRs
        prs = fetch_pull_requests(client)
        
        # Should only include the PR once despite multiple queries
        assert len(prs) == 1
        assert prs[0].id == 123
        
        # Verify all 4 queries were made
        assert client.search_issues.call_count == 4