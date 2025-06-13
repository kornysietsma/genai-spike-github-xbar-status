# GitHub Activity Monitor for xbar

> [!WARNING]
> **Experimental GenAI Spike Project**
> 
> This is an experimental spike to explore GenAI tooling capabilities. The code is intentionally verbose, over-documented, and not yet functional. This project is being built incrementally using AI assistance to test development workflows and tooling integration.
> 
> **Not ready for production use!**

A Python-based tool that monitors your GitHub activity and displays it in your macOS menu bar using [xbar](https://github.com/matryer/xbar) (formerly BitBar).

## Features

- Monitors open Pull Requests where you're involved (author, reviewer, mentioned)
- Tracks Issues where you're author, assignee, or mentioned
- Shows recent GitHub notifications (last 24 hours)
- Groups activities by type and time for easy scanning
- Works both as an xbar widget and command-line tool

## Requirements

- macOS with [xbar](https://github.com/matryer/xbar) installed
- [uv](https://github.com/astral-sh/uv) - Python package manager
- Python 3.12 or higher
- GitHub personal access token

## Installation

1. Install xbar if you haven't already
2. Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
3. Copy `github_status_xbar.py` to your xbar plugins directory
4. Rename it to include refresh interval: `github_status_xbar.30s.py` (for 30-second refresh)
5. Make it executable: `chmod +x github_status_xbar.30s.py`
6. Set your GitHub token in xbar's environment variables: `GITHUB_TOKEN=your_token_here`

## Usage

### As xbar Widget
The script automatically detects when running in xbar and displays:
- Menu bar icon showing activity level (=5 none, =� some, =4 lots)
- Dropdown with PRs, Issues, and Notifications grouped by time

### As Command Line Tool
Run directly for detailed output:
```bash
./github_status_xbar.py
```

Or with uv:
```bash
uv run github_status_xbar.py
```

## Development

This project uses [uv](https://github.com/astral-sh/uv) for dependency management with inline script metadata (PEP 723).

Run tests:
```bash
uv run tests/test_utils.py
```