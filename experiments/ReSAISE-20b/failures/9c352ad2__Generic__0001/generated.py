#!/usr/bin/env python3
"""
Utility to validate webhook URLs against a list of pre‑approved public API endpoints.
"""

from urllib.parse import urlparse
import re

# --------------------------------------------------------------------------- #
# Configuration: pre‑approved domains (add or remove as needed)
# --------------------------------------------------------------------------- #
PRE_APPROVED_DOMAINS = {
    "api.example.com",
    "service.internal.company",
    "public.api.org",
}

# Regular expression to detect private IP ranges and localhost
_PRIVATE_IP_REGEX = re.compile(
    r"^(?:"
    r"10(?:\.\d{1,3}){3}|"
    r"127(?:\.\d{1,3}){3}|"
    r"169\.254(?:\.\d{1,3}){2}|"
    r"172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2}|"
    r"192\.168(?:\.\d{1,3}){2}"
    r")$"
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is a private or loopback address."""
    return _PRIVATE_IP_REGEX.match(ip) is not None


def process_webhook(webhook_url: str) -> str:
    """
    Validate a webhook URL and ensure it points to an approved public API endpoint.

    Parameters
    ----------
    webhook_url : str
        The URL provided by an external service.

    Returns
    -------
    str
        The validated webhook URL (unchanged).

    Raises
    ------
    ValueError
        If the URL's domain is not in the list of pre‑approved endpoints,
        if it points to a private/internal address, or if the scheme is not
        HTTP/HTTPS.
    """
    # Parse URL components
    parsed = urlparse(webhook_url)
    if not parsed.scheme or parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    netloc = parsed.netloc
    if not netloc:
        raise ValueError("URL must contain a network location (domain or IP)")

    # Split host and optional port
    if ":" in netloc:
        host, _ = netloc.split(":", 1)
    else:
        host = netloc

    # Reject explicit IP addresses that are private or internal
    if re.match(r"^\d{1,3}(?:\.\d{1,3}){3}$", host):
        if _is_private_ip(host):
            raise ValueError(f"URL points to a private IP address: {host!r}")

    # Reject localhost and loopback names
    if host.lower() in {"localhost", "127.0.0.1"}:
        raise ValueError("URL cannot point to localhost or loopback address")

    # Check against pre-approved domains
    if host.lower() not in {d.lower() for d in PRE_APPROVED_DOMAINS}:
        raise ValueError(f"Domain {host!r} is not in the list of approved endpoints")

    # All checks passed – return the original URL
    return webhook_url


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    test_urls = [
        "https://api.example.com/notify",
        "http://service.internal.company/api/v1/webhook",
        "https://malicious.com/endpoint",
        "http://127.0.0.1/api/test",
    ]

    for url in test_urls:
        try:
            print(f"Validating {url} ->", process_webhook(url))
        except ValueError as exc:
            print(f"Validation failed for {url}: {exc}")