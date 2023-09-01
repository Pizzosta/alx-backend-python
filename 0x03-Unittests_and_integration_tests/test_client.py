#!/usr/bin/env python3
"""A module for testing client.GithubOrgClient"""
import unittest
from typing import Dict
from unittest.mock import patch, MagicMock, PropertyMock, Mock
from fixtures import TEST_PAYLOAD
from parameterized import parameterized, parameterized_class
from requests import HTTPError
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

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected_result):
        """Tests the has_license method with parameterization."""
        github_client = GithubOrgClient("google")
        result = github_client.has_license(repo, license_key)
        self.assertEqual(result, expected_result)


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Performs integration tests for the `GithubOrgClient` class."""

    @classmethod
    def setUpClass(cls) -> None:
        """Sets up class fixtures before running tests."""
        route_payload = {
            'https://api.github.com/orgs/google': cls.org_payload,
            'https://api.github.com/orgs/google/repos': cls.repos_payload,
        }

        def get_payload(url):
            if url in route_payload:
                return Mock(**{'json.return_value': route_payload[url]})
            return HTTPError

        cls.get_patcher = patch("requests.get", side_effect=get_payload)
        cls.get_patcher.start()

    def test_public_repos(self) -> None:
        """Tests the `public_repos` method."""
        self.assertEqual(
            GithubOrgClient("google").public_repos(),
            self.expected_repos,
        )

    def test_public_repos_with_license(self) -> None:
        """Tests the `public_repos` method with a license."""
        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """Removes the class fixtures after running all tests."""
        cls.get_patcher.stop()


if __name__ == '__main__':
    unittest.main()
