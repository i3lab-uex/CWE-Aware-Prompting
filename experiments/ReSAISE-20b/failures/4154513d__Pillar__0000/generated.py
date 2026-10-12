#!/usr/bin/env python3
"""
Utilities for building an SSO redirect URL.

The implementation guards against open‑redirect attacks by validating that
the supplied `redirect_url` points to one of the allowed domains.  It also
ensures that all query parameters are properly percent‑encoded and that the
final URL is correctly assembled even when the base `auth_endpoint`
already contains query parameters.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import urllib.parse
from typing import Set, Iterable


# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# The set of domains that are permitted as a return target.
ALLOWED_RETURN_DOMAINS: Set[str] = {
    "example.com",
    "myapp.example.org",
    # Add more domains as needed
}


# --------------------------------------------------------------------------- #
# Helper Functions
# --------------------------------------------------------------------------- #

def _extract_domain(url: str) -> str:
    """
    Extract the domain part (netloc) from a URL.

    Args:
        url: The URL to parse.

    Returns:
        The domain string (lower‑cased, without port).

    Raises:
        ValueError: If the URL does not contain a netloc.
    """
    parsed = urllib.parse.urlparse(url)
    if not parsed.netloc:
        raise ValueError(f"Redirect URL '{url}' is missing a domain")
    # Strip port if present
    domain = parsed.hostname or ""
    return domain.lower()


def _is_allowed_domain(domain: str, allowed_domains: Iterable[str]) -> bool:
    """
    Check whether the given domain is in the list of allowed domains.

    Args:
        domain: The domain to check.
        allowed_domains: An iterable of allowed domain strings.

    Returns:
        True if the domain is allowed, False otherwise.
    """
    return domain in (d.lower() for d in allowed_domains)


# --------------------------------------------------------------------------- #
# Main Function
# --------------------------------------------------------------------------- #

def build_sso_redirect(auth_endpoint: str, uid: str, redirect_url: str) -> str:
    """
    Build a secure SSO redirect URL.

    The function validates that the `redirect_url` points to an allowed
    domain, then constructs a URL pointing at the SSO service with the user
    ID and return URL as query parameters.

    Args:
        auth_endpoint: The base SSO service endpoint (e.g., "https://sso.example.com/auth").
        uid: The unique identifier for the user.
        redirect_url: The URL to return to after authentication.

    Returns:
        A fully constructed, percent‑encoded redirect URL.

    Raises:
        ValueError: If the return URL's domain is not in ALLOWED_RETURN_DOMAINS.
    """
    # Validate that the redirect URL points to an allowed domain
    domain = _extract_domain(redirect_url)
    if not _is_allowed_domain(domain, ALLOWED_RETURN_DOMAINS):
        raise ValueError(
            f"Return URL domain '{domain}' is not in the list of allowed domains"
        )

    # Parse the auth endpoint to handle existing query parameters
    parsed_auth = urllib.parse.urlparse(auth_endpoint)

    # Build the new query string, preserving any existing params
    existing_params = urllib.parse.parse_qs(parsed_auth.query, keep_blank_values=True)
    # parse_qs returns values as lists; convert to single values for our case
    existing_params = {k: v[0] if len(v) == 1 else v for k, v in existing_params.items()}

    # Add/override with SSO-specific parameters
    new_params = {
        **existing_params,
        "uid": uid,
        "redirect_url": redirect_url,  # will be encoded by urlencode
    }

    # Construct the final URL
    new_query = urllib.parse.urlencode(new_params, doseq=True)
    built_url_parts = parsed_auth._replace(query=new_query)
    final_url = urllib.parse.urlunparse(built_url_parts)

    return final_url


# --------------------------------------------------------------------------- #
# Example Usage (remove or comment out in production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Example configuration
    example_auth_endpoint = "https://sso.example.com/auth"
    example_uid = "user-12345"
    example_redirect = "https://myapp.example.org/dashboard"

    try:
        redirect = build_sso_redirect(example_auth_endpoint, example_uid, example_redirect)
        print("Redirect URL:", redirect)
    except ValueError as e:
        print("Validation error:", e)