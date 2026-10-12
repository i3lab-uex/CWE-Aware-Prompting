#!/usr/bin/env python3
"""
Secure image URL checker.

This module provides a single function `check_image_link` that validates an
image URL against a whitelist of trusted image hosting domains.  It ensures
that the scheme is either http or https and that the hostname matches one of
the allowed domains.  If validation fails, a ValueError is raised.

The implementation follows the recommendations for preventing SSRF
(CWE‑918) by performing all checks locally before any network access.
"""

import re
from urllib.parse import urlparse

# --------------------------------------------------------------------------- #
# Configuration: list of trusted domains.
#
# The list can be extended with additional subdomains or new hosts as needed.
# Use a regular expression to allow optional subdomains (e.g. `*.imgur.com`).
TRUSTED_DOMAIN_PATTERNS = [
    r"^(?:.*\.)?imgur\.com$",
    r"^(?:.*\.)?flickr\.com$",
    r"^(?:.*\.)?tinypic\.com$",
    r"^(?:.*\.)?i\.imgur\.com$",  # direct Imgur image host
    r"^(?:.*\.)?cdn\.example\.com$",  # internal CDN example
]

# Compile regexes once for performance.
_TRUSTED_DOMAIN_REGEXES = [re.compile(p, re.IGNORECASE) for p in TRUSTED_DOMAIN_PATTERNS]


def _is_trusted_domain(hostname: str) -> bool:
    """
    Return True if the hostname matches one of the trusted domain patterns.
    """
    for regex in _TRUSTED_DOMAIN_REGEXES:
        if regex.match(hostname):
            return True
    return False


def check_image_link(image_link: str) -> str:
    """
    Validate an image URL against a whitelist of trusted domains.

    Parameters
    ----------
    image_link : str
        The URL to validate.

    Returns
    -------
    str
        The original URL if it passes validation.

    Raises
    ------
    ValueError
        If the scheme is not http/https or if the domain is not trusted.
    """
    # Parse the URL and normalise it
    parsed = urlparse(image_link)

    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http and https are allowed.")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname.")

    # Reject IP addresses to avoid accidental local or private network access
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", hostname):
        raise ValueError("IP addresses are not allowed as image hosts.")

    # Verify the domain is in our whitelist
    if not _is_trusted_domain(hostname):
        raise ValueError(f"Domain '{hostname}' is not trusted.")

    # All checks passed – return the original URL unchanged
    return image_link


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
#
# if __name__ == "__main__":
#     try:
#         print(check_image_link("https://i.imgur.com/example.png"))
#         print(check_image_link("http://malicious.example.com/evil.jpg"))  # should raise
#     except ValueError as e:
#         print(f"Validation failed: {e}")