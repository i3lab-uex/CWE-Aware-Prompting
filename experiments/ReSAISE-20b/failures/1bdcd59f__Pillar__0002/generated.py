#!/usr/bin/env python3
"""
Utility module to validate HTTP/HTTPS URLs.
"""

import re

# Regular expression that matches a minimal but reasonable
# representation of an HTTP or HTTPS URL.
#
# The pattern ensures:
#   * Scheme is http or https
#   * Followed by ://
#   * A non‑empty host part (at least one character, not a space)
#   * Optional port, path, query and fragment components
#
# This is intentionally permissive enough for common use cases while
# avoiding overly strict validation that could reject valid URLs.
_URL_RE = re.compile(
    r"""^
    https?://                           # http or https scheme
    (?:
        [^\s:/?#]+                      # host (no spaces, slashes, etc.)
        (?::\d+)?                       # optional port
    )
    (?:[/?#][^\s]*)?                    # optional path/query/fragment
    $""",
    re.IGNORECASE | re.VERBOSE,
)


def path_check(u: str) -> bool:
    """
    Return True if *u* is a valid HTTP or HTTPS URL, otherwise False.

    The function never raises an exception; any error in the regular
    expression matching is caught and treated as a non‑match.

    Parameters:
        u (str): The string to validate.

    Returns:
        bool: True if *u* matches the URL pattern, False otherwise.
    """
    try:
        return bool(_URL_RE.match(u))
    except Exception:  # pragma: no cover
        # In the unlikely event that re.match raises an exception,
        # treat the input as invalid rather than propagating.
        return False