#!/usr/bin/env python3
"""Module for aggregating GitHub activity data."""

from dataclasses import dataclass
from typing import List
from github import Github, PullRequest, Issue, Notification
from github_pr_fetcher import fetch_pull_requests
from github_issue_fetcher import fetch_issues
from github_notification_fetcher import fetch_notifications


@dataclass
class ActivityData:
    """Container for all GitHub activity data."""
    pull_requests: List[PullRequest.PullRequest]
    issues: List[Issue.Issue]
    notifications: List[Notification.Notification]
    
    @property
    def total_count(self) -> int:
        """Total count of all activity items."""
        return len(self.pull_requests) + len(self.issues) + len(self.notifications)
    
    @property
    def activity_level(self) -> str:
        """Determine activity level for menu bar display.
        
        Returns:
            "none" for 0 items
            "low" for 1-5 items  
            "high" for 6+ items
        """
        if self.total_count == 0:
            return "none"
        elif self.total_count <= 5:
            return "low"
        else:
            return "high"


def fetch_all_activity(client: Github) -> ActivityData:
    """Fetch all GitHub activity for the authenticated user.
    
    Args:
        client: Authenticated GitHub client
        
    Returns:
        ActivityData containing all fetched items
    """
    pull_requests = fetch_pull_requests(client)
    issues = fetch_issues(client)
    notifications = fetch_notifications(client)
    
    return ActivityData(
        pull_requests=pull_requests,
        issues=issues,
        notifications=notifications
    )