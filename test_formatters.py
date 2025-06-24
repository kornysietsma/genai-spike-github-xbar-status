#!/usr/bin/env python3
# /// script
# dependencies = [
#     "pytest>=7.0.0",
#     "PyGithub>=2.0.0",
# ]
# requires-python = ">=3.12"
# ///

from datetime import datetime, timedelta, timezone
from unittest.mock import Mock
from formatters import group_by_time


class TestGroupByTime:
    def test_empty_items(self):
        """Test grouping with no items."""
        result = group_by_time([])
        assert result == {"last_hour": {}, "last_day": {}}
    
    def test_single_item_last_hour(self):
        """Test single item from the last hour."""
        now = datetime.now(timezone.utc)
        
        # Mock PullRequest
        pr = Mock()
        pr.id = 1
        pr.title = "Recent PR"
        pr.html_url = "https://github.com/owner/repo/pull/1"
        pr.updated_at = now - timedelta(minutes=30)
        pr.draft = False
        
        # Mock repository
        pr.repository = Mock()
        pr.repository.full_name = "owner/repo"
        
        result = group_by_time([pr])
        assert "owner/repo" in result["last_hour"]
        assert len(result["last_hour"]["owner/repo"]) == 1
        assert result["last_hour"]["owner/repo"][0] == pr
        assert result["last_day"] == {}
    
    def test_single_item_last_day(self):
        """Test single item from the last day but not last hour."""
        now = datetime.now(timezone.utc)
        
        # Mock Issue
        issue = Mock()
        issue.id = 2
        issue.title = "Yesterday's issue"
        issue.html_url = "https://github.com/owner/repo/issues/2"
        issue.updated_at = now - timedelta(hours=12)
        
        # Mock repository
        issue.repository = Mock()
        issue.repository.full_name = "owner/repo"
        
        result = group_by_time([issue])
        assert result["last_hour"] == {}
        assert "owner/repo" in result["last_day"]
        assert len(result["last_day"]["owner/repo"]) == 1
        assert result["last_day"]["owner/repo"][0] == issue
    
    def test_multiple_items_same_repo(self):
        """Test multiple items from same repository."""
        now = datetime.now(timezone.utc)
        
        # Mock PullRequest 1
        pr1 = Mock()
        pr1.id = 1
        pr1.title = "PR 1"
        pr1.html_url = "https://github.com/owner/repo/pull/1"
        pr1.updated_at = now - timedelta(minutes=20)
        pr1.draft = False
        pr1.repository = Mock()
        pr1.repository.full_name = "owner/repo"
        
        # Mock PullRequest 2
        pr2 = Mock()
        pr2.id = 2
        pr2.title = "PR 2"
        pr2.html_url = "https://github.com/owner/repo/pull/2"
        pr2.updated_at = now - timedelta(minutes=40)
        pr2.draft = False
        pr2.repository = Mock()
        pr2.repository.full_name = "owner/repo"
        
        result = group_by_time([pr1, pr2])
        assert "owner/repo" in result["last_hour"]
        assert len(result["last_hour"]["owner/repo"]) == 2
        # Check ordering - newest first
        assert result["last_hour"]["owner/repo"][0] == pr1
        assert result["last_hour"]["owner/repo"][1] == pr2
    
    def test_multiple_repos(self):
        """Test items from different repositories."""
        now = datetime.now(timezone.utc)
        
        # Mock PullRequest
        pr = Mock()
        pr.id = 1
        pr.title = "PR in repo1"
        pr.html_url = "https://github.com/owner/repo1/pull/1"
        pr.updated_at = now - timedelta(minutes=30)
        pr.draft = False
        pr.repository = Mock()
        pr.repository.full_name = "owner/repo1"
        
        # Mock Issue
        issue = Mock()
        issue.id = 2
        issue.title = "Issue in repo2"
        issue.html_url = "https://github.com/owner/repo2/issues/2"
        issue.updated_at = now - timedelta(minutes=45)
        issue.repository = Mock()
        issue.repository.full_name = "owner/repo2"
        
        result = group_by_time([pr, issue])
        assert "owner/repo1" in result["last_hour"]
        assert "owner/repo2" in result["last_hour"]
        assert len(result["last_hour"]["owner/repo1"]) == 1
        assert len(result["last_hour"]["owner/repo2"]) == 1
    
    def test_mixed_time_periods(self):
        """Test items spanning both time periods."""
        now = datetime.now(timezone.utc)
        
        # Mock recent PullRequest
        recent_pr = Mock()
        recent_pr.id = 1
        recent_pr.title = "Recent PR"
        recent_pr.html_url = "https://github.com/owner/repo/pull/1"
        recent_pr.updated_at = now - timedelta(minutes=30)
        recent_pr.draft = False
        recent_pr.repository = Mock()
        recent_pr.repository.full_name = "owner/repo"
        
        # Mock old Issue
        old_issue = Mock()
        old_issue.id = 2
        old_issue.title = "Old issue"
        old_issue.html_url = "https://github.com/owner/repo/issues/2"
        old_issue.updated_at = now - timedelta(hours=18)
        old_issue.repository = Mock()
        old_issue.repository.full_name = "owner/repo"
        
        result = group_by_time([recent_pr, old_issue])
        assert "owner/repo" in result["last_hour"]
        assert "owner/repo" in result["last_day"]
        assert len(result["last_hour"]["owner/repo"]) == 1
        assert len(result["last_day"]["owner/repo"]) == 1
        assert result["last_hour"]["owner/repo"][0] == recent_pr
        assert result["last_day"]["owner/repo"][0] == old_issue
    
    def test_ordering_within_group(self):
        """Test that items are ordered newest first within each group."""
        now = datetime.now(timezone.utc)
        items = []
        
        # Create items with different timestamps
        for i in range(3):
            pr = Mock()
            pr.id = i
            pr.title = f"PR {i}"
            pr.html_url = f"https://github.com/owner/repo/pull/{i}"
            pr.updated_at = now - timedelta(minutes=10 + i * 10)
            pr.draft = False
            pr.repository = Mock()
            pr.repository.full_name = "owner/repo"
            items.append(pr)
        
        result = group_by_time(items)
        assert "owner/repo" in result["last_hour"]
        repo_items = result["last_hour"]["owner/repo"]
        assert len(repo_items) == 3
        
        # Check ordering - newest (smallest time delta) first
        assert repo_items[0].id == 0  # 10 minutes ago
        assert repo_items[1].id == 1  # 20 minutes ago
        assert repo_items[2].id == 2  # 30 minutes ago
    
    def test_notification_grouping(self):
        """Test that notifications are grouped correctly."""
        now = datetime.now(timezone.utc)
        
        # Mock Notification
        notification = Mock()
        notification.id = "n1"
        notification.subject = Mock()
        notification.subject.title = "You were mentioned"
        notification.subject.url = "https://github.com/owner/repo/issues/1"
        notification.updated_at = now - timedelta(minutes=15)
        notification.reason = "mention"
        notification.unread = True
        notification.repository = Mock()
        notification.repository.full_name = "owner/repo"
        
        result = group_by_time([notification])
        assert "owner/repo" in result["last_hour"]
        assert result["last_hour"]["owner/repo"][0] == notification
    
    def test_items_older_than_day(self):
        """Test that items older than 24 hours are excluded."""
        now = datetime.now(timezone.utc)
        
        # Mock old PullRequest
        old_pr = Mock()
        old_pr.id = 1
        old_pr.title = "Old PR"
        old_pr.html_url = "https://github.com/owner/repo/pull/1"
        old_pr.updated_at = now - timedelta(hours=36)
        old_pr.draft = False
        old_pr.repository = Mock()
        old_pr.repository.full_name = "owner/repo"
        
        result = group_by_time([old_pr])
        assert result["last_hour"] == {}
        assert result["last_day"] == {}
    
    def test_mixed_item_types(self):
        """Test grouping with different types of items."""
        now = datetime.now(timezone.utc)
        
        # Mock PullRequest
        pr = Mock()
        pr.id = 1
        pr.title = "PR"
        pr.html_url = "https://github.com/owner/repo/pull/1"
        pr.updated_at = now - timedelta(minutes=20)
        pr.draft = False
        pr.repository = Mock()
        pr.repository.full_name = "owner/repo"
        
        # Mock Issue
        issue = Mock()
        issue.id = 2
        issue.title = "Issue"
        issue.html_url = "https://github.com/owner/repo/issues/2"
        issue.updated_at = now - timedelta(minutes=30)
        issue.repository = Mock()
        issue.repository.full_name = "owner/repo"
        
        # Mock Notification
        notification = Mock()
        notification.id = "n1"
        notification.subject = Mock()
        notification.subject.title = "Notification"
        notification.subject.url = "https://github.com/owner/repo/issues/3"
        notification.updated_at = now - timedelta(minutes=25)
        notification.reason = "mention"
        notification.unread = True
        notification.repository = Mock()
        notification.repository.full_name = "owner/repo"
        
        result = group_by_time([pr, issue, notification])
        assert "owner/repo" in result["last_hour"]
        repo_items = result["last_hour"]["owner/repo"]
        assert len(repo_items) == 3
        # Check ordering - newest first
        assert repo_items[0] == pr        # 20 min ago
        assert repo_items[1] == notification  # 25 min ago
        assert repo_items[2] == issue     # 30 min ago