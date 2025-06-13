# Plan: Step 1 - Project Setup and Basic Structure

## Goal
Establish the foundational structure for the GitHub Activity Monitor, setting up dependencies, configuration, and basic script architecture.

## Implementation Plan

### 1. Script Metadata and Dependencies
- Set up inline script metadata (PEP 723) with required dependencies:
  - PyGithub for GitHub API interaction
  - pyxbar for xbar widget functionality
  - click for CLI handling
  - Python 3.12+ requirement

### 2. Configuration Module
Create a configuration module that defines:
- Constants for refresh intervals, time windows, thresholds
- Environment variable names for GitHub token
- Display settings (emoji icons, text formatting)
- Error messages

### 3. Basic Script Structure
- Main entry point that detects execution context (xbar vs CLI)
- Placeholder functions for:
  - xbar widget output
  - CLI output
  - Error handling
- Basic logging setup for debugging

### 4. Utility Functions
Create utility module with:
- Time formatting functions (e.g., "1h20m" format)
- Text truncation function for xbar display
- Environment variable validation

### 5. Test Infrastructure
- Set up test directory structure
- Create base test class with common fixtures
- Write tests for utility functions
- Add test for environment detection

## Testing Strategy
- Test utility functions with various inputs
- Test configuration loading
- Test environment detection logic
- Mock environment variables for testing

## Success Criteria
- Script runs without errors in both xbar and CLI modes
- Dependencies are properly declared
- Basic test suite passes
- Configuration is cleanly separated from logic
- Utility functions work correctly