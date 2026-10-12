import urllib.parse
from typing import Set

# Example set of allowed CDN domains. In real code this would be configurable.
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.example.org",
}

def construct_external_resource_url(
    cdn_base_url: str,
    resource_id: str,
    resource_type: str
) -> str:
    """
    Construct a secure URL to an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_base_url : str
        Base URL of the CDN (e.g. "https://cdn.example.com/").
    resource_id : str
        Identifier of the resource (e.g. "12345" or "logo.png").
    resource_type : str
        Type of the resource (e.g. "image", "script"). This is used only for
        informational purposes and may be incorporated into the path.

    Returns
    -------
    str
        The fully qualified URL pointing to the resource on an allowed CDN.

    Raises
    ------
    ValueError
        If the resolved URL does not resolve to a domain in ``ALLOWED_CDN_DOMAINS``
        or if the base URL uses an unsafe scheme.
    """

    # Parse and validate the CDN base URL
    parsed_base = urllib.parse.urlparse(cdn_base_url)
    if parsed_base.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme '{parsed_base.scheme}'. Only http and https are allowed.")
    if parsed_base.netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain '{parsed_base.netloc}' is not an allowed CDN domain.")

    # Build a safe path component
    # Ensure the resource type is alphanumeric to avoid injection attacks.
    if not resource_type.isalnum():
        raise ValueError("resource_type must be alphanumeric.")

    # Quote the resource_id to avoid path traversal or special characters
    safe_resource_id = urllib.parse.quote(resource_id, safe="")

    # Construct the final path: /{resource_type}/{safe_resource_id}
    resource_path = urllib.parse.urljoin(f"{parsed_base.path.rstrip('/')}/", f"{resource_type}/{safe_resource_id}")

    # Reassemble the final URL
    final_url = urllib.parse.urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        resource_path,
        "",  # params
        "",  # query
        ""   # fragment
    ))

    # Final sanity check: ensure the resulting domain is still allowed
    final_parsed = urllib.parse.urlparse(final_url)
    if final_parsed.netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Resulting URL domain '{final_parsed.netloc}' is not allowed.")

    return final_url