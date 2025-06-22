#!/usr/bin/env python3

import pytest
from unittest.mock import Mock, patch
from activity_aggregator import ActivityData, fetch_all_activity


class TestActivityData:
    def test_total_count(self):
        activity = ActivityData(
            pull_requests=["pr1", "pr2"],
            issues=["issue1"],
            notifications=["notif1", "notif2", "notif3"]
        )
        
        assert activity.total_count == 6
    
    def test_activity_level_none(self):
        activity = ActivityData(
            pull_requests=[],
            issues=[],
            notifications=[]
        )
        assert activity.activity_level == "none"
    
    def test_activity_level_low(self):
        # Test with 1 item
        activity = ActivityData(
            pull_requests=["pr1"],
            issues=[],
            notifications=[]
        )
        assert activity.activity_level == "low"
        
        # Test with 5 items
        activity = ActivityData(
            pull_requests=["pr1", "pr2"],
            issues=["issue1", "issue2"],
            notifications=["notif1"]
        )
        assert activity.activity_level == "low"
    
    def test_activity_level_high(self):
        # Test with 6 items
        activity = ActivityData(
            pull_requests=["pr1", "pr2"],
            issues=["issue1", "issue2"],
            notifications=["notif1", "notif2"]
        )
        assert activity.activity_level == "high"


class TestFetchAllActivity:
    @patch('activity_aggregator.fetch_notifications')
    @patch('activity_aggregator.fetch_issues')
    @patch('activity_aggregator.fetch_pull_requests')
    def test_fetch_all_activity(self, mock_fetch_prs, mock_fetch_issues, mock_fetch_notifications):
        # Setup stubs to return test data
        mock_fetch_prs.return_value = ["pr1", "pr2"]
        mock_fetch_issues.return_value = ["issue1"]
        mock_fetch_notifications.return_value = ["notif1", "notif2", "notif3"]
        
        # Fetch all activity
        result = fetch_all_activity(Mock())
        
        # Verify the aggregated result
        assert result.pull_requests == ["pr1", "pr2"]
        assert result.issues == ["issue1"]
        assert result.notifications == ["notif1", "notif2", "notif3"]
        assert result.total_count == 6
        assert result.activity_level == "high"