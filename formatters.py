#!/usr/bin/env python3
# /// script
# dependencies = []
# requires-python = ">=3.12"
# ///

from datetime import datetime, timedelta, timezone
from typing import Union, Dict, List
from github import PullRequest, Issue, Notification

ActivityItem = Union[PullRequest.PullRequest, Issue.Issue, Notification.Notification]


def group_by_time(items: List[ActivityItem]) -> Dict[str, Dict[str, List[ActivityItem]]]:
    """
    Group items by time buckets (last hour, last day) and then by repository.
    
    Returns a dict with 'last_hour' and 'last_day' keys, each containing
    a dict mapping repository names to lists of items, ordered newest first.
    """
    result = {"last_hour": {}, "last_day": {}}
    
    if not items:
        return result
    
    now = datetime.now(timezone.utc)
    one_hour_ago = now - timedelta(hours=1)
    one_day_ago = now - timedelta(days=1)
    
    for item in items:
        # All GitHub items should have updated_at and repository attributes
        if not hasattr(item, 'updated_at') or not hasattr(item, 'repository'):
            continue
            
        item_time = item.updated_at
        
        # Skip items older than 24 hours
        if item_time < one_day_ago:
            continue
        
        # Determine which bucket this item belongs in
        if item_time >= one_hour_ago:
            bucket = result["last_hour"]
        else:
            bucket = result["last_day"]
        
        # Get repository name
        repo_name = item.repository.full_name
        
        if repo_name not in bucket:
            bucket[repo_name] = []
        bucket[repo_name].append(item)
    
    # Sort items within each repository group by updated_at (newest first)
    for bucket in [result["last_hour"], result["last_day"]]:
        for repo_name in bucket:
            bucket[repo_name].sort(key=lambda x: x.updated_at, reverse=True)
    
    return result