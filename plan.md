# GitHub Activity Monitor - TDD Implementation Plan

## Overview
This plan breaks down the GitHub Activity Monitor into small, testable steps. Each step builds on the previous one, ensuring continuous integration and no orphaned code.

## Architecture Overview
The project will be structured as follows:
- `github_status_xbar.py` - Main script with xbar integration
- `github_client.py` - Abstracted GitHub API client
- `models.py` - Data models for PRs, Issues, Notifications
- `formatters.py` - Display formatting logic
- `test_*.py` - Test files for each module

## Implementation Steps

### Step 1: Project Setup and Basic Structure

```text
Set up the basic Python project structure with dependencies and configuration. Create a minimal script that can run both as an xbar widget and command-line tool.

1. Update the existing github_status_xbar.py to use inline script metadata (PEP 723) with dependencies: PyGithub, PyXbar, Click
2. Create a basic main() function that detects if running in xbar mode or CLI mode
3. Add configuration constants for: TOKEN_ENV_VAR name, NOTIFICATION_WINDOW_HOURS (24), ACTIVITY_THRESHOLDS (0, 5, 6)
4. Create a simple test that verifies the script can be imported and main() can be called
5. Implement basic error handling that prints to stderr for CLI and returns xbar-formatted error for widget mode

The script should successfully run in both modes, showing a placeholder message.
```

### Step 2: GitHub Authentication Module

```text
Create a GitHub client module that handles authentication and provides a testable interface to the GitHub API.

1. Create github_client.py with a GitHubClient class
2. Implement __init__ that takes a token parameter and creates a PyGithub instance
3. Add a property to get the authenticated user
4. Create error handling for invalid/missing tokens that raises custom exceptions
5. Write tests using mock PyGithub instances to verify:
   - Successful authentication with valid token
   - Appropriate exception for invalid token
   - Appropriate exception for missing token
6. Update main script to read token from environment variable and create client instance

The module should handle all authentication concerns and be fully tested with mocks.
```

### Step 3: Data Models

```text
Use PyGithub's built-in models directly instead of creating custom data models.

1. Rely on PyGithub's PullRequest, Issue, and Notification objects
2. Create utility functions in github_utils.py for common operations:
   - format_age() to format age as brief string (e.g., "1h20m", "3d") 
   - get_time_bucket() to categorize items by time
   - is_dependabot_item() to check if item is from dependabot
   - truncate_title() for display formatting
3. Write tests for all utility functions
4. Use PyGithub objects throughout the codebase

This approach avoids data translation overhead and leverages PyGithub's existing functionality.
```

### Step 4: Fetching Pull Requests

```text
Implement the GitHub client method to fetch relevant pull requests.

1. Add fetch_pull_requests() method to GitHubClient
2. Implement search query to find PRs where user is: author, reviewer, mentioned, or review requested
3. Filter out draft PRs at the API level if possible, otherwise in code
4. Filter out dependabot PRs (check author login)
5. Convert GitHub PR objects to our PullRequest model
6. Write tests with mock data covering:
   - PRs where user is author
   - PRs where user is requested reviewer
   - Filtering out drafts
   - Filtering out dependabot
   - Empty results
7. Handle pagination if needed

The method should return a list of PullRequest objects matching our criteria.
```

### Step 5: Fetching Issues

```text
Implement the GitHub client method to fetch relevant issues.

1. Add fetch_issues() method to GitHubClient
2. Implement search query to find issues where user is: author, assignee, or mentioned
3. Filter to only include open issues
4. Filter out dependabot issues
5. Convert GitHub issue objects to our Issue model
6. Write tests with mock data covering:
   - Issues where user is author
   - Issues where user is assignee
   - Issues where user is mentioned
   - Filtering out closed issues
   - Filtering out dependabot
   - Empty results
7. Handle pagination if needed

The method should return a list of Issue objects matching our criteria.
```

### Step 6: Fetching Notifications

```text
Implement the GitHub client method to fetch recent notifications.

1. Add fetch_notifications() method to GitHubClient
2. Fetch all notifications from the last 24 hours
3. Filter to only include mention reasons
4. Keep notifications unread (don't mark as read)
5. Convert GitHub notification objects to our Notification model
6. Write tests with mock data covering:
   - Recent notifications with mention reason
   - Filtering out non-mention notifications
   - Filtering out old notifications
   - Empty results
7. Ensure we're respecting the time window

The method should return a list of Notification objects from the last 24 hours with mention reason.
```

