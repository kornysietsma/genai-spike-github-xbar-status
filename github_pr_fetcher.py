#!/usr/bin/env python3
"""Module for fetching pull requests from GitHub."""

from typing import List, Set
from github import Github, PullRequest
from github_utils import is_dependabot_item


def fetch_pull_requests(client: Github) -> List[PullRequest.PullRequest]:
    """Fetch all relevant pull requests for the authenticated user.
    
    Returns pull requests where the user is:
    - Author
    - Assigned reviewer
    - Mentioned in comments
    - Requested for review
    
    Filters out:
    - Draft PRs
    - Dependabot PRs
    """
    user = client.get_user()
    username = user.login
    
    # Use a set to avoid duplicates
    pr_ids: Set[int] = set()
    all_prs: List[PullRequest.PullRequest] = []
    
    # Search for PRs where user is author
    author_query = f"is:pr is:open author:{username}"
    for pr in client.search_issues(query=author_query):
        pr_obj = pr.as_pull_request()
        if pr_obj.id not in pr_ids and not pr_obj.draft and not is_dependabot_item(pr_obj):
            pr_ids.add(pr_obj.id)
            all_prs.append(pr_obj)
    
    # Search for PRs where user is assigned as reviewer
    reviewer_query = f"is:pr is:open review-requested:{username}"
    for pr in client.search_issues(query=reviewer_query):
        pr_obj = pr.as_pull_request()
        if pr_obj.id not in pr_ids and not pr_obj.draft and not is_dependabot_item(pr_obj):
            pr_ids.add(pr_obj.id)
            all_prs.append(pr_obj)
    
    # Search for PRs where user is mentioned
    mentions_query = f"is:pr is:open mentions:{username}"
    for pr in client.search_issues(query=mentions_query):
        pr_obj = pr.as_pull_request()
        if pr_obj.id not in pr_ids and not pr_obj.draft and not is_dependabot_item(pr_obj):
            pr_ids.add(pr_obj.id)
            all_prs.append(pr_obj)
    
    # Search for PRs where user is assigned
    assignee_query = f"is:pr is:open assignee:{username}"
    for pr in client.search_issues(query=assignee_query):
        pr_obj = pr.as_pull_request()
        if pr_obj.id not in pr_ids and not pr_obj.draft and not is_dependabot_item(pr_obj):
            pr_ids.add(pr_obj.id)
            all_prs.append(pr_obj)
    
    return all_prs