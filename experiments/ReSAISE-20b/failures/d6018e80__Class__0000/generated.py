#!/usr/bin/env python3
"""
Utility for generating a Single Sign-On (SSO) redirect URL.

The implementation follows best practices to mitigate CWE‑610 by ensuring
that the return URL belongs to an allowed domain before constructing the
final redirect URL. All user‑supplied data is properly encoded to prevent
URL injection or other content‑based attacks.
"""

from __future__ import annotations

import urllib.parse
from typing import Set


# --------------------------------------------------------------------------- #
# Configuration: Define the set of domains that are permitted for redirect URLs.
# In a real deployment, populate this with your trusted domains.
ALLOWED_RETURN_DOMAINS: Set[str] = {
    "example.com",
    "sub.example.org",
    # Add other allowed domains here.
}
# --------------------------------------------------------------------------- #

def _extract_domain(url: str) -> str:
    """
    Extract the hostname from a URL.

    Parameters
    ----------
    url : str
        The URL to parse.

    Returns
    -------
    str
        The hostname component of the URL (lower‑cased).

    Raises
    ------
    ValueError
        If the URL is malformed or does not contain a network location.
    """
    parsed = urllib.parse.urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL: {url!r}")
    # Return the hostname in lower‑case for case‑insensitive comparison.
    return parsed.hostname.lower() if parsed.hostname else ""


def create_sso_redirect_url(sso_url: str, uid: str, redirect_url: str) -> str:
    """
    Build an SSO redirect URL that safely forwards the user to a third‑party
    authentication provider and then back to the supplied return URL.

    Parameters
    ----------
    sso_url : str
        Base URL of the SSO service (e.g., https://sso.example.com/login).
    uid : str
        Unique identifier of the user to be passed to the SSO service.
    redirect_url : str
        URL that the SSO provider should return to after authentication.

    Returns
    -------
    str
        The fully‑qualified SSO redirect URL with properly encoded query
        parameters.

    Raises
    ------
    ValueError
        If the return URL’s domain is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate that the return URL's domain is allowed.
    return_domain = _extract_domain(redirect_url)
    if return_domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"Return URL domain '{return_domain}' is not allowed. "
            "Allowed domains: "
            f"{', '.join(sorted(ALLOWED_RETURN_DOMAINS))}"
        )

    # Build the query parameters.  Use a dictionary so that values are
    # automatically percent‑encoded by ``urlencode``.
    query_params = {
        "uid": uid,
        "redirect_uri": redirect_url,
    }

    # Parse the base SSO URL to preserve any existing query parameters.
    parsed_sso = urllib.parse.urlparse(sso_url)
    # Merge any existing query parameters with the new ones.
    existing_params = urllib.parse.parse_qs(parsed_sso.query, keep_blank_values=True)
    # ``parse_qs`` returns values as lists; flatten them for our use case.
    flattened_existing = {k: v[0] for k, v in existing_params.items()}

    # Combine parameters, giving precedence to the new ones.
    combined_params = {**flattened_existing, **query_params}

    # Reconstruct the SSO URL with the combined query string.
    new_query = urllib.parse.urlencode(combined_params, doseq=True)
    final_sso_url = urllib.parse.urlunparse(
        (
            parsed_sso.scheme,
            parsed_sso.netloc,
            parsed_sso.path,
            parsed_sso.params,
            new_query,
            parsed_sso.fragment,
        )
    )

    return final_sso_url


# --------------------------------------------------------------------------- #
# Example usage (remove or comment out in production)
if __name__ == "__main__":
    try:
        result = create_sso_redirect_url(
            sso_url="https://sso.example.com/login",
            uid="user123",
            redirect_url="https://app.example.com/callback"
        )
        print("Generated SSO URL:")
        print(result)
    except ValueError as exc:
        print(f"Error: {exc}")