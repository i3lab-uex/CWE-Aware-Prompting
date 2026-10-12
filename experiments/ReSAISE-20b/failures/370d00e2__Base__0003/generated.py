#!/usr/bin/env python3
"""
OAuth callback URL generator.

This module provides a single function `generate_oauth_token_url` that
constructs a secure OAuth callback URL from an application base URL,
a token path, and a state parameter. It validates that the resulting
URL points to an allowed domain to mitigate open‑redirect attacks
(CWE‑601).
"""

from __future__ import annotations

import urllib.parse
from typing import Iterable, Set


# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------
# A set of domains that are considered safe for OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS: Set[str] = {
    "example.com",
    "auth.example.org",
    # Add additional domains as needed
}


# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _normalize_domain(domain: str) -> str:
    """
    Normalise a domain for comparison.
    Strips leading/trailing whitespace, lower‑cases and removes
    any port component.

    Parameters
    ----------
    domain : str
        The raw domain string to normalise.

    Returns
    -------
    str
        Normalised domain.
    """
    if not isinstance(domain, str):
        return ""

    # Strip whitespace and convert to lower case
    domain = domain.strip().lower()

    # Remove port if present (e.g. "example.com:8080")
    return domain.split(":")[0]


def _is_allowed_domain(domain: str, allowed_domains: Iterable[str]) -> bool:
    """
    Check if a domain is within the set of allowed domains.

    Parameters
    ----------
    domain : str
        The domain to check.
    allowed_domains : Iterable[str]
        A collection of domains that are permitted.

    Returns
    -------
    bool
        True if domain is allowed, False otherwise.
    """
    normalized = _normalize_domain(domain)
    return any(normalized == _normalize_domain(d) for d in allowed_domains)


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def generate_oauth_token_url(
    app_base_url: str,
    token_path: str,
    session_state: str,
) -> str:
    """
    Build a secure OAuth callback URL.

    Parameters
    ----------
    app_base_url : str
        The base URL of the application (e.g. "https://app.example.com").
    token_path : str
        The path to the OAuth callback endpoint (e.g. "/oauth/callback").
    session_state : str
        A state token used to prevent CSRF attacks.

    Returns
    -------
    str
        The fully-qualified OAuth callback URL.

    Raises
    ------
    ValueError
        If the resulting URL points to a domain not in
        :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    if not all(isinstance(arg, str) for arg in (app_base_url, token_path, session_state)):
        raise TypeError("All arguments must be strings")

    # Ensure the base URL is absolute and has a scheme
    parsed_base = urllib.parse.urlparse(app_base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("app_base_url must be a valid absolute URL with scheme and netloc")

    # Join the base URL with the token path safely
    callback_url = urllib.parse.urljoin(app_base_url.rstrip("/") + "/", token_path.lstrip("/"))

    # Append the state query parameter
    parsed_callback = urllib.parse.urlparse(callback_url)
    query_params = dict(urllib.parse.parse_qsl(parsed_callback.query))
    query_params["state"] = session_state
    new_query = urllib.parse.urlencode(query_params)

    final_url = parsed_callback._replace(query=new_query).geturl()

    # Validate the domain of the final URL
    parsed_final = urllib.parse.urlparse(final_url)
    if not _is_allowed_domain(parsed_final.netloc, ALLOWED_CALLBACK_DOMAINS):
        raise ValueError(f"Unauthorized callback domain: {parsed_final.netloc}")

    return final_url


# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Example call – replace with real values in production
    try:
        url = generate_oauth_token_url(
            "https://app.example.com",
            "/oauth/callback",
            "random_state_token_12345"
        )
        print("Generated OAuth callback URL:", url)
    except Exception as e:
        print(f"Error: {e}")