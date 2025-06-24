#!/usr/bin/env python3
"""Utility functions for working with PyGithub objects."""

from datetime import datetime, timedelta
from typing import Union
from github import PullRequest, Issue, Notification


def format_age(created_at: datetime) -> str:
    now = datetime.now(created_at.tzinfo)
    age = now - created_at
    
    if age < timedelta(minutes=1):
        return "now"
    elif age < timedelta(hours=1):
        minutes = int(age.total_seconds() / 60)
        return f"{minutes}m"
    elif age < timedelta(days=1):
        hours = int(age.total_seconds() / 3600)
        minutes = int((age.total_seconds() % 3600) / 60)
        if minutes > 0:
            return f"{hours}h{minutes}m"
        return f"{hours}h"
    else:
        days = age.days
        return f"{days}d"


def get_time_bucket(item: Union[PullRequest.PullRequest, Issue.Issue, Notification.Notification]) -> str:
    # Get the relevant timestamp
    if hasattr(item, 'created_at'):
        timestamp = item.created_at
    elif hasattr(item, 'updated_at'):
        timestamp = item.updated_at
    else:
        raise ValueError(f"Item {item} has no timestamp attribute")
    
    now = datetime.now(timestamp.tzinfo)
    age = now - timestamp
    
    if age < timedelta(hours=1):
        return "last_hour"
    elif age < timedelta(days=1):
        return "last_day"
    else:
        return "older"


def is_dependabot_item(item: Union[PullRequest.PullRequest, Issue.Issue]) -> bool:
    if hasattr(item, 'user') and item.user:
        return item.user.login == 'dependabot[bot]'
    return False


def truncate_title(title: str, max_length: int = 50) -> str:
    if len(title) <= max_length:
        return title
    return title[:max_length - 3] + "..."