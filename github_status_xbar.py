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

import click

from github_auth import get_authenticated_client

# Configuration constants
REFRESH_INTERVAL = 30  # seconds (managed by xbar filename)
NOTIFICATION_WINDOW = 24  # hours
ACTIVITY_THRESHOLD_FEW = 5
ACTIVITY_THRESHOLD_LOTS = 6


# Display constants
ICON_NO_ACTIVITY = "🔵"
ICON_FEW_ACTIVITY = "🟡"
ICON_LOTS_ACTIVITY = "🔴"


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



def is_xbar_environment() -> bool:
    # xbar sets SWIFTBAR environment variable
    return "SWIFTBAR" in os.environ or "BITBAR" in os.environ


def output_xbar_widget():
    try:
        get_authenticated_client()  # Verify authentication works
        # TODO: Implement actual GitHub data fetching
        print(f"{ICON_NO_ACTIVITY} GitHub")
        print("---")
        print("No activity")
    except Exception as e:
        print(f"{ICON_LOTS_ACTIVITY} Error")
        print("---")
        print(f"Error: {str(e)}")


@click.command()
@click.option('--debug', is_flag=True, help='Enable debug logging')
def cli(debug: bool):
    """GitHub Activity Monitor - Command Line Interface."""
    if debug:
        logger.setLevel(logging.DEBUG)
    
    try:
        get_authenticated_client()  # Verify authentication works
        # TODO: Implement actual GitHub data fetching
        click.echo("GitHub Activity Monitor")
        click.echo("=" * 50)
        click.echo("No activity to display")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        if debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def main() -> None:
    if is_xbar_environment():
        output_xbar_widget()
    else:
        cli()


if __name__ == "__main__":
    main()
