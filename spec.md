# GitHub Activity Monitor - Specification

## Overview
A Python-based tool for monitoring recent GitHub activity for a user, displaying open Pull Requests, Issues, and Notifications. The tool operates in two modes:
1. As an xbar widget for macOS menu bar display
2. As a command-line interface for interactive use

## Core Requirements

### Authentication
- Use GitHub API v3 with personal access token
- Token stored in environment variable (xbar manages env vars for widget mode)
- Command-line mode can set env var using 1Password CLI

### Data Sources and Filtering

#### Pull Requests
- Monitor: All repositories user has access to (public and private)
- Include PRs where user is:
  - Author
  - Assigned reviewer
  - Mentioned in comments
  - Requested for review
- Filter: Only show ready PRs (exclude drafts)
- Exclude: Dependabot PRs

#### Issues
- Monitor: All repositories user has access to
- Include issues where user is:
  - Author
  - Assignee
  - Mentioned in issue or comments
- Filter: Only show open issues
- Exclude: Dependabot issues

#### Notifications
- Time window: Last 24 hours
- Filter: Only show mentions
- Behavior: Keep notifications unread in GitHub
- Provide clickable links to GitHub web interface

### Display Modes

#### xbar Widget Mode
**Menu Bar Display:**
- Use emoji icons to indicate activity level:
  - No activity: Default icon
  - 1-5 items: "Few activity" icon
  - 6+ items: "Lots of activity" icon

**Dropdown Menu Structure:**
1. Group by type (PRs, Issues, Notifications)
2. Within type, group by time bucket:
   - Last hour
   - Last day
3. Within time bucket, group by repository
4. For each item show:
   - Age in brief format (e.g., "1h20m")
   - Title (may be truncated for display)

**Error Handling:**
- Show brief error states in menu bar
- User can run command-line version for detailed error messages

#### Command-Line Mode
- Display same information as xbar mode
- Show full titles (no truncation)
- Include URLs for all items
- Provide detailed error messages
- Use plain text output (no rich formatting needed)

### Technical Implementation

#### Dependencies
- PyGithub - GitHub API interaction
- PyXbar - xbar widget functionality
- Click - CLI handling (if useful)
- Standard library for everything else

#### Configuration
- Personal access token: Environment variable
- All other settings: Hardcoded constants in script
  - Refresh interval: 30 seconds (managed by xbar filename)
  - Notification window: 24 hours
  - Activity thresholds: 0, 1-5, 6+

#### Code Structure
- Don't Abstract GitHub API logic
- Don't use unit tests, testing will be manual
- Display logic can remain in main code (text-based, easily testable)
- No caching mechanism needed initially

#### Performance
- Refresh every 30 seconds (via xbar filename convention)
- Fetch fresh data on each refresh
- No result caching between refreshes

### Future Considerations
Settings that are hardcoded initially but may become configurable:
- Notification time window
- Activity level thresholds
- Additional notification types beyond mentions
- Repository filtering options