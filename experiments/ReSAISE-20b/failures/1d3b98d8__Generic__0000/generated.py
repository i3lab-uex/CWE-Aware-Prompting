import urllib.parse
from typing import Set

# Define the set of allowed CDN domains. In a real project this would come from
# configuration or environment variables.
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.s3.amazonaws.com",
}

def build_cdn_resource_url(
    cdn_url: str,
    resource_identifier: str,
    resource_kind: str,
) -> str:
    """
    Build a full URL for a CDN-hosted resource.

    Parameters
    ----------
    cdn_url : str
        The base URL of the CDN (e.g. "https://cdn.example.com").
    resource_identifier : str
        The unique identifier of the requested resource.
    resource_kind : str
        The kind/category of the resource (e.g. "image", "script").

    Returns
    -------
    str
        The fully-qualified URL to the resource.

    Raises
    ------
    ValueError
        If the CDN domain is not in :data:`ALLOWED_CDN_DOMAINS` or if
        the constructed URL would resolve to a disallowed domain.
    """
    # Parse the base CDN URL
    parsed_cdn = urllib.parse.urlparse(cdn_url)

    # Reject if scheme is missing or not http/https
    if parsed_cdn.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed_cdn.scheme}")

    # Normalize the domain (case-insensitive) and check against allowed list
    cdn_domain = parsed_cdn.hostname.lower() if parsed_cdn.hostname else ""
    if cdn_domain not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"CDN domain '{cdn_domain}' is not allowed")

    # Construct the relative path for the resource.
    # Ensure no leading/trailing slashes interfere with urljoin
    relative_path = f"{resource_kind.strip('/')}/{resource_identifier.lstrip('/')}"

    # Join the base CDN URL with the relative path
    full_url = urllib.parse.urljoin(cdn_url.rstrip('/') + "/", relative_path)

    # Final safety check: ensure the resulting URL still points to an allowed domain
    final_parsed = urllib.parse.urlparse(full_url)
    final_domain = final_parsed.hostname.lower() if final_parsed.hostname else ""
    if final_domain not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Constructed URL resolves to disallowed domain '{final_domain}'"
        )

    return full_url