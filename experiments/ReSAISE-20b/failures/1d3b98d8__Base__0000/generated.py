import urllib.parse

# Set of CDN domains that are considered safe.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "static.content.net",
    "assets.myapp.org",
}

def build_cdn_resource_url(cdn_url: str, resource_identifier: str, resource_kind: str) -> str:
    """
    Build a fully-qualified URL for a CDN-hosted resource.

    Parameters
    ----------
    cdn_url : str
        Base URL of the CDN (e.g. "https://cdn.example.com").
    resource_identifier : str
        Unique identifier for the resource (e.g. "logo.png").
    resource_kind : str
        Kind of resource, typically a directory name (e.g. "image" or "script").

    Returns
    -------
    str
        The complete URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the CDN URL does not belong to one of the allowed domains.
    """
    # Parse the provided CDN base URL
    parsed_cdn = urllib.parse.urlparse(cdn_url)

    # Basic validation: scheme must be http or https
    if parsed_cdn.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed_cdn.scheme}'. Only http and https are allowed.")

    # Ensure the domain is in the whitelist
    if parsed_cdn.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain '{parsed_cdn.hostname}' is not an allowed CDN domain.")

    # Normalise the path to avoid duplicate slashes
    base_path = parsed_cdn.path.rstrip("/")
    resource_path = f"{resource_kind.strip('/')}/{resource_identifier.lstrip('/')}"

    # Construct the final URL
    full_path = f"{base_path}/{resource_path}"
    built_url = urllib.parse.urlunparse((
        parsed_cdn.scheme,
        parsed_cdn.netloc,
        full_path,
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return built_url