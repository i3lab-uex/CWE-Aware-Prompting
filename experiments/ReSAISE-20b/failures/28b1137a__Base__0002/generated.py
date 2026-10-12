#!/usr/bin/env python3
"""
Utility for building a secure SSO redirect URL.

The function validates that the user‑supplied return URL points to an
approved domain before constructing the final SSO redirect link.
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, List, Set

# Whitelist of domains that are allowed to receive the SSO redirect.
ALLOWED_RETURN_DOMAINS: Set[str] = {
    "example.com",
    "app.example.org",
    # Add additional trusted domains here.
}


def _normalize_domain(domain: str) -> str:
    """
    Normalise a domain string by lower‑casing and stripping leading/trailing
    whitespace.  Ports are ignored because the whitelist contains hostnames only.
    """
    return domain.strip().lower()


def _is_allowed_domain(url: str) -> bool:
    """
    Return True if the domain of *url* is in ALLOWED_RETURN_DOMAINS.
    """
    try:
        parsed = urllib.parse.urlparse(url)
        host = _normalize_domain(parsed.hostname or "")
    except Exception:
        return False

    # Allow subdomains if they are explicitly listed.
    return host in ALLOWED_RETURN_DOMAINS


def build_sso_url(sso_path: str, uid: str, redirect_url: str) -> str:
    """
    Construct a full SSO redirect URL.

    Parameters
    ----------
    sso_path : str
        Base URL of the SSO endpoint (may contain query parameters).
    uid : str
        User identifier to be sent to the SSO provider.
    redirect_url : str
        URL to which the user should be redirected after successful SSO.

    Returns
    -------
    str
        A fully‑formed redirect URL that includes the SSO endpoint,
        user ID, and return destination.

    Raises
    ------
    ValueError
        If *redirect_url* does not point to an approved domain.
    """
    if not _is_allowed_domain(redirect_url):
        raise ValueError("Redirect URL domain is not allowed")

    # Parse the base SSO path.
    parsed_sso = urllib.parse.urlparse(sso_path)

    # Extract existing query parameters (if any).
    existing_params: Dict[str, List[str]] = urllib.parse.parse_qs(parsed_sso.query)

    # Add/override with new parameters.
    existing_params["uid"] = [uid]
    existing_params["redirect_url"] = [redirect_url]

    # Reconstruct the query string.
    new_query = urllib.parse.urlencode(existing_params, doseq=True)

    # Build the final URL.
    sso_url = urllib.parse.urlunparse(
        (
            parsed_sso.scheme,
            parsed_sso.netloc,
            parsed_sso.path,
            parsed_sso.params,
            new_query,
            parsed_sso.fragment,
        )
    )

    return sso_url