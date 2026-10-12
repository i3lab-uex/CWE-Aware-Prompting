import urllib.parse

# Example set of allowed CDN domains; replace with your actual whitelist.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.contentprovider.org"
}

def create_cdn_resource_link(cdn_url_base: str, resource_identifier: str, type_of_resource: str) -> str:
    """
    Construct a fully qualified CDN URL for the requested resource.

    Parameters
    ----------
    cdn_url_base : str
        Base URL of the CDN (e.g., "https://cdn.example.com/").
    resource_identifier : str
        Identifier of the specific resource (e.g., "images/logo.png").
    type_of_resource : str
        Type of the resource (e.g., "image", "script").

    Returns
    -------
    str
        The complete URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the constructed URL resolves to a domain not in ``ALLOWED_CDN_DOMAINS``.
    """
    # Normalize base URL: ensure it ends with a slash
    if not cdn_url_base.endswith('/'):
        cdn_url_base += '/'

    # Build the relative path
    relative_path = urllib.parse.urljoin('', resource_identifier.lstrip('/'))

    # Combine base and relative path
    full_url = urllib.parse.urljoin(cdn_url_base, relative_path)

    # Parse the resulting URL to inspect its components
    parsed = urllib.parse.urlparse(full_url)

    # Ensure the scheme is HTTP or HTTPS
    if parsed.scheme not in ('http', 'https'):
        raise ValueError(f"Unsupported URL scheme '{parsed.scheme}'. Only HTTP/HTTPS are allowed.")

    # Validate the host against the whitelist
    host = parsed.hostname or ''
    if host not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain '{host}' is not in the list of allowed CDN domains.")

    # Optionally, you can add type_of_resource checks or transformations here.
    # For now we simply return the fully constructed URL.

    return full_url