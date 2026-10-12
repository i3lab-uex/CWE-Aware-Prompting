#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Secure redirect URL construction for a login flow.

The function ``construct_redirect_link`` builds a full redirect URL from
the application's base URL and a user supplied ``next`` parameter.
It validates that the resulting target is either:

* within the same origin as ``domain_base_url``, or
* an absolute URL whose domain is in :data:`ALLOWED_DOMAINS`.

If the target does not meet either condition, a ``ValueError`` is raised
to prevent open‑redirect vulnerabilities (CWE‑610).
"""

from urllib.parse import urlparse, urljoin
from typing import List

# Example list of externally allowed domains.
ALLOWED_DOMAINS: List[str] = [
    "example.com",
    "trustedpartner.org",
    # Add more domains as needed
]


def construct_redirect_link(domain_base_url: str, next_redirect_param: str) -> str:
    """
    Construct a safe redirect URL after login.

    Parameters
    ----------
    domain_base_url : str
        The base URL of the application (e.g. "https://app.example.com").
    next_redirect_param : str
        The user supplied redirect target. May be a relative path or an absolute URL.

    Returns
    -------
    str
        The fully resolved redirect URL.

    Raises
    ------
    ValueError
        If the constructed target is not within the same origin as ``domain_base_url``
        or does not belong to one of the :data:`ALLOWED_DOMAINS`.
    """
    if not domain_base_url:
        raise ValueError("Base URL must be provided")

    # Normalize base URL (ensure it ends with a slash for urljoin to work correctly)
    if not domain_base_url.endswith("/"):
        base = f"{domain_base_url}/"
    else:
        base = domain_base_url

    # Resolve the next parameter against the base URL
    target_url = urljoin(base, next_redirect_param)

    # Parse both URLs for comparison
    base_parsed = urlparse(base)
    target_parsed = urlparse(target_url)

    # Check if the target is a relative path (no netloc) or within same origin
    if not target_parsed.netloc:
        # Relative path is safe; just return the resolved URL
        return target_url

    # If netloc differs, ensure it is in ALLOWED_DOMAINS
    target_domain = target_parsed.netloc.split(":")[0]  # strip port if present
    if target_domain.lower() in (d.lower() for d in ALLOWED_DOMAINS):
        return target_url

    # If netloc matches base domain (same origin)
    if target_parsed.netloc.lower() == base_parsed.netloc.lower():
        return target_url

    # If none of the above, reject
    raise ValueError(
        f"Redirect target '{target_url}' is not allowed: "
        "must be within the same origin or an explicitly permitted domain."
    )