### Step 7: Activity Aggregation

```text
Create a method to fetch all activity and calculate summary statistics.

1. Add fetch_all_activity() method to GitHubClient that calls all three fetch methods
2. Return a dictionary with 'pull_requests', 'issues', 'notifications' keys
3. Add calculate_activity_level() function that takes counts and returns 'none', 'few', or 'many'
4. Write tests for:
   - Successful aggregation of all three types
   - Correct activity level calculation (0, 1-5, 6+)
   - Handling when individual fetches fail
5. Add error handling to gracefully handle partial failures

This provides a single entry point for fetching all GitHub activity.
```

### Step 8: Time-based Grouping Logic

```text
Implement the logic to group items by time buckets.

1. Create a group_by_time() function in formatters.py
2. Implement logic to categorize items into "last hour" and "last day" buckets
3. Within each time bucket, group by repository
4. Maintain order: newest items first within each group
5. Write tests for:
   - Items from the last hour
   - Items from the last day but not last hour
   - Items from same repository staying together
   - Correct ordering within groups
6. Use the age calculation from models

This prepares the data for display in the hierarchical format.
```

### Step 9: Basic CLI Formatter

```text
Create a CLI formatter that outputs plain text with full information.

1. Create format_for_cli() function in formatters.py
2. Display items grouped by type (PRs, Issues, Notifications)
3. Within each type, use the time-based grouping
4. Show full titles and URLs
5. Include item counts and activity summary
6. Write tests for:
   - Formatting each type of item
   - Correct grouping and ordering
   - Empty results handling
   - Multiple items from same repo
7. Keep output simple and readable

The formatter should produce clean, scannable text output.
```

### Step 10: xbar Formatter

```text
Create an xbar formatter that outputs xbar-compatible format.

1. Create format_for_xbar() function in formatters.py
2. Implement menu bar line with appropriate emoji based on activity level
3. Format dropdown with proper xbar syntax including:
   - Separators between groups
   - Clickable URLs using href parameter
   - Proper escaping of special characters
4. Truncate long titles appropriately
5. Write tests for:
   - Emoji selection based on activity level
   - Proper xbar syntax generation
   - URL formatting with href
   - Title truncation
6. Use PyXbar if it simplifies formatting

The formatter should produce valid xbar output that displays correctly.
```

### Step 11: Error Handling and Display

```text
Implement comprehensive error handling for both display modes.

1. Create custom exception classes for different error types
2. Add format_error_for_cli() function for detailed error messages
3. Add format_error_for_xbar() function for brief menu bar errors
4. Handle specific cases:
   - Missing/invalid token
   - Network errors
   - Rate limiting
   - API errors
5. Write tests for each error scenario in both formats
6. Ensure errors are user-friendly and actionable

Error handling should guide users to resolution.
```

### Step 12: Main Script Integration

```text
Wire everything together in the main script.

1. Update github_status_xbar.py to use all modules
2. Detect execution mode (xbar vs CLI)
3. Create GitHubClient with token from environment
4. Fetch all activity
5. Format appropriately based on mode
6. Handle all errors gracefully
7. Add Click decorators if beneficial for CLI mode
8. Write integration tests that mock GitHubClient
9. Test both successful and error paths
10. Ensure script name follows xbar convention for 30s refresh

The script should be fully functional in both modes.
```

### Step 13: Final Testing and Polish

```text
Add comprehensive integration tests and polish the user experience.

1. Create test_integration.py with end-to-end tests
2. Test complete workflows for both CLI and xbar modes
3. Add any missing edge case tests
4. Verify proper exit codes
5. Test with various combinations of activity
6. Add helpful docstrings throughout
7. Ensure all error messages are clear
8. Verify xbar output renders correctly
9. Test script can be run directly and via xbar

The tool should be production-ready with comprehensive test coverage.
```

## Testing Strategy

Each step includes specific test requirements. Tests should:
- Use mocks to avoid real API calls
- Cover both happy paths and error cases
- Be independent and fast
- Use clear test names that describe the scenario

## Success Criteria

After completing all steps:
1. Both CLI and xbar modes work correctly
2. All three types of GitHub activity are fetched and displayed
3. Filtering rules are properly applied
4. Error handling is comprehensive
5. Code is well-tested and maintainable
6. No orphaned code - everything is integrated