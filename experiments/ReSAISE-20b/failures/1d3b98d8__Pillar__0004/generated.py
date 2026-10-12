import urllib.parse
from typing import Set

# Example set of allowed CDN domains; replace with real values as needed.
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.content.net"
}

def build_cdn_resource_url(
    cdn_url: str,
    resource_identifier: str,
    resource_kind: str
) -> str:
    """
    Construct a full CDN URL for a specific resource.

    Parameters
    ----------
    cdn_url : str
        Base URL of the CDN. Must include a scheme (http/https) and a host.
    resource_identifier : str
        Unique identifier of the resource (e.g., filename or hash).
    resource_kind : str
        Type of resource, such as 'image' or 'script'.

    Returns
    -------
    str
        The fully-qualified URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resulting URL does not resolve to an allowed CDN domain,
        or if the base URL is malformed.
    """
    # Parse the base CDN URL
    parsed_base = urllib.parse.urlparse(cdn_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid CDN base URL: {cdn_url!r}")

    # Ensure the domain is allowed
    if parsed_base.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"CDN domain {parsed_base.hostname!r} is not in the allowed list."
        )

    # Construct the path to the resource
    # Normalize paths: strip leading/trailing slashes then join
    base_path = parsed_base.path.rstrip("/")
    resource_path = urllib.parse.quote_plus(resource_identifier.strip())
    kind_path = resource_kind.strip().strip("/")

    # Build the final path
    full_path = f"{base_path}/{kind_path}/{resource_path}"

    # Reconstruct the full URL
    final_url = urllib.parse.urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        full_path,
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return final_url