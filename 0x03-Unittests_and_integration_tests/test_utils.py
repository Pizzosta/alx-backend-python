#!/usr/bin/env python3
"""A module for testing the utils module."""
import unittest
from typing import Any, Dict, Tuple
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Tests the utils.access_nested_map function"""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(
        self,
        nested_map: Dict[str, Any],
        path: Tuple[str, ...],
        expected_result: Any
    ) -> None:
        """Tests the utils.access_nested_map function output"""
        self.assertEqual(access_nested_map(nested_map, path), expected_result)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError)
    ])
    def test_access_nested_map_exception(
        self,
        nested_map: Dict[str, Any],
        path: Tuple[str, ...],
        expected_exception: Exception
    ) -> None:
        """Tests the utils.access_nested_map function raising exception"""
        with self.assertRaises(expected_exception):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Tests the utils.get_json function."""
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")
    def test_get_json(
            self,
            test_url: str,
            test_payload: Dict,
            mock_get: Mock,
    ) -> None:
        """Tests the utils.get_json function output."""
        attrs = {'json.return_value': test_payload}
        mock_get.return_value = Mock(**attrs)

        result = get_json(test_url)

        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Tests the utils.memoize function."""

    def test_memoize(self) -> None:
        """Tests the utils.memoize function output."""
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(
            TestClass,
            "a_method",
            return_value=lambda: 42
        ) as mock_method:
            test_class = TestClass()

            result1 = test_class.a_property()
            result2 = test_class.a_property()

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()
