import urllib.parse

# Predefined set of safe CDN domains (example)
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.content.org",
}

def generate_external_resource_url(cdn_base: str, res_id: str, res_type: str) -> str:
    """
    Construct a fully qualified URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_base : str
        The base URL of the CDN (e.g., "https://cdn.example.com/").
    res_id : str
        Identifier of the resource (e.g., "12345", "logo.png").
    res_type : str
        Type of the resource (e.g., "image", "script").

    Returns
    -------
    str
        The fully constructed URL.

    Raises
    ------
    ValueError
        If the resulting URL does not resolve to a domain in ALLOWED_CDN_DOMAINS.
    """
    # Normalise the CDN base to ensure it ends with a slash
    cdn_base = cdn_base.rstrip('/') + '/'

    # Build the path part of the URL
    # Example: for image type we might want to prepend a subdirectory
    # This logic can be adjusted as needed; here we simply append the type and id.
    path = urllib.parse.urljoin(f"{res_type}/", res_id)

    # Construct the full URL
    url = urllib.parse.urljoin(cdn_base, path)

    # Parse the resulting URL to inspect its components
    parsed = urllib.parse.urlparse(url)

    # Extract hostname and compare against allowed domains
    if parsed.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Disallowed CDN domain: {parsed.hostname!r}. "
            f"Allowed domains are: {', '.join(sorted(ALLOWED_CDN_DOMAINS))}"
        )

    # Ensure the URL uses HTTPS for security
    if parsed.scheme != "https":
        # Rebuild with https scheme while preserving the path and query
        url = urllib.parse.urlunparse(
            ("https", parsed.hostname, parsed.path, parsed.params, parsed.query, parsed.fragment)
        )

    return url