import urllib.parse

# Set of domains that are considered safe CDNs for this application.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.mysite.net",
}

def build_cdn_resource_url(cdn_url: str, resource_identifier: str, resource_kind: str) -> str:
    """
    Construct a full CDN URL for the requested resource.

    Parameters
    ----------
    cdn_url : str
        Base CDN URL (e.g., "https://cdn.example.com").
    resource_identifier : str
        Unique identifier for the resource (e.g., "logo.png" or "app.js").
    resource_kind : str
        Kind of the resource (e.g., "image", "script").

    Returns
    -------
    str
        Fully qualified URL pointing to the resource on the CDN.

    Raises
    ------
    ValueError
        If the resolved domain is not in :data:`ALLOWED_CDN_DOMAINS`.
    """
    # Parse the base CDN URL.
    parsed_base = urllib.parse.urlparse(cdn_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid CDN base URL: {cdn_url!r}")

    # Verify that the domain is allowed.
    if parsed_base.netloc.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Domain '{parsed_base.netloc}' is not an allowed CDN domain."
        )

    # Normalize and join the path components.
    # Ensure no leading/trailing slashes cause double slashes in the result.
    base_path = parsed_base.path.rstrip("/")
    resource_path = urllib.parse.quote_plus(resource_identifier.lstrip("/"))
    full_path = f"{base_path}/{resource_kind.rstrip('/')}/{resource_path}"

    # Reconstruct the full URL.
    built_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            full_path,
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    return built_url