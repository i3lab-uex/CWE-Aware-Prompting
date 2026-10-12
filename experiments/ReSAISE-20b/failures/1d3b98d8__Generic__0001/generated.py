import urllib.parse

# Example allowed CDN domains; in a real project this would come from config or env
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.somesite.org",
}

def build_cdn_resource_url(cdn_url: str, resource_identifier: str, resource_kind: str) -> str:
    """
    Construct a fully qualified URL for a CDN-hosted resource.

    Parameters
    ----------
    cdn_url : str
        Base URL of the CDN (e.g., "https://cdn.example.com/").
    resource_identifier : str
        Unique identifier for the requested resource (e.g., "logo.png").
    resource_kind : str
        Category of the resource (e.g., "image", "script").

    Returns
    -------
    str
        The complete, validated URL pointing to the resource.

    Raises
    ------
    ValueError
        If the resulting URL does not belong to an allowed CDN domain.
    """
    # Normalise base URL: ensure it ends with a single slash
    cdn_url = cdn_url.rstrip('/') + '/'

    # Build relative path (e.g., "image/logo.png")
    rel_path = urllib.parse.quote(f"{resource_kind.rstrip('/')}/{resource_identifier.lstrip('/')}", safe='/')

    # Join base and relative path
    full_url = urllib.parse.urljoin(cdn_url, rel_path)

    # Parse the resulting URL to validate domain
    parsed = urllib.parse.urlparse(full_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL constructed: {full_url}")

    # Domain check (case-insensitive)
    domain = parsed.netloc.lower()
    if domain not in {d.lower() for d in ALLOWED_CDN_DOMAINS}:
        raise ValueError(f"URL domain '{domain}' is not in the allowed CDN domains list")

    return full_url