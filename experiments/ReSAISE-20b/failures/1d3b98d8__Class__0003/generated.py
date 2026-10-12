import urllib.parse

# Example set of domains considered safe for CDN usage.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.content.net",
}

def build_cdn_resource_url(cdn_url: str, resource_identifier: str, resource_kind: str) -> str:
    """
    Construct a fully-qualified CDN URL for the requested resource.

    Parameters
    ----------
    cdn_url : str
        The base URL of the CDN (e.g., "https://cdn.example.com/").
    resource_identifier : str
        A unique identifier for the requested resource.
    resource_kind : str
        The kind of resource (e.g., "image", "script").

    Returns
    -------
    str
        The complete URL pointing to the resource on the CDN.

    Raises
    ------
    ValueError
        If the constructed URL resolves to a domain not present in
        :data:`ALLOWED_CDN_DOMAINS`.  This protects against CWE‑610 by
        ensuring that only known CDN domains are used.
    """
    # Ensure the base URL has a scheme
    if not urllib.parse.urlparse(cdn_url).scheme:
        cdn_url = "https://" + cdn_url

    # Normalise the base URL: strip trailing slashes for consistent joining
    cdn_url = cdn_url.rstrip("/")

    # Build a relative path that includes the kind and identifier.
    # Using urllib.parse.quote to escape any problematic characters.
    rel_path = "/".join([urllib.parse.quote(resource_kind.strip("/")),
                         urllib.parse.quote(resource_identifier.strip("/"))])

    # Construct the full URL
    full_url = urllib.parse.urljoin(cdn_url + "/", rel_path)

    # Validate the resulting domain
    parsed = urllib.parse.urlparse(full_url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Extract the hostname for validation
    host = parsed.hostname
    if not host or host.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Disallowed CDN domain: {host}")

    return full_url