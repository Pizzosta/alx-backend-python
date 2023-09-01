#!/usr/bin/env python3
"""A module for testing client.GithubOrgClient"""
import unittest
from typing import Dict
from unittest.mock import patch, MagicMock, PropertyMock
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

    @patch('client.GithubOrgClient._public_repos_url',
           new_callable=PropertyMock)
    @patch('client.GithubOrgClient.org')
    def test_public_repos_url(self, mock_org, mock_public_repos_url):
        """Tests the _public_repos_url property."""
        mock_org.return_value = {
            'repos_url': "https://api.github.com/users/google/repos",
        }
        mock_public_repos_url.return_value = \
            "https://api.github.com/users/google/repos"
        github_client = GithubOrgClient("google")
        self.assertEqual(
            github_client._public_repos_url,
            "https://api.github.com/users/google/repos",
        )


if __name__ == '__main__':
    unittest.main()
