#!/usr/bin/env python3
"""
Utility to safely build an API redirect URL.

The function validates that the base URL belongs to an approved domain
and that the requested endpoint is allowed.  It then appends any query
parameters provided by the caller and returns a fully‑formed URL.

The implementation follows the OWASP guidance for preventing
Open Redirects (CWE‑601) by performing strict validation of both the
domain and the endpoint path.
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Iterable, Optional

# ----------------------------------------------------------------------
# Configuration – in a real project these would be imported from
# a central settings module.
# ----------------------------------------------------------------------
APPROVED_API_DOMAINS: set[str] = {
    "api.example.com",
    "service.internal.company.org",
}

ALLOWED_ENDPOINTS: Iterable[str] = (
    "/users",
    "/orders",
    "/products",
    "/healthcheck",
)

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _is_domain_approved(base_url: str) -> bool:
    """
    Check that the netloc of `base_url` is in APPROVED_API_DOMAINS.
    """
    parsed = urllib.parse.urlparse(base_url)
    # Normalise: lower‑case and strip port if present
    netloc = parsed.netloc.split(":")[0].lower()
    return netloc in APPROVED_API_DOMAINS


def _is_endpoint_allowed(endpoint: str) -> bool:
    """
    Validate that the supplied endpoint is one of the allowed endpoints.
    Leading and trailing slashes are normalised for comparison.
    """
    # Reject empty or absolute URLs
    if not endpoint or endpoint.startswith(("http://", "https://")):
        return False

    # Normalise: ensure a single leading slash, no trailing slash
    ep = "/" + endpoint.lstrip("/")
    ep = ep.rstrip("/")

    return any(ep == allowed.rstrip("/") for allowed in ALLOWED_ENDPOINTS)


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def build_api_redirect_url(
    api_base_url: str,
    endpoint: str,
    query_params: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a fully‑qualified API redirect URL.

    Parameters
    ----------
    api_base_url : str
        The base URL of the API, e.g. "https://api.example.com".
    endpoint : str
        The specific endpoint path, e.g. "/users/123".
    query_params : dict[str, str] | None
        Optional dictionary of query parameters.

    Returns
    -------
    str
        The fully‑qualified URL ready for redirection.

    Raises
    ------
    ValueError
        If the base domain is not approved or the endpoint is disallowed.
    """
    # Validate base URL
    if not _is_domain_approved(api_base_url):
        raise ValueError(f"Domain not approved: {api_base_url}")

    # Validate endpoint
    if not _is_endpoint_allowed(endpoint):
        raise ValueError(f"Endpoint not allowed: {endpoint}")

    # Parse the base URL to preserve scheme, netloc, and any existing path
    parsed_base = urllib.parse.urlparse(api_base_url)

    # Combine the base path with the endpoint
    combined_path = urllib.parse.urljoin(parsed_base.path + "/", endpoint)

    # Build the new URL components
    url_parts = list(parsed_base)
    url_parts[2] = combined_path  # path
    url_parts[4] = ""             # params (unused)
    url_parts[5] = ""             # fragment (unused)

    # Encode query parameters if provided
    if query_params:
        url_parts[4] = urllib.parse.urlencode(query_params)

    final_url = urllib.parse.urlunparse(url_parts)
    return final_url


# ----------------------------------------------------------------------
# Example usage (would normally be in a separate test module)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    try:
        url = build_api_redirect_url(
            "https://api.example.com/v1",
            "/users/42",
            {"detail": "full", "lang": "en"},
        )
        print("Redirect URL:", url)
    except ValueError as exc:
        print(f"Invalid redirect: {exc}")