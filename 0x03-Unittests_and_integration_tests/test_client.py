#!/usr/bin/env python3
"""A module for testing client.GithubOrgClient"""
import unittest
from typing import Dict
from unittest.mock import patch, MagicMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests the GithubOrgClient class."""

    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"}),
    ])
    @patch('client.get_json')
    def test_org(
        self,
        org_name: str,
        expected_result: Dict,
        mock_get_json: MagicMock
    ) -> None:
        """Tests the GithubOrgClient.org method."""

        mock_get_json.return_value = MagicMock(return_value=expected_result)

        github_client = GithubOrgClient(org_name)

        org_info = github_client.org()

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}")

        self.assertEqual(org_info, expected_result)


if __name__ == '__main__':
    unittest.main()
