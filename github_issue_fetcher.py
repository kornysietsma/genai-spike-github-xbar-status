#!/usr/bin/env python3
"""Module for fetching issues from GitHub."""

from typing import List, Set
from github import Github, Issue
from github_utils import is_dependabot_item


def fetch_issues(client: Github) -> List[Issue.Issue]:
    """Fetch all relevant issues for the authenticated user.
    
    Returns issues where the user is:
    - Author
    - Assignee  
    - Mentioned in issue or comments
    
    Filters out:
    - Closed issues (only returns open issues)
    - Dependabot issues
    """
    user = client.get_user()
    username = user.login
    
    # Use a set to avoid duplicates
    issue_ids: Set[int] = set()
    all_issues: List[Issue.Issue] = []
    
    # Search for issues where user is author
    author_query = f"is:issue is:open author:{username}"
    for issue in client.search_issues(query=author_query):
        if issue.id not in issue_ids and not is_dependabot_item(issue):
            issue_ids.add(issue.id)
            all_issues.append(issue)
    
    # Search for issues where user is assignee
    assignee_query = f"is:issue is:open assignee:{username}"
    for issue in client.search_issues(query=assignee_query):
        if issue.id not in issue_ids and not is_dependabot_item(issue):
            issue_ids.add(issue.id)
            all_issues.append(issue)
    
    # Search for issues where user is mentioned
    mentions_query = f"is:issue is:open mentions:{username}"
    for issue in client.search_issues(query=mentions_query):
        if issue.id not in issue_ids and not is_dependabot_item(issue):
            issue_ids.add(issue.id)
            all_issues.append(issue)
    
    return all_issues