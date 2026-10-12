#!/usr/bin/env python3
"""
Utility for constructing secure CDN URLs.
"""

from urllib.parse import urlparse, urlunparse, quote
import pathlib

# Example set of allowed CDN domains; replace with your own safe list.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "static.myapp.net",
    "assets.safe-cdn.org"
}


def _sanitize_path_component(component: str) -> str:
    """
    Ensure the path component is safe for URLs.
    Reject components that are empty, contain slashes or '..'.
    """
    if not component:
        raise ValueError("Resource key cannot be empty")

    # Reject components that could navigate outside the intended path
    if component.startswith(("/", "..")) or (".." in component):
        raise ValueError(f"Invalid resource key component: {component!r}")

    # Quote to make it URL‑safe
    return quote(component)


def build_external_resource_link(cdn_url: str, resource_key: str, res_category: str) -> str:
    """
    Construct a full CDN URL for an external resource.

    Parameters
    ----------
    cdn_url : str
        Base URL of the CDN (e.g., "https://cdn.example.com/").
    resource_key : str
        Identifier of the requested resource (e.g., "logo.png").
    res_category : str
        Resource category or sub‑path (e.g., "image", "script").

    Returns
    -------
    str
        The fully qualified URL pointing to the resource.

    Raises
    ------
    ValueError
        If the CDN domain is not in ``ALLOWED_CDN_DOMAINS`` or if any
        component contains unsafe characters.
    """
    # Parse the CDN URL and validate its domain
    parsed = urlparse(cdn_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid CDN URL: {cdn_url!r}")

    # Normalize the domain to lowercase for comparison
    domain = parsed.netloc.lower()
    if domain not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"CDN domain {domain!r} is not allowed")

    # Sanitize the category and resource key
    safe_category = _sanitize_path_component(res_category)
    safe_key = _sanitize_path_component(resource_key)

    # Build the path by joining category and key
    # Ensure no leading slash so it is appended to base URL correctly
    path = pathlib.PurePosixPath(safe_category) / safe_key

    # Reconstruct the final URL
    new_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        path.as_posix(),
        "",  # params
        "",  # query
        ""   # fragment
    ))
    return new_url


# Example usage:
if __name__ == "__main__":
    try:
        url = build_external_resource_link(
            cdn_url="https://cdn.example.com/",
            resource_key="logo.png",
            res_category="image"
        )
        print(url)  # https://cdn.example.com/image/logo.png
    except ValueError as exc:
        print(f"URL construction failed: {exc}")