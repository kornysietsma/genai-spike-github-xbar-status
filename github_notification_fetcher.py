#!/usr/bin/env python3
"""Module for fetching notifications from GitHub."""

from datetime import datetime, timedelta, timezone
from typing import List
from github import Github, Notification


def fetch_notifications(client: Github) -> List[Notification.Notification]:
    """Fetch recent mention notifications for the authenticated user.
    
    Returns notifications that:
    - Are mentions only
    - Were updated in the last 24 hours
    - Does NOT mark them as read (preserves unread state)
    """
    # Calculate 24 hours ago
    since = datetime.now(timezone.utc) - timedelta(hours=24)
    
    # Get all unread notifications
    # participating=False ensures we don't mark them as read
    notifications = client.get_user().get_notifications(
        all=False,  # Only unread
        participating=False,  # Don't mark as read
        since=since
    )
    
    # Filter to only mentions
    mention_notifications = []
    for notification in notifications:
        if notification.reason == "mention":
            mention_notifications.append(notification)
    
    return mention_notifications