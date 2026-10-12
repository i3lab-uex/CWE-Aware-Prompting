import urllib.parse

# Predefined set of domains that are considered safe CDNs.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.content.org",
}

def build_cdn_resource_url(cdn_url: str, resource_identifier: str, resource_kind: str) -> str:
    """
    Construct a fully‑qualified CDN URL for a given resource.

    Parameters
    ----------
    cdn_url : str
        Base CDN URL (e.g. "https://cdn.example.com/").
    resource_identifier : str
        Unique identifier of the resource (e.g. "12345abc").
    resource_kind : str
        Kind of resource, e.g. "image" or "script".

    Returns
    -------
    str
        The fully resolved CDN URL.

    Raises
    ------
    ValueError
        If the resulting URL does not resolve to an allowed CDN domain.
    """
    # Normalise base URL and ensure it ends with a slash for proper joining
    if not cdn_url.endswith("/"):
        cdn_url += "/"

    # Build the relative path and join it with the base URL
    relative_path = urllib.parse.urljoin(f"{resource_kind}/", resource_identifier)
    full_url = urllib.parse.urljoin(cdn_url, relative_path)

    # Parse the resulting URL to extract scheme and netloc
    parsed = urllib.parse.urlparse(full_url)

    # Basic validation: must be HTTP(S) and domain must be in the whitelist
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Normalize domain to lower case for comparison
    netloc = parsed.netloc.lower()

    # Strip any port number for domain matching
    host, _, _ = netloc.partition(":")
    if host not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain '{host}' is not an allowed CDN domain")

    return full_url