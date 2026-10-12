#!/usr/bin/env python3
"""
Utility for constructing a secure SSO redirect URL.

The function ensures that the return URL (redirect_link) is restricted to a
whitelisted set of domains. This protects against open‑redirect attacks
(CWE-610) by preventing the application from redirecting users to arbitrary
domains.
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Iterable


# --------------------------------------------------------------------------- #
# Configuration – whitelist of allowed domains for the return URL.
# --------------------------------------------------------------------------- #
ALLOWED_RETURN_DOMAINS: set[str] = {
    "example.com",
    "app.example.org",
    "trusted.partner.net",
}


def _is_domain_allowed(url: str, allowed_domains: Iterable[str]) -> bool:
    """
    Check whether the hostname of *url* is present in *allowed_domains*.

    Parameters
    ----------
    url : str
        The URL to validate.
    allowed_domains : Iterable[str]
        A collection of domain names considered safe.

    Returns
    -------
    bool
        True if the hostname is in *allowed_domains*, False otherwise.
    """
    try:
        parsed = urllib.parse.urlparse(url)
    except Exception:  # pragma: no cover
        return False

    host = parsed.hostname or ""
    # Normalize subdomains – only the effective top‑level domain + one
    # additional label is considered (e.g. "sub.example.com" -> "example.com").
    parts = host.lower().split(".")
    if len(parts) >= 2:
        effective_domain = ".".join(parts[-2:])
    else:
        effective_domain = host.lower()

    return effective_domain in allowed_domains


def construct_sso_redirect(
    sso_uri: str, user_identifier: str, redirect_link: str
) -> str:
    """
    Construct an SSO redirect URL that safely includes a user identifier and
    a return link.

    The function validates that the *redirect_link* domain is present in the
    :data:`ALLOWED_RETURN_DOMAINS` whitelist. If it is not, a ``ValueError`` is
    raised.

    Parameters
    ----------
    sso_uri : str
        Base SSO endpoint URL (e.g. "https://sso.example.com/auth").
    user_identifier : str
        Unique identifier for the user (e.g. a UUID or username).
    redirect_link : str
        URL to which the identity provider should redirect after login.

    Returns
    -------
    str
        A fully formed SSO URL containing the user identifier and return link.

    Raises
    ------
    ValueError
        If *redirect_link* does not resolve to an allowed domain.
    """
    # --------------------------------------------------------------------- #
    # 1. Validate the return URL against the whitelist.
    # --------------------------------------------------------------------- #
    if not _is_domain_allowed(redirect_link, ALLOWED_RETURN_DOMAINS):
        raise ValueError(
            f"Redirect domain not allowed: {urllib.parse.urlparse(redirect_link).hostname}"
        )

    # --------------------------------------------------------------------- #
    # 2. Build query parameters.
    # --------------------------------------------------------------------- #
    query_params: Dict[str, str] = {
        "user": user_identifier,
        "redirect": redirect_link,
    }

    # --------------------------------------------------------------------- #
    # 3. Merge with any existing query parameters on the SSO endpoint.
    # --------------------------------------------------------------------- #
    parsed_sso = urllib.parse.urlparse(sso_uri)
    existing_params = dict(urllib.parse.parse_qsl(parsed_sso.query, keep_blank_values=True))
    merged_params = {**existing_params, **query_params}
    encoded_query = urllib.parse.urlencode(merged_params)

    # --------------------------------------------------------------------- #
    # 4. Reconstruct the full URL.
    # --------------------------------------------------------------------- #
    final_url = urllib.parse.urlunparse(
        (
            parsed_sso.scheme,
            parsed_sso.netloc,
            parsed_sso.path,
            parsed_sso.params,
            encoded_query,
            parsed_sso.fragment,
        )
    )

    return final_url


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        url = construct_sso_redirect(
            sso_uri="https://sso.example.com/login",
            user_identifier="user-12345",
            redirect_link="https://app.example.org/dashboard",
        )
        print(url)
    except ValueError as exc:
        print(f"Validation error: {exc}")