#!/usr/bin/env python3
"""
Utility to safely construct an API redirect URL.

The implementation checks that:
* the base URL belongs to a pre‑approved domain,
* the endpoint is among a whitelist of allowed paths,
* the final URL does not redirect to an untrusted site (CWE‑601).

If any check fails, a ValueError is raised.
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Optional

# --------------------------------------------------------------------------- #
# Configuration – adjust as appropriate for your environment
# --------------------------------------------------------------------------- #

# Domains that are known to be safe and trusted.
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.mycompany.org",
    "trusted-api.net",
}

# Exact endpoint paths that are allowed.
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/status",
    "/public/info",
]

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def generate_api_redirect(
    base_url: str,
    api_path: str,
    params: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a fully qualified API redirect URL.

    Parameters
    ----------
    base_url : str
        The base address of the API (e.g., "https://api.example.com").
    api_path : str
        The endpoint path (e.g., "/v1/users").
    params : dict, optional
        Query parameters to append.

    Returns
    -------
    str
        The fully constructed URL ready for redirection.

    Raises
    ------
    ValueError
        If the base domain is not approved or the endpoint is disallowed.
    """
    # 1. Parse and normalise base URL
    parsed_base = urllib.parse.urlparse(base_url)
    if parsed_base.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported scheme '{parsed_base.scheme}'. Only HTTP/HTTPS are allowed.")

    # 2. Validate domain
    base_domain = parsed_base.hostname
    if not base_domain or base_domain.lower() not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{base_domain}' is not approved for API redirects.")

    # 3. Normalise and validate endpoint
    # Ensure api_path starts with a slash
    normalized_endpoint = urllib.parse.urljoin("/", api_path)
    if normalized_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{normalized_endpoint}' is not allowed.")

    # 4. Build the path by joining base path and endpoint
    # Preserve any existing path in base_url (e.g., a prefix)
    full_path = urllib.parse.urljoin(parsed_base.path + "/", normalized_endpoint.lstrip("/"))

    # 5. Assemble the final URL
    scheme = parsed_base.scheme
    netloc = parsed_base.netloc
    query = urllib.parse.urlencode(params or {})
    fragment = ""  # No fragments allowed in redirects

    final_url_parts = urllib.parse.ParseResult(
        scheme=scheme,
        netloc=netloc,
        path=full_path,
        params="",
        query=query,
        fragment=fragment,
    )
    final_url = urllib.parse.urlunparse(final_url_parts)

    # 6. Final safety check – ensure the resulting URL stays within the same domain
    parsed_final = urllib.parse.urlparse(final_url)
    if parsed_final.hostname.lower() != base_domain.lower():
        raise ValueError("Redirect URL points to a different domain than the base URL.")

    return final_url

# --------------------------------------------------------------------------- #
# Example usage (remove or comment out in production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        url = generate_api_redirect(
            base_url="https://api.example.com",
            api_path="/v1/users",
            params={"id": "123", "format": "json"},
        )
        print(f"Redirect URL: {url}")
    except ValueError as exc:
        print(f"Failed to generate redirect URL: {exc}")