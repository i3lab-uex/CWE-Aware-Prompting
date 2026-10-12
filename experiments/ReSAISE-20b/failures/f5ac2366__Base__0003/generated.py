import urllib.parse

# Example set of allowed CDN domains; replace with real values as needed.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.provider.org",
}


def construct_external_resource_url(cdn_base_url: str, resource_id: str, resource_type: str) -> str:
    """
    Construct a fully-qualified URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_base_url : str
        The base URL of the CDN (e.g. "https://cdn.example.com/").
    resource_id : str
        Identifier of the specific resource to fetch.
    resource_type : str
        Type/category of the resource (e.g. "image", "script").

    Returns
    -------
    str
        A fully-qualified URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resulting URL does not resolve to an allowed CDN domain,
        or if the scheme is not HTTP/HTTPS.
    """
    # Sanitize inputs: strip whitespace and ensure they are strings
    if not all(isinstance(arg, str) for arg in (cdn_base_url, resource_id, resource_type)):
        raise TypeError("All arguments must be strings")

    cdn_base_url = cdn_base_url.strip()
    resource_id = resource_id.strip().lstrip("/")   # remove leading slash to avoid double slashes
    resource_type = resource_type.strip().lstrip("/")

    # Build the path: <resource_type>/<resource_id>
    relative_path = urllib.parse.urljoin(f"{resource_type}/", resource_id)

    # Resolve the full URL
    full_url = urllib.parse.urljoin(cdn_base_url, relative_path)

    # Parse the URL to inspect components
    parsed = urllib.parse.urlparse(full_url)

    # Basic scheme check (must be HTTP or HTTPS)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Resolve any potential hostname rewriting by checking the netloc
    host = parsed.hostname
    if host is None:
        raise ValueError("URL does not contain a valid hostname")

    # Ensure the host is in the whitelist
    if host.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Disallowed CDN domain: {host}")

    # Optionally, enforce that the path does not contain any '..' segments
    if ".." in parsed.path.split("/"):
        raise ValueError("URL path contains unsafe traversal components")

    return full_url