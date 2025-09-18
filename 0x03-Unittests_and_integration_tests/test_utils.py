#!/usr/bin/env python3
"""
Unit tests for utils.py
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import get_json, memoize


class TestGetJson(unittest.TestCase):
    """Test case for the get_json function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """Test that utils.get_json returns the expected result."""
        mock_response = Mock()
        mock_response.json.return_value = test_payload

        with patch("utils.requests.get", return_value=mock_response) as mock_get:
            result = get_json(test_url)

            # Check that requests.get was called exactly once with test_url
            mock_get.assert_called_once_with(test_url)
            # Check that the result is equal to test_payload
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test case for the memoize decorator."""

    def test_memoize(self):
        """Test that memoize caches the result of a method."""

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            obj = TestClass()

            # Call twice
            first = obj.a_property
            second = obj.a_property

            # Both should return the same result
            self.assertEqual(first, 42)
            self.assertEqual(second, 42)

            # a_method should only be called once due to memoization
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
