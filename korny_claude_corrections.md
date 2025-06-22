# Korny's Corrections and Implementation Variations

This document tracks instances where Korny corrected my approach or asked me to vary from my initial implementation.

## Corrections and Variations

1. **Don't create custom models for GitHub data** (Step 3)
   - I initially created custom dataclasses for PullRequest, Issue, and Notification
   - Korny corrected: Use PyGithub's built-in types instead of creating our own models
   - Reason: Keeps code simpler and avoids unnecessary abstraction

2. **Remove unnecessary docstrings** (Step 3)
   - I was adding docstrings to all functions, including simple ones
   - Korny corrected: Only add docstrings for public functions or when parameters/return values are not obvious
   - Applied to: Simple utility functions like `format_age`, `get_time_bucket`, etc.

3. **Skip tests for trivial functions** (Step 3)
   - I was writing comprehensive tests for simple utility functions
   - Korny corrected: Don't write tests for trivial functions
   - Applied to: Basic utility functions in `github_utils.py`

4. **Prefer behavior-focused tests over mock-heavy tests** (Step 7)
   - I initially wrote tests with complex mocks and assertions about implementation details
   - Korny corrected: Use simple stubs that return test data and test behavior, not implementation
   - Example: In `test_activity_aggregator.py`, replaced Mock objects with simple strings and removed assertions about how many times methods were called