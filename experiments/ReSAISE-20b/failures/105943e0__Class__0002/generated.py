#!/usr/bin/env python3
"""
Utility to construct a secure SSO redirect URL.

The function validates that the provided callback URL belongs to an
allowed domain set before appending it as a query parameter to the
SSO login endpoint.  This mitigates CWE‑610 (externally controlled reference)
by ensuring that only trusted domains can be used as a return target.
"""

from __future__ import annotations

import urllib.parse
from typing import Set


# Example set of allowed domains; replace with your real configuration.
ALLOWED_RETURN_DOMAINS: Set[str] = {
    "example.com",
    "auth.example.org",
    "trusted.partner.net",
}


def _normalize_domain(domain: str) -> str:
    """
    Normalise a domain string for comparison.

    - Lower‑case.
    - Strip any leading ``www.`` prefix.
    """
    domain = domain.lower()
    if domain.startswith("www."):
        domain = domain[4:]
    return domain


def _is_domain_allowed(url: str, allowed_domains: Set[str]) -> bool:
    """
    Return ``True`` if the domain part of *url* is in *allowed_domains*.
    """
    parsed = urllib.parse.urlparse(url)
    host = parsed.hostname
    if not host:
        return False

    # Allow sub‑domains of the approved domains.
    normalized = _normalize_domain(host)
    for allowed in allowed_domains:
        if normalized == _normalize_domain(allowed) or \
           normalized.endswith("." + _normalize_domain(allowed)):
            return True
    return False


def create_sso_redirect_url(
    login_endpoint: str,
    account_id: str,
    callback_url: str
) -> str:
    """
    Build a redirect URL for SSO authentication.

    Parameters
    ----------
    login_endpoint : str
        Base URL of the third‑party SSO provider.
    account_id : str
        Unique identifier for the user to be authenticated.
    callback_url : str
        Destination URL to which the provider should redirect after
        successful authentication.

    Returns
    -------
    str
        A fully‑formed URL that the client should be redirected to.

    Raises
    ------
    ValueError
        If ``callback_url`` is not within the set of allowed domains.
    """
    # Validate callback domain
    if not _is_domain_allowed(callback_url, ALLOWED_RETURN_DOMAINS):
        raise ValueError(
            f"Return URL domain not allowed: {urllib.parse.urlparse(callback_url).hostname}"
        )

    # Construct query parameters safely
    params = {
        "account_id": account_id,
        "return_url": callback_url,
    }
    query = urllib.parse.urlencode(params, quote_via=urllib.parse.quote_plus)

    # Join with the base endpoint
    parsed_login = urllib.parse.urlparse(login_endpoint)
    if parsed_login.scheme not in {"http", "https"}:
        raise ValueError("Login endpoint must use http or https scheme")

    # Preserve existing query parameters on the login_endpoint
    if parsed_login.query:
        new_query = f"{parsed_login.query}&{query}"
    else:
        new_query = query

    redirect_parts = parsed_login._replace(query=new_query)
    return urllib.parse.urlunparse(redirect_parts)


# Example usage (commented out; remove for production)
if __name__ == "__main__":
    try:
        url = create_sso_redirect_url(
            login_endpoint="https://sso.provider.com/auth",
            account_id="user12345",
            callback_url="https://example.com/dashboard"
        )
        print(url)
    except ValueError as exc:
        print(f"Invalid callback URL: {exc}")