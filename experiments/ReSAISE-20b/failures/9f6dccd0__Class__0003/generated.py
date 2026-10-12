#!/usr/bin/env python3
"""
Utility to safely generate an API redirect URL.

The function validates that the base URL belongs to a pre‑approved
domain, that the requested endpoint is on an allow list, and that
the final URL does not exceed a reasonable length.  It uses the
standard library `urllib.parse` for all URL manipulation, thereby
avoiding manual string concatenation which could lead to malformed
or insecure URLs.

The implementation follows best practices for preventing
CWE‑610 (Externally Controlled Reference to a Resource in Another Sphere)
by strictly whitelisting domains and endpoints.
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Optional

# ----------------------------------------------------------------------
# Configuration – replace with your real values.
# ----------------------------------------------------------------------
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.example.org",
}

ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/status",
]

# Maximum length for a redirect URL (typical browsers support > 2000 chars,
# but keeping it conservative avoids surprises).
MAX_URL_LENGTH = 2048

# ----------------------------------------------------------------------
def _normalize_domain(netloc: str) -> str:
    """
    Extract the host part of a network location, ignoring ports.
    """
    return netloc.split(":")[0].lower()


def _validate_domain(base_url: str) -> None:
    """
    Ensure that the base URL resolves to an approved domain.
    Raises ValueError if not allowed.
    """
    parsed = urllib.parse.urlparse(base_url)
    host = _normalize_domain(parsed.netloc)

    if host not in APPROVED_API_DOMAINS:
        raise ValueError(
            f"Domain '{host}' is not in the list of approved API domains."
        )


def _validate_endpoint(endpoint: str) -> None:
    """
    Ensure that the endpoint is on the allow list.
    Raises ValueError if not allowed.
    """
    # Normalise to a single leading slash and strip trailing slashes
    normalized = "/" + endpoint.lstrip("/").rstrip("/")
    if normalized not in ALLOWED_ENDPOINTS:
        raise ValueError(
            f"Endpoint '{endpoint}' is not allowed. "
            f"Allowed endpoints: {ALLOWED_ENDPOINTS}"
        )


def generate_api_redirect(
    base_url: str,
    api_path: str,
    params: Optional[Dict[str, str]] = None,
) -> str:
    """
    Generate a safe redirect URL for an API request.

    Parameters
    ----------
    base_url : str
        The base address of the API (e.g., "https://api.example.com").
    api_path : str
        The endpoint path (e.g., "/v1/users").
    params : dict, optional
        Dictionary of query parameters to append.

    Returns
    -------
    str
        Fully constructed, validated redirect URL.

    Raises
    ------
    ValueError
        If the domain or endpoint is not approved, or if the URL
        exceeds MAX_URL_LENGTH.
    """
    # 1. Validate base domain and endpoint
    _validate_domain(base_url)
    _validate_endpoint(api_path)

    # 2. Construct the base URL (ensure it ends with a slash if needed)
    parsed_base = urllib.parse.urlparse(base_url)
    # Use urljoin to correctly combine paths
    base_with_slash = (
        parsed_base.scheme + "://" + parsed_base.netloc
        if not parsed_base.path.endswith("/")
        else base_url.rstrip("/")
    )
    full_path = urllib.parse.urljoin(base_with_slash + "/", api_path.lstrip("/"))

    # 3. Append query parameters if provided
    if params:
        query_string = urllib.parse.urlencode(params, doseq=True)
        full_url = f"{full_path}?{query_string}"
    else:
        full_url = full_path

    # 4. Final sanity check on length
    if len(full_url) > MAX_URL_LENGTH:
        raise ValueError(
            f"Generated URL exceeds maximum length of {MAX_URL_LENGTH} characters."
        )

    return full_url


# ----------------------------------------------------------------------
# Example usage (commented out – remove for production)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    try:
        url = generate_api_redirect(
            base_url="https://api.example.com",
            api_path="/v1/users",
            params={"page": "2", "limit": "50"},
        )
        print("Redirect URL:", url)
    except ValueError as exc:
        print(f"Invalid redirect: {exc}")