#!/usr/bin/env python3
"""
Utility to construct a safe redirect URL after login.

The function ensures that the resulting URL is either:
* within the same origin as ``domain_base_url``, or
* points to an explicitly allowed external domain.
"""

from urllib.parse import urlparse, urljoin

# List of fully-qualified domains that are considered safe for external redirects.
ALLOWED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
    # Add more domains as required.
]

def construct_redirect_link(domain_base_url: str, next_redirect_param: str) -> str:
    """
    Construct a full redirect URL after login.

    Parameters
    ----------
    domain_base_url : str
        The base URL of the application (e.g., "https://app.example.com").
    next_redirect_param : str
        The user‑supplied path or URL to redirect to after login.

    Returns
    -------
    str
        The fully‑qualified redirect URL that is safe to use.

    Raises
    ------
    ValueError
        If the resulting URL resolves outside the base domain and is not in
        ``ALLOWED_DOMAINS``.
    """
    if not isinstance(domain_base_url, str) or not isinstance(next_redirect_param, str):
        raise ValueError("Both arguments must be strings.")

    # Parse the base URL to extract its components.
    base_parts = urlparse(domain_base_url)
    if not base_parts.scheme or not base_parts.netloc:
        raise ValueError("`domain_base_url` must be a valid absolute URL.")

    # Resolve the next redirect relative to the base.
    # urljoin handles leading slashes and ensures a proper absolute URL.
    resolved_url = urljoin(domain_base_url, next_redirect_param)

    # Parse the resolved URL to inspect its components.
    parsed_resolved = urlparse(resolved_url)

    # If the resolved URL has no netloc, it is a relative path and thus safe.
    if not parsed_resolved.netloc:
        return resolved_url

    # Normalize netloc for comparison (strip port if present).
    def normalize_netloc(netloc: str) -> str:
        return netloc.split(":")[0].lower()

    resolved_netloc = normalize_netloc(parsed_resolved.netloc)
    base_netloc = normalize_netloc(base_parts.netloc)

    # If the resolved URL is within the same origin as the base, accept it.
    if resolved_netloc == base_netloc:
        return resolved_url

    # Otherwise, check against the list of allowed external domains.
    if resolved_netloc in (d.lower() for d in ALLOWED_DOMAINS):
        return resolved_url

    # If none of the above, reject to prevent open redirect vulnerabilities.
    raise ValueError(
        f"Redirect URL '{resolved_url}' is not allowed: "
        "must be within the base domain or an approved external domain."
    )