import urllib.parse
from typing import Set

# Example set of allowed CDN domains; in real code this would be defined elsewhere
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.safe-cdn.net",
    "static.content.org",
}


def create_cdn_resource_link(
    cdn_url_base: str,
    resource_identifier: str,
    type_of_resource: str,
) -> str:
    """
    Construct a fully qualified CDN URL for the requested resource.

    Parameters
    ----------
    cdn_url_base : str
        Base URL of the CDN (e.g., "https://cdn.example.com").
    resource_identifier : str
        Identifier of the requested resource (e.g., "logo.png").
    type_of_resource : str
        Type of the resource, used to form a sub‑path (e.g., "image", "script").

    Returns
    -------
    str
        The full URL pointing to the external resource.

    Raises
    ------
    ValueError
        If the resulting URL does not resolve to an allowed CDN domain.
    """
    # Normalize base URL
    parsed_base = urllib.parse.urlparse(cdn_url_base)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid CDN base URL: {cdn_url_base!r}")

    # Ensure the scheme is HTTP/HTTPS
    if parsed_base.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme {parsed_base.scheme!r} in CDN base URL")

    # Build the path: <type_of_resource>/<resource_identifier>
    # Ensure no leading/trailing slashes cause double slashes
    cleaned_type = type_of_resource.strip("/")
    cleaned_identifier = resource_identifier.lstrip("/")

    # Construct the full path
    new_path = urllib.parse.urljoin(
        f"{cleaned_type}/", cleaned_identifier
    )

    # Assemble the final URL
    full_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            new_path,
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    # Validate that the domain is allowed
    if parsed_base.netloc.lower() not in {d.lower() for d in ALLOWED_CDN_DOMAINS}:
        raise ValueError(f"Disallowed CDN domain: {parsed_base.netloc!r}")

    return full_url