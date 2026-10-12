import urllib.parse
from typing import Iterable

# Example list of allowed CDN domains.
ALLOWED_CDN_DOMAINS: Iterable[str] = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.content.org",
}


def build_cdn_resource_url(cdn_url_base: str, file_id: str, file_type: str) -> str:
    """
    Assemble a validated CDN URL for a given resource.

    Parameters
    ----------
    cdn_url_base : str
        Base URL of the CDN (e.g. "https://cdn.example.com/").
    file_id : str
        Unique identifier of the resource.
    file_type : str
        Resource type (e.g. "image", "script").

    Returns
    -------
    str
        Fully-qualified, validated URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resolved URL resolves to a domain not in ``ALLOWED_CDN_DOMAINS``.
    """
    # Normalise the base URL to ensure it is absolute
    parsed_base = urllib.parse.urlparse(cdn_url_base)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid CDN base URL: {cdn_url_base!r}")

    # Build the relative path; use forward slashes only
    relative_path = urllib.parse.quote(f"{file_type.rstrip('/')}/{file_id.lstrip('/')}")
    # Construct the full URL
    full_url = urllib.parse.urljoin(cdn_url_base, relative_path)

    # Validate the domain
    parsed_full = urllib.parse.urlparse(full_url)
    if parsed_full.netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Disallowed CDN domain: {parsed_full.netloc!r}. "
            f"Allowed domains are: {', '.join(sorted(ALLOWED_CDN_DOMAINS))}"
        )

    return full_url