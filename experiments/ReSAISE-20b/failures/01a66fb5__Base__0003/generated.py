import urllib.parse

# Example set of allowed CDN domains.  In a real application this would be
# populated from configuration or environment variables.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.securecdn.org",
    "static.myapp.net",
}

def create_cdn_resource_link(cdn_url_base: str, resource_identifier: str,
                              type_of_resource: str) -> str:
    """
    Construct a fully-qualified CDN URL for the requested resource.

    Parameters
    ----------
    cdn_url_base : str
        Base URL of the CDN (e.g., "https://cdn.example.com/").
    resource_identifier : str
        Identifier of the resource (e.g., "images/logo.png").
    type_of_resource : str
        Type of the resource (e.g., "image", "script").  Currently unused
        but retained for future extensibility.

    Returns
    -------
    str
        The fully qualified URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain that is not in
        ``ALLOWED_CDN_DOMAINS``.
    """
    # Normalize the base URL: ensure it ends with a slash so that urljoin
    # behaves predictably.
    base = cdn_url_base.rstrip('/') + '/'

    # Sanitize the resource identifier: strip leading slashes to avoid
    # accidental absolute paths that could escape the base URL.
    resource = resource_identifier.lstrip('/')

    # Build the full URL
    full_url = urllib.parse.urljoin(base, resource)

    # Parse the resulting URL to inspect its components
    parsed = urllib.parse.urlparse(full_url)

    # Extract the hostname (netloc may contain port, strip it)
    host = parsed.hostname or ""

    # Validate the hostname against the allowed CDN domains
    if host not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Disallowed CDN domain: {host}. "
            f"Allowed domains are: {', '.join(sorted(ALLOWED_CDN_DOMAINS))}"
        )

    # Reconstruct the URL to ensure it doesn't contain any user info or
    # fragments that could be abused.
    safe_url = urllib.parse.urlunparse((
        parsed.scheme,
        host,                    # no port or userinfo
        parsed.path,
        "",                      # params
        parsed.query,            # keep query if present
        ""                       # no fragment
    ))

    return safe_url


# Example usage:
if __name__ == "__main__":
    try:
        url = create_cdn_resource_link(
            "https://cdn.example.com/",
            "/images/logo.png",
            "image"
        )
        print(url)  # https://cdn.example.com/images/logo.png
    except ValueError as e:
        print(f"URL generation failed: {e}")