#!/usr/bin/env python3
"""
Utility to validate HTTP/HTTPS paths.

The function uses a compiled regular expression with a fixed pattern,
avoiding back‑tracking pitfalls and ensuring efficient matching
even for maliciously crafted inputs.
"""

import re

# Pre‑compile a safe, non‑backtracking regex for HTTP/HTTPS URLs.
# This pattern accepts any non‑whitespace characters after the scheme,
# which covers typical paths, queries and fragments.
_URL_REGEX = re.compile(
    r"^https?://[^\s]+$",  # http or https, followed by :// and non‑whitespace
    flags=re.ASCII | re.IGNORECASE,
)

def check_path(input_path: str) -> bool:
    """
    Determine if `input_path` is a valid HTTP or HTTPS URL.

    Parameters
    ----------
    input_path : str
        The string to evaluate as a potential URL.

    Returns
    -------
    bool
        True if `input_path` matches the HTTP/HTTPS URL pattern,
        False otherwise.

    Notes
    -----
    - The function never raises exceptions; it safely handles
      malformed inputs by returning False.
    - Uses a pre‑compiled regex to avoid repeated compilation overhead
      and to mitigate potential denial‑of‑service attacks via
      catastrophic backtracking (CWE-407).
    """
    if not isinstance(input_path, str):
        # Non‑string inputs are automatically considered invalid.
        return False

    # Use fullmatch to ensure the entire string conforms to the pattern.
    match = _URL_REGEX.fullmatch(input_path)
    return bool(match)

# Example usage (uncomment to test):
# if __name__ == "__main__":
#     tests = [
#         "http://example.com/path",
#         "https://sub.domain.co.uk?query=1",
#         "ftp://example.com",  # invalid scheme
#         "http:///missinghost",
#         "https:// example.com",  # contains space
#     ]
#     for t in tests:
#         print(t, "->", check_path(t))