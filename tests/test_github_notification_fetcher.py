#!/usr/bin/env python3

import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import Mock, call
from github_notification_fetcher import fetch_notifications


class TestFetchNotifications:
    def test_fetch_notifications_filters_mentions_only(self):
        # Mock GitHub client
        client = Mock()
        user = Mock()
        client.get_user.return_value = user
        
        # Create mock notifications with different reasons
        mention_notification = Mock()
        mention_notification.reason = "mention"
        
        review_notification = Mock()
        review_notification.reason = "review_requested"
        
        assign_notification = Mock()
        assign_notification.reason = "assign"
        
        user.get_notifications.return_value = [
            mention_notification,
            review_notification,
            assign_notification
        ]
        
        # Fetch notifications
        notifications = fetch_notifications(client)
        
        # Should only include the mention notification
        assert len(notifications) == 1
        assert notifications[0].reason == "mention"
    
    def test_fetch_notifications_uses_24_hour_window(self):
        # Mock GitHub client
        client = Mock()
        user = Mock()
        client.get_user.return_value = user
        user.get_notifications.return_value = []
        
        # Fetch notifications
        fetch_notifications(client)
        
        # Verify the call was made with correct parameters
        assert user.get_notifications.called
        call_args = user.get_notifications.call_args
        
        # Check that 'since' parameter is approximately 24 hours ago
        since_param = call_args[1]['since']
        now = datetime.now(timezone.utc)
        time_diff = now - since_param
        
        # Allow 1 second tolerance for test execution time
        assert timedelta(hours=23, minutes=59, seconds=59) <= time_diff <= timedelta(hours=24, seconds=1)
    
    def test_fetch_notifications_preserves_unread_state(self):
        # Mock GitHub client
        client = Mock()
        user = Mock()
        client.get_user.return_value = user
        user.get_notifications.return_value = []
        
        # Fetch notifications
        fetch_notifications(client)
        
        # Verify the call was made with participating=False
        call_args = user.get_notifications.call_args
        assert call_args[1]['participating'] is False
        assert call_args[1]['all'] is False  # Only unread