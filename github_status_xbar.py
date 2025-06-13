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
from datetime import datetime
from typing import Optional

import click

# Configuration constants
REFRESH_INTERVAL = 30  # seconds (managed by xbar filename)
NOTIFICATION_WINDOW = 24  # hours
ACTIVITY_THRESHOLD_FEW = 5
ACTIVITY_THRESHOLD_LOTS = 6

# Environment variables
GITHUB_TOKEN_ENV = "GITHUB_TOKEN"

# Display constants
ICON_NO_ACTIVITY = "🔵"
ICON_FEW_ACTIVITY = "🟡"
ICON_LOTS_ACTIVITY = "🔴"

# Error messages
ERROR_NO_TOKEN = "GitHub token not found in environment"
ERROR_API_FAILURE = "Failed to connect to GitHub API"

# Logging setup
logging.basicConfig(
    level=logging.DEBUG if os.getenv("DEBUG") else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


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


def get_github_token() -> Optional[str]:
    return os.getenv(GITHUB_TOKEN_ENV)


def is_xbar_environment() -> bool:
    # xbar sets SWIFTBAR environment variable
    return "SWIFTBAR" in os.environ or "BITBAR" in os.environ


def output_xbar_widget():
    token = get_github_token()
    if not token:
        print(f"{ICON_LOTS_ACTIVITY} Error")
        print("---")
        print(ERROR_NO_TOKEN)
        return
    
    # TODO: Implement actual GitHub data fetching
    print(f"{ICON_NO_ACTIVITY} GitHub")
    print("---")
    print("No activity")


@click.command()
@click.option('--debug', is_flag=True, help='Enable debug logging')
def cli(debug: bool):
    """GitHub Activity Monitor - Command Line Interface."""
    if debug:
        logger.setLevel(logging.DEBUG)
    
    token = get_github_token()
    if not token:
        click.echo(f"Error: {ERROR_NO_TOKEN}", err=True)
        click.echo("Set the GITHUB_TOKEN environment variable with your GitHub personal access token.")
        sys.exit(1)
    
    # TODO: Implement actual GitHub data fetching
    click.echo("GitHub Activity Monitor")
    click.echo("=" * 50)
    click.echo("No activity to display")


def main() -> None:
    if is_xbar_environment():
        output_xbar_widget()
    else:
        cli()


if __name__ == "__main__":
    main()
