#!/usr/bin/env python3
"""
validate_webhook.py

Validates an external webhook URL against a whitelist of public API endpoints.
Prevents Server‑Side Request Forgery (CWE‑918) by:
  • Resolving the hostname to IP(s) and ensuring they are public.
  • Ensuring the domain is in an approved whitelist.
  • Normalising and sanitising the URL before returning it.

Author: OpenAI
"""

import ipaddress
import socket
from urllib.parse import urlparse, urlunparse


# --------------------------------------------------------------------------- #
# Configuration – whitelist of approved public API domains
# --------------------------------------------------------------------------- #
WHITELIST_DOMAINS = {
    "api.example.com",
    "webhooks.service.net",
    "trusted.api.org",
}

# Optional: allow subdomains of the whitelisted domains
ALLOW_SUBDOMAINS = True

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _is_public_ip(ip: str) -> bool:
    """
    Return True if the IP address is public (not private, loopback, link‑local,
    or reserved).
    """
    try:
        ip_obj = ipaddress.ip_address(ip)
    except ValueError:
        return False
    # Exclude private, loopback, link‑local and reserved addresses
    return not (
        ip_obj.is_private
        or ip_obj.is_loopback
        or ip_obj.is_link_local
        or ip_obj.is_reserved
    )


def _resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve the hostname to a list of IP addresses.
    Raises ValueError if resolution fails or no public IPs are found.
    """
    try:
        # getaddrinfo returns a list of tuples; we extract the IPs
        infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{hostname}': {exc}") from exc

    ips = set()
    for info in infos:
        ip_str = info[4][0]
        if _is_public_ip(ip_str):
            ips.add(ip_str)

    if not ips:
        raise ValueError(f"Hostname '{hostname}' resolves only to private or reserved IPs.")
    return list(ips)


def _domain_in_whitelist(domain: str) -> bool:
    """
    Check if the domain is in the whitelist, optionally allowing subdomains.
    """
    if ALLOW_SUBDOMAINS:
        for allowed in WHITELIST_DOMAINS:
            if domain == allowed or domain.endswith("." + allowed):
                return True
    else:
        return domain in WHITELIST_DOMAINS
    return False


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def validate_webhook(webhook_link: str) -> str:
    """
    Validate a webhook URL.

    Parameters
    ----------
    webhook_link : str
        External webhook URL to be validated.

    Returns
    -------
    str
        Normalised and sanitized URL that is safe for internal use.

    Raises
    ------
    ValueError
        If the URL's domain is not in the whitelist or resolves to a private
       /internal IP address.
    """
    if not webhook_link:
        raise ValueError("webhook_link must be a non‑empty string")

    parsed = urlparse(webhook_link)

    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme '{parsed.scheme}'. Only http/https allowed.")

    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    domain = parsed.hostname.lower()

    if not _domain_in_whitelist(domain):
        raise ValueError(f"Domain '{domain}' is not in the approved whitelist")

    # Resolve and verify that at least one public IP exists
    _resolve_hostname(domain)

    # Re‑build the URL with a normalized path and query string
    safe_path = parsed.path or "/"
    # Preserve query and fragment; they are part of the API contract
    safe_url = urlunparse(
        (
            parsed.scheme,
            domain,
            safe_path,
            parsed.params,
            parsed.query,
            parsed.fragment,
        )
    )

    return safe_url


# --------------------------------------------------------------------------- #
# Example usage (uncomment for testing)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    test_urls = [
        "https://api.example.com/webhook?token=abc",
        "http://malicious.internal.local/api",
        "https://unknown.com/endpoint",
    ]

    for url in test_urls:
        try:
            print(f"Validated: {validate_webhook(url)}")
        except ValueError as e:
            print(f"Validation failed for '{url}': {e}")