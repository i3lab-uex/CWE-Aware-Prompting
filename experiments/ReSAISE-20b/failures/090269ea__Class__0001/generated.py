#!/usr/bin/env python3
"""
Utility to safely construct a CDN URL for an external resource.

This module mitigates CWE-610 by validating that the resolved domain
belongs to a known set of approved CDN hosts before returning the URL.
"""

from __future__ import annotations

import urllib.parse
from typing import Iterable, Set


# ----------------------------------------------------------------------
# Configuration: set of allowed CDN domains.
# This should be populated with the exact hostnames that are trusted
# (e.g., 'cdn.example.com', 'assets.myapp.net').
# ----------------------------------------------------------------------
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.myapp.net",
    # Add more trusted CDN hosts here.
}


def _normalize_cdn_url(cdn_url: str) -> urllib.parse.ParseResult:
    """
    Normalise and parse the CDN base URL.

    Parameters
    ----------
    cdn_url : str
        The raw CDN base URL supplied by the caller.

    Returns
    -------
    urllib.parse.ParseResult
        The parsed URL components.
    """
    # Ensure the base URL has a scheme; default to https if missing.
    parsed = urllib.parse.urlparse(cdn_url)
    if not parsed.scheme:
        parsed = urllib.parse.urlparse(f"https://{cdn_url}")

    # Remove trailing slashes to simplify joining.
    netloc = parsed.netloc.rstrip("/")
    path = parsed.path.rstrip("/") + "/"
    return urllib.parse.ParseResult(
        scheme=parsed.scheme,
        netloc=netloc,
        path=path,
        params="",
        query="",
        fragment="",
    )


def _validate_domain(parsed_url: urllib.parse.ParseResult) -> None:
    """
    Ensure the parsed URL's domain is in ALLOWED_CDN_DOMAINS.

    Raises
    ------
    ValueError
        If the domain is not permitted.
    """
    # Extract host part (excluding port).
    hostname = parsed_url.hostname
    if hostname is None:
        raise ValueError("CDN URL does not contain a valid host.")

    if hostname.lower() not in {d.lower() for d in ALLOWED_CDN_DOMAINS}:
        raise ValueError(f"Unauthorized CDN domain: {hostname}")


def create_external_resource_link(cdn_url: str, res_id: str, res_type: str) -> str:
    """
    Construct a fully-qualified URL to an external resource served by a CDN.

    Parameters
    ----------
    cdn_url : str
        Base URL of the CDN (e.g., 'https://cdn.example.com').
    res_id : str
        Unique identifier for the resource (e.g., image hash).
    res_type : str
        Resource type used as a sub-path or query parameter (e.g., 'image').

    Returns
    -------
    str
        The complete, validated URL to the requested resource.

    Raises
    ------
    ValueError
        If the constructed URL resolves to a domain not in ALLOWED_CDN_DOMAINS.
    """
    # Normalise the base CDN URL and validate its domain.
    parsed_base = _normalize_cdn_url(cdn_url)
    _validate_domain(parsed_base)

    # Build the path: <cdn_base>/<res_type>/<res_id>
    # Ensure no leading/trailing slashes cause duplication.
    safe_res_type = urllib.parse.quote(res_type.strip("/"))
    safe_res_id = urllib.parse.quote(res_id.strip("/"))

    resource_path = f"{parsed_base.path}{safe_res_type}/{safe_res_id}"

    # Reconstruct the full URL.
    full_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            resource_path,
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    # Final domain validation to catch any edge cases (e.g., double-encoding).
    final_parsed = urllib.parse.urlparse(full_url)
    _validate_domain(final_parsed)

    return full_url