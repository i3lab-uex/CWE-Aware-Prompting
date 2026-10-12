import urllib.parse

# Predefined set of safe CDN domains.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.safe-cdn.net",
    "static.content.org",
}

def build_external_resource_link(cdn_url: str, resource_key: str, res_category: str) -> str:
    """
    Construct a full URL to an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_url : str
        Base URL of the CDN (e.g., "https://cdn.example.com").
    resource_key : str
        Identifier of the specific resource (e.g., "logo.png").
    res_category : str
        Resource category used to namespace the resource (e.g., "image").

    Returns
    -------
    str
        The fully qualified URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resolved URL does not target a domain that belongs to
        ``ALLOWED_CDN_DOMAINS`` or if the URL scheme is not HTTP(S).
    """
    # Normalize and parse the CDN base URL.
    parsed_base = urllib.parse.urlparse(cdn_url)

    # Reject non‑HTTP(S) schemes.
    if parsed_base.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed_base.scheme!r}")

    # Ensure the domain is in the allowed set.
    if parsed_base.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain {parsed_base.hostname!r} is not allowed")

    # Clean the resource components to avoid path traversal.
    safe_category = urllib.parse.quote(res_category.strip("/"))
    safe_key = urllib.parse.quote(resource_key.strip("/"))

    # Build the relative path: /{category}/{key}
    relative_path = f"/{safe_category}/{safe_key}"

    # Resolve the full URL.
    full_url = urllib.parse.urljoin(cdn_url.rstrip("/") + "/", relative_path)

    # Final safety check: parse again to confirm hostname.
    parsed_full = urllib.parse.urlparse(full_url)
    if parsed_full.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Resulting URL points to disallowed domain: {parsed_full.hostname!r}")

    return full_url