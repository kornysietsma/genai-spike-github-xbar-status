# GitHub Activity Monitor - Todo List

## Completed
- [x] Remove all test files and testing infrastructure
- [x] Consolidate into single uv script
- [x] Basic authentication with GITHUB_TOKEN
- [x] Fetch PRs (excluding drafts and dependabot)
- [x] Fetch Issues (excluding dependabot)
- [x] Fetch Notifications (mentions only from last 24h)
- [x] Group items by type, time bucket, and repository
- [x] Display appropriate emoji based on activity count
- [x] Basic xbar and CLI output formatting

## High Priority - Core Functionality
- [ ] Fix notification URLs (convert API URLs to web URLs)
- [ ] Add proper error handling for rate limits
- [ ] Improve error messages to be more helpful

## Medium Priority - Improvements
- [ ] Optimize API calls (avoid fetching full PR objects)
- [ ] Add refresh menu item in xbar mode
- [ ] Better handling of edge cases (long titles, unicode, etc)

## Low Priority - Nice to Have
- [ ] Improve search queries for better coverage
- [ ] Add CLI flags for configuration
- [ ] Add debug timing information
- [ ] Consider deduplication of results

## Testing Checklist
- [ ] Test with no GITHUB_TOKEN set
- [ ] Test with invalid GITHUB_TOKEN
- [ ] Test with no activity
- [ ] Test with 1-5 items (yellow emoji)
- [ ] Test with 6+ items (red emoji)
- [ ] Test clickable links in xbar
- [ ] Test CLI mode with --debug flag
- [ ] Test 30 second refresh in xbar