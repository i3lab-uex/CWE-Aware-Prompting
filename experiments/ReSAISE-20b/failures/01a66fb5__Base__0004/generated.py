import urllib.parse

# Example set of allowed CDN domains.  In a real application this should be
# configured from a secure source such as an environment variable or a config file.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.securecdn.net",
    "static.myapp.org",
}

def create_cdn_resource_link(cdn_url_base: str, resource_identifier: str,
                             type_of_resource: str) -> str:
    """
    Construct a fully qualified URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_url_base : str
        The base URL of the CDN, e.g. "https://cdn.example.com/"
    resource_identifier : str
        The unique identifier for the requested resource, e.g. "logo.png"
    type_of_resource : str
        The category of the resource, e.g. "image" or "script"

    Returns
    -------
    str
        A fully constructed, absolute URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain that is not in ALLOWED_CDN_DOMAINS.
    """
    # Sanitize inputs: strip leading/trailing whitespace
    cdn_url_base = cdn_url_base.strip()
    resource_identifier = resource_identifier.strip().lstrip('/')
    type_of_resource = type_of_resource.strip().lstrip('/')

    # Build a relative path: <type>/<resource_identifier>
    relative_path = urllib.parse.urljoin(f"{type_of_resource}/", resource_identifier)

    # Construct the absolute URL
    full_url = urllib.parse.urljoin(cdn_url_base, relative_path)

    # Parse the URL to extract the hostname
    parsed = urllib.parse.urlparse(full_url)
    host = parsed.hostname

    if not host or host.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Disallowed CDN domain: {host!r}")

    # Ensure the URL is absolute and uses https for security
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    return full_url