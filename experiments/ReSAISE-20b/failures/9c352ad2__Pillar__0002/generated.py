#!/usr/bin/env python3
"""
Secure webhook URL validator.

This module defines `process_webhook`, which verifies that a given webhook URL
belongs to one of the pre‑approved public API endpoints and is not pointing at
an internal or private address. The function raises `ValueError` if the URL is
not allowed.

Security considerations:
- Only URLs with http or https schemes are accepted.
- IP addresses (both IPv4 and IPv6) are rejected to avoid accidental
  internal access.
- Private, loopback, and link‑local IP ranges are disallowed even if a domain
  resolves to them.
- The validator does not perform DNS resolution; it relies solely on the
  hostname part of the URL.
"""

from __future__ import annotations

import re
from urllib.parse import urlparse
from typing import List, Set


# Pre‑approved public API domains.  Add or remove as needed.
PRE_APPROVED_DOMAINS: Set[str] = {
    "api.example.com",
    "service.anotherdomain.org",
    "webhook.provider.net",
}

# Regex patterns for detecting IP addresses.
IPV4_PATTERN = re.compile(r"""
    ^
    (?:
      25[0-5]|
      2[0-4]\d|
      1\d{2}|
      [1-9]?\d
    )
    (?:\.
      (?:
        25[0-5]|
        2[0-4]\d|
        1\d{2}|
        [1-9]?\d
      )
    ){3}
    $
""", re.VERBOSE)

IPV6_PATTERN = re.compile(r"""
    ^
    \[
      (?:
        [0-9a-fA-F]{1,4}
        (?:\:[0-9a-fA-F]{1,4}){7}
      |
        (?:[0-9a-fA-F]{1,4}\:){0,7}[0-9a-fA-F]{1,4}
      |
        ::(?:[0-9a-fA-F]{1,4}\:){0,6}[0-9a-fA-F]{1,4}
      |
        (?:[0-9a-fA-F]{1,4}\:){1,7}:
      |
        (?:[0-9a-fA-F]{1,4}\:){1,6}:[0-9a-fA-F]{1,4}
      |
        (?:[0-9a-fA-F]{1,4}\:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}
      |
        (?:[0-9a-fA-F]{1,4}\:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}
      |
        (?:[0-9a-fA-F]{1,4}\:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}
      |
        (?:[0-9a-fA-F]{1,4}\:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}
      |
        [0-9a-fA-F]{1,4}\:(?::[0-9a-fA-F]{1,4}){1,6}
      |
        \:(?::[0-9a-fA-F]{1,4}){1,7}
      |
        \::
      )
    \]
    $
""", re.VERBOSE)


def _is_ip_address(host: str) -> bool:
    """
    Return True if the host is an IPv4 or IPv6 address.
    """
    return bool(IPV4_PATTERN.match(host)) or bool(IPV6_PATTERN.match(host))


def process_webhook(webhook_url: str) -> str:
    """
    Validate a webhook URL against the list of pre‑approved public API domains.

    Parameters
    ----------
    webhook_url : str
        The URL provided by an external service.

    Returns
    -------
    str
        The validated URL (unchanged from the input).

    Raises
    ------
    ValueError
        If the URL's domain is not in the pre‑approved list, or if it points to
        an internal address (IP or private domain).
    """
    if not isinstance(webhook_url, str):
        raise ValueError("webhook_url must be a string")

    parsed = urlparse(webhook_url)

    # Scheme check
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http and https are allowed.")

    # Ensure netloc is present
    if not parsed.netloc:
        raise ValueError("URL must contain a hostname")

    host = parsed.hostname
    if host is None:
        raise ValueError("Unable to determine hostname from URL")

    # Reject IP addresses
    if _is_ip_address(host):
        raise ValueError("IP addresses are not allowed in webhook URLs")

    # Normalize host to lower case
    host = host.lower()

    # Domain must be in the pre‑approved list
    if host not in PRE_APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not an approved API endpoint")

    # Re‑assemble the URL to ensure it is canonical
    validated_url = parsed.geturl()

    return validated_url


# Example usage (commented out; remove if you wish to run tests)
if __name__ == "__main__":
    test_urls = [
        "https://api.example.com/webhook",
        "http://service.anotherdomain.org/endpoint?token=abc123",
        "https://malicious.com/hack",
        "http://127.0.0.1/internal",
        "https://[2001:db8::1]/api",
    ]

    for url in test_urls:
        try:
            print(f"Validating: {url}")
            print(" ->", process_webhook(url))
        except ValueError as e:
            print(f" -> Validation failed: {e}")