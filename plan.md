# GitHub Activity Monitor - Implementation Plan (Non-TDD)

## Overview
This plan outlines the remaining work to complete the GitHub Activity Monitor as a single Python script that works both as an xbar widget and command-line tool, without tests.

## Current Status
- Basic script structure is in place with all core functionality
- Authentication works with GITHUB_TOKEN environment variable
- Fetches PRs, Issues, and Notifications from GitHub API
- Groups items by type, time bucket, and repository
- Displays appropriate emoji in menu bar based on activity level
- Formats output for both xbar widget and CLI modes

## Remaining Tasks

### 1. Fix Notification URLs
The notification URLs are currently API URLs that need to be converted to web URLs. The notification.subject.url returns something like `https://api.github.com/repos/owner/repo/issues/123` which needs to be converted to `https://github.com/owner/repo/issues/123`.

### 2. Improve PR and Issue Search
The current search using `involves:{user.login}` might miss some cases. Consider using more specific queries or multiple searches:
- For PRs: separate searches for author, review-requested, assignee
- For Issues: separate searches for author, assignee, mentioned
- Combine and deduplicate results

### 3. Handle Rate Limiting
Add proper handling for GitHub API rate limits:
- Catch rate limit exceptions
- Display appropriate error message
- Show when rate limit will reset

### 4. Add Refresh Command
In xbar mode, add a "Refresh" menu item that runs the script again.

### 5. Optimize API Calls
Currently fetching full PR objects to check draft status is inefficient. Look for ways to:
- Filter drafts in the search query if possible
- Batch API calls where feasible
- Only fetch necessary fields

### 6. Better Error Messages
Improve error messages to be more helpful:
- For missing token: explain how to set GITHUB_TOKEN
- For network errors: suggest checking connection
- For API errors: show specific error from GitHub

### 7. Add Configuration Options
While keeping configuration in constants, consider adding:
- Command line flags for different time windows
- Flag to include/exclude certain types of activity
- Flag to show all notifications (not just mentions)

### 8. Handle Edge Cases
- Very long repository names or titles
- Unicode in titles
- Items with no updated_at timestamp
- Repositories user no longer has access to

### 9. Performance Monitoring
Add timing information in debug mode to identify slow operations.

### 10. Manual Testing Checklist
Before considering complete, manually test:
- [ ] xbar widget displays correctly with no activity
- [ ] xbar widget displays correctly with 1-5 items  
- [ ] xbar widget displays correctly with 6+ items
- [ ] CLI mode works with --debug flag
- [ ] Handles missing GITHUB_TOKEN gracefully
- [ ] Handles invalid GITHUB_TOKEN gracefully
- [ ] PRs display correctly (excluding drafts and dependabot)
- [ ] Issues display correctly (excluding dependabot)
- [ ] Notifications display correctly (mentions only)
- [ ] Time buckets work correctly
- [ ] Repository grouping works correctly
- [ ] Links are clickable in xbar dropdown
- [ ] Refresh interval works (30 seconds via filename)

## Implementation Notes
- Keep everything in a single file for simplicity
- Use PyGithub's built-in models and methods
- Focus on reliability and user experience
- Don't over-engineer - this is a simple status widget