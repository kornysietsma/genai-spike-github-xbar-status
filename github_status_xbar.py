#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "PyGithub>=2.1.0",
#     "swiftbarmenu>=0.1.0",
#     "click>=8.1.0",
# ]
# ///

import os
import sys
import logging
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any

import click
from github import Github, GithubException

# Configuration constants
REFRESH_INTERVAL = 30  # seconds (managed by xbar filename)
NOTIFICATION_WINDOW = 24  # hours
ACTIVITY_THRESHOLD_FEW = 5
ACTIVITY_THRESHOLD_LOTS = 6

# Display constants
ICON_NO_ACTIVITY = "🔵"
ICON_FEW_ACTIVITY = "🟡"
ICON_LOTS_ACTIVITY = "🔴"

# Logging setup
logging.basicConfig(
    level=logging.DEBUG if os.getenv("DEBUG") else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def get_authenticated_client() -> Github:
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN environment variable not set")
    
    try:
        client = Github(token)
        # Test authentication by getting user info
        user = client.get_user()
        logger.debug(f"Authenticated as: {user.login}")
        return client
    except GithubException as e:
        raise ValueError(f"GitHub authentication failed: {e}")


def format_time_ago(timestamp: datetime) -> str:
    now = datetime.now(timestamp.tzinfo)
    delta = now - timestamp
    
    if delta.total_seconds() < 0:
        return "future"
    
    days = delta.days
    hours = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60
    
    if days > 0:
        if hours > 0:
            return f"{days}d{hours}h"
        return f"{days}d"
    elif hours > 0:
        if minutes > 0:
            return f"{hours}h{minutes}m"
        return f"{hours}h"
    elif minutes > 0:
        return f"{minutes}m"
    else:
        return "now"


def truncate_text(text: str, max_length: int = 50) -> str:
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def is_xbar_environment() -> bool:
    return "SWIFTBAR" in os.environ or "BITBAR" in os.environ


def fetch_pull_requests(github_client: Github) -> List[Dict[str, Any]]:
    prs = []
    user = github_client.get_user()
    
    # Search for PRs where user is involved
    # Note: GitHub search has limitations, this is a simplified approach
    query = f"type:pr state:open involves:{user.login} -author:app/dependabot"
    
    try:
        search_results = github_client.search_issues(query)
        for issue in search_results:
            if hasattr(issue, 'pull_request') and issue.pull_request:
                # Get the actual PR object to check if it's a draft
                repo = github_client.get_repo(issue.repository.full_name)
                pr = repo.get_pull(issue.number)
                
                if not pr.draft:  # Exclude drafts as per spec
                    prs.append({
                        'title': issue.title,
                        'url': issue.html_url,
                        'repo': issue.repository.name,
                        'created_at': issue.created_at,
                        'updated_at': issue.updated_at,
                        'type': 'PR'
                    })
    except Exception as e:
        logger.error(f"Error fetching PRs: {e}")
    
    return prs


def fetch_issues(github_client: Github) -> List[Dict[str, Any]]:
    issues = []
    user = github_client.get_user()
    
    # Search for issues where user is involved
    query = f"type:issue state:open involves:{user.login} -author:app/dependabot"
    
    try:
        search_results = github_client.search_issues(query)
        for issue in search_results:
            if not hasattr(issue, 'pull_request') or not issue.pull_request:
                issues.append({
                    'title': issue.title,
                    'url': issue.html_url,
                    'repo': issue.repository.name,
                    'created_at': issue.created_at,
                    'updated_at': issue.updated_at,
                    'type': 'Issue'
                })
    except Exception as e:
        logger.error(f"Error fetching issues: {e}")
    
    return issues


def fetch_notifications(github_client: Github) -> List[Dict[str, Any]]:
    notifications = []
    
    # Calculate 24 hours ago
    since = datetime.now(timezone.utc) - timedelta(hours=NOTIFICATION_WINDOW)
    
    try:
        # Get notifications from the last 24 hours
        user_notifications = github_client.get_user().get_notifications(since=since)
        
        for notification in user_notifications:
            # Filter for mentions only (reason = 'mention')
            if notification.reason == 'mention':
                notifications.append({
                    'title': notification.subject.title,
                    'url': notification.subject.url,  # API URL, would need conversion for web URL
                    'repo': notification.repository.name,
                    'updated_at': notification.updated_at,
                    'type': 'Mention'
                })
    except Exception as e:
        logger.error(f"Error fetching notifications: {e}")
    
    return notifications


def group_items_by_time_and_repo(items: List[Dict[str, Any]]) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
    now = datetime.now(timezone.utc)
    one_hour_ago = now - timedelta(hours=1)
    one_day_ago = now - timedelta(days=1)
    
    grouped = {
        "Last hour": {},
        "Last day": {}
    }
    
    for item in items:
        # Determine time bucket
        item_time = item['updated_at']
        if item_time.replace(tzinfo=timezone.utc) >= one_hour_ago:
            bucket = "Last hour"
        elif item_time.replace(tzinfo=timezone.utc) >= one_day_ago:
            bucket = "Last day"
        else:
            continue  # Skip items older than 1 day
        
        # Group by repo within time bucket
        repo = item['repo']
        if repo not in grouped[bucket]:
            grouped[bucket][repo] = []
        grouped[bucket][repo].append(item)
    
    return grouped


def get_activity_icon(total_items: int) -> str:
    if total_items == 0:
        return ICON_NO_ACTIVITY
    elif total_items <= ACTIVITY_THRESHOLD_FEW:
        return ICON_FEW_ACTIVITY
    else:
        return ICON_LOTS_ACTIVITY


def output_xbar_widget():
    try:
        github_client = get_authenticated_client()
        
        # Fetch all data
        prs = fetch_pull_requests(github_client)
        issues = fetch_issues(github_client)
        notifications = fetch_notifications(github_client)
        
        all_items = prs + issues + notifications
        total_items = len(all_items)
        
        # Menu bar display
        icon = get_activity_icon(total_items)
        print(f"{icon} GitHub")
        print("---")
        
        if total_items == 0:
            print("No recent activity")
            return
        
        # Group by type
        for item_type in ['PR', 'Issue', 'Mention']:
            type_items = [item for item in all_items if item['type'] == item_type]
            if not type_items:
                continue
                
            print(f"**{item_type}s ({len(type_items)})**")
            
            # Group by time and repo
            grouped = group_items_by_time_and_repo(type_items)
            
            for time_bucket in ["Last hour", "Last day"]:
                if not grouped[time_bucket]:
                    continue
                    
                print(f"--{time_bucket}")
                
                for repo, repo_items in grouped[time_bucket].items():
                    print(f"----{repo}")
                    for item in repo_items:
                        age = format_time_ago(item['updated_at'])
                        title = truncate_text(item['title'])
                        print(f"------{age} {title} | href={item['url']}")
            
            print("---")  # Separator between types
        
    except Exception as e:
        print(f"{ICON_LOTS_ACTIVITY} Error")
        print("---")
        print(f"Error: {str(e)}")


@click.command()
@click.option('--debug', is_flag=True, help='Enable debug logging')
def cli(debug: bool):
    if debug:
        logger.setLevel(logging.DEBUG)
    
    try:
        github_client = get_authenticated_client()
        
        # Fetch all data
        prs = fetch_pull_requests(github_client)
        issues = fetch_issues(github_client)
        notifications = fetch_notifications(github_client)
        
        all_items = prs + issues + notifications
        total_items = len(all_items)
        
        click.echo("GitHub Activity Monitor")
        click.echo("=" * 50)
        
        if total_items == 0:
            click.echo("No recent activity")
            return
        
        # Group by type and display with full details
        for item_type in ['PR', 'Issue', 'Mention']:
            type_items = [item for item in all_items if item['type'] == item_type]
            if not type_items:
                continue
                
            click.echo(f"\n{item_type}s ({len(type_items)}):")
            
            # Group by time and repo
            grouped = group_items_by_time_and_repo(type_items)
            
            for time_bucket in ["Last hour", "Last day"]:
                if not grouped[time_bucket]:
                    continue
                    
                click.echo(f"\n  {time_bucket}:")
                
                for repo, repo_items in grouped[time_bucket].items():
                    click.echo(f"    {repo}:")
                    for item in repo_items:
                        age = format_time_ago(item['updated_at'])
                        # Don't truncate in CLI mode
                        click.echo(f"      [{age}] {item['title']}")
                        click.echo(f"               {item['url']}")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        if debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def main() -> None:
    if is_xbar_environment():
        output_xbar_widget()
    else:
        cli()


if __name__ == "__main__":
    main()