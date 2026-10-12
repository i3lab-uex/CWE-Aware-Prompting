#!/usr/bin/env python3
"""
SSO redirect URL constructor.

This module provides a single function `construct_sso_redirect` that
creates a secure redirect URL for an external SSO provider.  The function
ensures that the supplied return link belongs to a whitelisted domain,
avoids open redirect vulnerabilities, and correctly encodes all
parameters.
"""

from __future__ import annotations

import urllib.parse
from typing import Set

# --------------------------------------------------------------------------- #
# Whitelist of allowed return domains.  Adjust this set to match your
# infrastructure requirements.
# --------------------------------------------------------------------------- #
ALLOWED_RETURN_DOMAINS: Set[str] = {
    "example.com",
    "app.example.org",
    # Add other trusted domains here
}


def _normalize_domain(domain: str) -> str:
    """
    Normalise a domain for comparison by stripping any leading 'www.' and
    converting to lowercase.

    Parameters
    ----------
    domain : str
        The domain string extracted from a URL.

    Returns
    -------
    str
        Normalised domain.
    """
    return domain.lower().lstrip("www.")


def construct_sso_redirect(
    sso_uri: str,
    user_identifier: str,
    redirect_link: str,
) -> str:
    """
    Construct a full SSO redirect URL.

    The function validates that the `redirect_link` domain is in
    ``ALLOWED_RETURN_DOMAINS`` to prevent open‑redirect attacks.  It then
    appends the user identifier and encoded return URL as query
    parameters to ``sso_uri``.  The resulting URL is fully percent‑encoded.

    Parameters
    ----------
    sso_uri : str
        The base URL of the SSO provider endpoint.
    user_identifier : str
        Unique identifier for the user (e.g., UUID, username).
    redirect_link : str
        URL to return to after SSO authentication completes.

    Returns
    -------
    str
        The fully constructed redirect URL ready for the client to use.

    Raises
    ------
    ValueError
        If ``redirect_link``'s domain is not in ``ALLOWED_RETURN_DOMAINS``.
    """
    # ----------------------------------------------------------------------- #
    # Validate the redirect link domain
    # ----------------------------------------------------------------------- #
    parsed_redirect = urllib.parse.urlparse(redirect_link)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError(f"Invalid redirect link: {redirect_link}")

    domain = _normalize_domain(parsed_redirect.netloc)
    if domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"Redirect domain '{domain}' is not allowed. "
            "Only whitelisted domains are permitted."
        )

    # ----------------------------------------------------------------------- #
    # Build the SSO URL
    # ----------------------------------------------------------------------- #
    parsed_sso = urllib.parse.urlparse(sso_uri)
    query_params = urllib.parse.parse_qs(parsed_sso.query, keep_blank_values=True)

    # Ensure we don't override existing parameters unintentionally
    query_params["user_id"] = [user_identifier]
    # Encode the redirect link safely; use a dedicated parameter name
    query_params["redirect"] = [redirect_link]

    # Construct the new query string
    encoded_query = urllib.parse.urlencode(query_params, doseq=True)

    # Rebuild the full URL
    sso_redirect = urllib.parse.urlunparse(
        (
            parsed_sso.scheme,
            parsed_sso.netloc,
            parsed_sso.path,
            parsed_sso.params,
            encoded_query,
            parsed_sso.fragment,
        )
    )

    return sso_redirect


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Example configuration
    SSO_ENDPOINT = "https://sso.example.com/auth"
    USER_ID = "123e4567-e89b-12d3-a456-426614174000"
    RETURN_URL = "https://app.example.org/dashboard"

    try:
        url = construct_sso_redirect(SSO_ENDPOINT, USER_ID, RETURN_URL)
        print("SSO redirect URL:")
        print(url)
    except ValueError as exc:
        print(f"Error: {exc}")