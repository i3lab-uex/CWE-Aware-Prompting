#!/usr/bin/env python3
"""
Utility to validate RSS feed URLs against a whitelist of trusted providers.
"""

from urllib.parse import urlparse, ParseResult
import re

# List of approved hostnames (case‑insensitive). Extend as needed.
TRUSTED_HOSTNAMES = {
    "rss.nytimes.com",
    "news.google.com",
    "feeds.bbci.co.uk",
    "rss.cnn.com",
    "feeds.reuters.com",
    "xml.slashdot.org",          # example of a public RSS source
}

# Regular expression to detect IP addresses (IPv4 or IPv6)
IP_RE = re.compile(
    r"""
    ^
    (?:
        # IPv4
        (?:\d{1,3}\.){3}\d{1,3}
        |
        # IPv6
        \[
            (?:
                [0-9a-fA-F]{1,4}
                (:[0-9a-fA-F]{1,4}){7}
            |
                ::[0-9a-fA-F]{1,4}(:[0-9a-fA-F]{1,4}){0,5}
            |
                [0-9a-fA-F]{1,4}::([0-9a-fA-F]{1,4}:){0,4}[0-9a-fA-F]{1,4}
            |
                [0-9a-fA-F]{1,4}(:[0-9a-fA-F]{1,4}){0,5}:
            |
                ::[0-9a-fA-F]{1,4}(:[0-9a-fA-F]{1,4}){0,3}
            |
                ::[0-9a-fA-F]{1,4}(:[0-9a-fA-F]{1,4}){0,2}
            |
                ::[0-9a-fA-F]{1,4}(:[0-9a-fA-F]{1,4})?
            |
                ::[0-9a-fA-F]{1,4}
            |
                :: 
            )
        \]
    )
    $
    """,
    re.VERBOSE,
)


def _is_ip_address(hostname: str) -> bool:
    """Return True if the hostname looks like an IP address."""
    return bool(IP_RE.match(hostname))


def check_rss_address(rss_address: str) -> str:
    """
    Validate that an RSS feed URL points to a trusted provider.

    Parameters
    ----------
    rss_address : str
        The raw URL supplied by the caller.

    Returns
    -------
    str
        The sanitized URL that has been validated to point to an approved provider.

    Raises
    ------
    ValueError
        If the URL uses an unsupported scheme, points to a non‑trusted host,
        or resolves to an IP address (including localhost).
    """
    if not isinstance(rss_address, str):
        raise ValueError("RSS address must be a string")

    # Parse the URL
    parsed: ParseResult = urlparse(rss_address.strip())

    # Enforce https or http only
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http/https allowed.")

    # Reject empty hostname
    if not parsed.hostname:
        raise ValueError("URL must contain a valid hostname")

    # Reject IP addresses or localhost
    hostname_lower = parsed.hostname.lower()
    if _is_ip_address(hostname_lower) or hostname_lower in {"127.0.0.1", "localhost"}:
        raise ValueError("IP addresses or localhost are not allowed for RSS feeds")

    # Validate against the whitelist (case‑insensitive)
    if hostname_lower not in TRUSTED_HOSTNAMES:
        raise ValueError(f"Hostname '{parsed.hostname}' is not an approved RSS provider")

    # Reconstruct the URL to ensure no fragments or query parameters are added
    sanitized = parsed._replace(fragment="", query="").geturl()
    return sanitized


# Example usage (uncomment for quick test)
# if __name__ == "__main__":
#     try:
#         url = "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"
#         print("Validated URL:", check_rss_address(url))
#     except ValueError as e:
#         print("Validation error:", e)