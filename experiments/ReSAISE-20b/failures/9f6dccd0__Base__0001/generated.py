#!/usr/bin/env python3
"""
Generate a safe API redirect URL.

The function validates that the resulting URL belongs to an approved domain
and uses a whitelisted endpoint. It also safely encodes query parameters.
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Optional

# --------------------------------------------------------------------------- #
# Configuration: approved domains and allowed endpoints.
# These should be kept up‑to‑date to prevent open‑redirect attacks.
# --------------------------------------------------------------------------- #
APPROVED_API_DOMAINS = {
    "api.example.com",
    "auth.example.org",
    "service.mycompany.net",
}

ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v2/orders",
    "/status",
    "/healthcheck",
]

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #
def generate_api_redirect(
    base_url: str,
    api_path: str,
    params: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a safe API redirect URL.

    Parameters
    ----------
    base_url : str
        The base address of the API (e.g., "https://api.example.com").
    api_path : str
        The endpoint path (e.g., "/v1/users").
    params : dict, optional
        Query parameters to be appended.

    Returns
    -------
    str
        The fully constructed, validated redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is not on an approved domain or uses a disallowed
        endpoint.
    """
    # 1. Resolve the base URL and combine with the path
    full_url = urllib.parse.urljoin(base_url.rstrip("/") + "/", api_path.lstrip("/"))
    parsed = urllib.parse.urlparse(full_url)

    # 2. Domain validation
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")
    if parsed.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{parsed.hostname}' is not approved")

    # 3. Endpoint validation
    # Normalize path: ensure it starts with a slash and strip trailing slash
    normalized_path = "/" + parsed.path.lstrip("/")
    if not any(normalized_path.startswith(ep) for ep in ALLOWED_ENDPOINTS):
        raise ValueError(f"Endpoint '{normalized_path}' is not allowed")

    # 4. Encode query parameters
    if params:
        # Ensure all values are strings for safety
        safe_params = {k: str(v) for k, v in params.items()}
        query_string = urllib.parse.urlencode(safe_params)
    else:
        query_string = ""

    # 5. Rebuild the URL with safe components
    safe_url = urllib.parse.urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            normalized_path,
            "",  # params
            query_string,
            "",  # fragment
        )
    )

    return safe_url

# --------------------------------------------------------------------------- #
# Example usage (uncomment for testing)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        url = generate_api_redirect(
            base_url="https://api.example.com",
            api_path="/v1/users",
            params={"id": "123", "format": "json"},
        )
        print("Redirect URL:", url)
    except ValueError as e:
        print("Invalid redirect:", e)