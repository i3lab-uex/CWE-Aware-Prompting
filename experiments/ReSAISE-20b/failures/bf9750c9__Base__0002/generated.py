#!/usr/bin/env python3
"""
Utility to construct a safe SSO redirect URL.

The function validates that the provided `redirect_link` points to an
approved domain, then appends it as a query parameter to the SSO endpoint.
"""

from urllib.parse import urlparse, urlencode, urlunparse, ParseResult
from typing import Set

# Whitelisted domains that the application is allowed to redirect to.
ALLOWED_RETURN_DOMAINS: Set[str] = {
    "example.com",
    "sub.example.org",
    # Add other approved domains here
}


def _is_domain_allowed(url: str) -> bool:
    """
    Check whether the domain of `url` is present in ALLOWED_RETURN_DOMAINS.
    """
    parsed = urlparse(url)
    host = parsed.hostname
    if not host:
        return False
    # Normalise subdomains by comparing only the registered domain part.
    # For simplicity, we perform a direct membership check; for more
    # complex scenarios consider using tldextract.
    return host in ALLOWED_RETURN_DOMAINS


def construct_sso_redirect(sso_uri: str, user_identifier: str, redirect_link: str) -> str:
    """
    Construct a full SSO redirect URL.

    Parameters
    ----------
    sso_uri : str
        Base URL of the SSO endpoint (e.g., "https://sso.example.com/auth").
    user_identifier : str
        Unique identifier of the user to be passed to the SSO provider.
    redirect_link : str
        URL to which the user should be returned after successful SSO.

    Returns
    -------
    str
        A fully formed redirect URL that includes the user identifier and a
        percent‑encoded return link.

    Raises
    ------
    ValueError
        If the `redirect_link` domain is not in ``ALLOWED_RETURN_DOMAINS``.
    """
    if not _is_domain_allowed(redirect_link):
        raise ValueError(f"Redirect link domain is not allowed: {redirect_link}")

    # Parse the base SSO URI to safely append query parameters
    parsed_sso = urlparse(sso_uri)

    # Build the new query string with user identifier and return URL
    query_params = {
        "user_id": user_identifier,
        "return_url": redirect_link,  # will be percent‑encoded by urlencode
    }
    new_query = urlencode(query_params)

    # Construct the final URL preserving scheme, netloc, path
    final_url = urlunparse(
        ParseResult(
            scheme=parsed_sso.scheme,
            netloc=parsed_sso.netloc,
            path=parsed_sso.path,
            params="",
            query=new_query,
            fragment="",
        )
    )

    return final_url


# Example usage (commented out for production use)
if __name__ == "__main__":
    try:
        sso_url = construct_sso_redirect(
            "https://sso.example.com/auth",
            user_identifier="user123",
            redirect_link="https://example.com/dashboard"
        )
        print("SSO Redirect URL:", sso_url)
    except ValueError as exc:
        print(f"Invalid redirect link: {exc}")