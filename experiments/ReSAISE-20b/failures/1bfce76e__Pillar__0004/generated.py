#!/usr/bin/env python3
"""
Utility to construct a CDN URL for an external resource.

The implementation validates that the final URL resolves to one of the
pre‑defined safe CDN domains.  It also normalises the path components and
percent‑encodes any user supplied parts to avoid directory traversal or
malformed URLs.
"""

from __future__ import annotations

import urllib.parse
from typing import Set

# --------------------------------------------------------------------------- #
# Configuration: list of safe CDN domains.
# In a real project this would be populated from configuration or environment.
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "static.myapp.org",
    "assets.somecdn.net",
}

# --------------------------------------------------------------------------- #
def generate_external_resource_url(cdn_base: str, res_id: str, res_type: str) -> str:
    """
    Construct a full CDN URL for an external resource.

    Parameters
    ----------
    cdn_base : str
        The base URL of the CDN.  Must be an absolute URL with a scheme.
    res_id : str
        Identifier of the resource (e.g. file name or hash).
    res_type : str
        Resource type – used as a sub‑path (e.g. 'image', 'script').

    Returns
    -------
    str
        The fully qualified URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resulting URL does not target an allowed CDN domain or if
        input values are malformed.
    """
    # Basic validation of inputs
    if not isinstance(cdn_base, str) or not cdn_base:
        raise ValueError("cdn_base must be a non-empty string")
    if not isinstance(res_id, str) or not res_id:
        raise ValueError("res_id must be a non-empty string")
    if not isinstance(res_type, str) or not res_type:
        raise ValueError("res_type must be a non-empty string")

    # Parse the base CDN URL
    parsed_base = urllib.parse.urlparse(cdn_base)
    if parsed_base.scheme not in {"http", "https"}:
        raise ValueError("cdn_base must have http or https scheme")

    # Ensure the domain is allowed
    base_domain = parsed_base.hostname
    if not base_domain or base_domain.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain '{base_domain}' is not in the list of allowed CDN domains")

    # Normalise and percent‑encode path components
    safe_res_type = urllib.parse.quote(res_type.strip("/"))
    safe_res_id   = urllib.parse.quote(res_id.strip("/"))

    # Construct the full path
    base_path = parsed_base.path.rstrip("/")
    new_path = f"{base_path}/{safe_res_type}/{safe_res_id}"

    # Rebuild the URL
    final_url = urllib.parse.urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        new_path,
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return final_url

# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Simple demo (will only work if the domain is in ALLOWED_CDN_DOMAINS)
    try:
        url = generate_external_resource_url(
            "https://cdn.example.com/assets",
            "logo.png",
            "image"
        )
        print("Generated URL:", url)
    except ValueError as exc:
        print("Error:", exc)