#!/usr/bin/env python3
"""
Utility to construct CDN resource URLs while guarding against
externally‑controlled references (CWE‑610).
"""

from __future__ import annotations

import re
from urllib.parse import urlparse, urlunparse, quote_plus

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# Domains that are considered safe for CDN usage.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.safe-cdn.net",
    "static.myapp.org",
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _is_allowed_domain(domain: str) -> bool:
    """
    Check if a domain is present in the ALLOWED_CDN_DOMAINS set.
    Normalises to lower‑case and strips port numbers.
    """
    # Remove any leading/trailing whitespace
    domain = domain.strip().lower()
    # Strip port if present (e.g., example.com:443)
    domain = re.sub(r":\d+$", "", domain)
    return domain in ALLOWED_CDN_DOMAINS


def _normalize_path(path: str) -> str:
    """
    Normalise a URL path by removing dot segments and ensuring
    that it does not contain traversal sequences.
    """
    # Reject absolute paths with leading slashes that could
    # escape the intended hierarchy.
    if path.startswith("/"):
        raise ValueError("Path must be relative (no leading slash).")

    # Reject any '..' segments that could navigate out of the
    # intended directory structure.
    if ".." in path.split("/"):
        raise ValueError("Path contains prohibited '..' segment.")

    # Encode each component separately to avoid injection.
    parts = [quote_plus(part) for part in path.split("/") if part]
    return "/".join(parts)


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def build_cdn_resource_url(
    cdn_url: str,
    resource_identifier: str,
    resource_kind: str,
) -> str:
    """
    Build a fully‑qualified CDN URL for a given resource.

    Parameters
    ----------
    cdn_url : str
        Base CDN URL, e.g. "https://cdn.example.com".
    resource_identifier : str
        Unique identifier for the resource, e.g. "logo.png".
    resource_kind : str
        Kind of resource (e.g., 'image', 'script').

    Returns
    -------
    str
        A safe, fully‑qualified URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the CDN domain is not in ALLOWED_CDN_DOMAINS, or if any
        component fails validation.
    """
    # Parse the base CDN URL and validate its components.
    parsed = urlparse(cdn_url)

    if not parsed.scheme or parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("cdn_url must have http or https scheme")

    if not parsed.netloc:
        raise ValueError("cdn_url must contain a network location (domain)")

    if not _is_allowed_domain(parsed.netloc):
        raise ValueError(f"Domain '{parsed.netloc}' is not an allowed CDN")

    # Normalise the resource kind and identifier.
    # Reject empty strings or those containing path separators.
    for name, value in (("resource_kind", resource_kind), ("resource_identifier", resource_identifier)):
        if not value:
            raise ValueError(f"{name} cannot be empty")
        if "/" in value or "\\" in value:
            raise ValueError(f"{name} must not contain path separators")

    # Construct the relative path: e.g., "image/logo.png"
    relative_path = f"{resource_kind}/{resource_identifier}"
    try:
        normalized_relative = _normalize_path(relative_path)
    except ValueError as exc:
        raise ValueError(f"Invalid resource path: {exc}") from None

    # Build the final URL by concatenating the base with the normalized path.
    # Ensure there is exactly one slash between them.
    final_path = f"{parsed.path.rstrip('/')}/{normalized_relative}"
    built_url = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            final_path,
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    return built_url


# --------------------------------------------------------------------------- #
# Example usage (for manual testing only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Example: should succeed
    print(
        build_cdn_resource_url(
            "https://cdn.example.com",
            "logo.png",
            "image",
        )
    )

    # Example: should fail due to disallowed domain
    try:
        build_cdn_resource_url(
            "https://evil.com",
            "script.js",
            "script",
        )
    except ValueError as e:
        print(f"Caught expected error: {e}")