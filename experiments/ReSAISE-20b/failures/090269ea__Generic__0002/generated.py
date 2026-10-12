#!/usr/bin/env python3
"""
Utility for constructing safe CDN resource URLs.
"""

import urllib.parse

# Allowed CDN domains (example values; populate with real ones)
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "static.myapp.net",
    "assets.contenthost.org",
}

def create_external_resource_link(cdn_url: str, res_id: str, res_type: str) -> str:
    """
    Assemble a fully-qualified URL for an external resource.

    Parameters
    ----------
    cdn_url : str
        Base CDN URL (e.g. 'https://cdn.example.com/').
    res_id : str
        Unique identifier for the resource (e.g. a file hash or UUID).
    res_type : str
        Resource type, used as a path segment (e.g. 'image', 'script').

    Returns
    -------
    str
        A fully-qualified, validated URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain that is not in
        :data:`ALLOWED_CDN_DOMAINS`.
    """
    if not cdn_url or not res_id or not res_type:
        raise ValueError("cdn_url, res_id and res_type must be non-empty strings")

    # Normalise the base URL: ensure scheme is present and trailing slash
    parsed_base = urllib.parse.urlparse(cdn_url)
    if not parsed_base.scheme:
        raise ValueError("cdn_url must include a scheme (http or https)")
    base_netloc = parsed_base.netloc.lower()
    if base_netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain '{base_netloc}' is not an allowed CDN")

    # Build the relative path safely
    # Avoid double slashes and ensure no leading/trailing spaces
    rel_path = f"{res_type.strip('/')}/{res_id.strip('/')}"
    full_url = urllib.parse.urljoin(parsed_base.geturl(), rel_path)

    # Final validation: ensure the domain hasn't changed due to redirects or tricks
    final_netloc = urllib.parse.urlparse(full_url).netloc.lower()
    if final_netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Resulting URL points to unauthorized domain '{final_netloc}'")

    return full_url