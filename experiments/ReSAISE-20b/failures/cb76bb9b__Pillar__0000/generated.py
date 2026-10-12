import urllib.parse

# Set of CDN domains that are considered safe/allowed.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.content.org",
}

def create_resource_url(base_cdn_url: str, res_id: str, res_type: str) -> str:
    """
    Construct a full CDN URL for the requested resource.

    Parameters
    ----------
    base_cdn_url : str
        The root URL of the CDN (e.g. "https://cdn.example.com/").
    res_id : str
        Unique identifier for the resource (e.g. "12345abc").
    res_type : str
        Type of the resource (e.g. "image", "script").

    Returns
    -------
    str
        The fully qualified URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resulting URL does not resolve to an allowed CDN domain.
    """
    # Ensure the base URL ends with a slash for proper joining
    if not base_cdn_url.endswith("/"):
        base_cdn_url += "/"

    # Build the relative path: <res_type>/<res_id>
    rel_path = f"{urllib.parse.quote(res_type)}/{urllib.parse.quote(res_id)}"

    # Join the base URL with the relative path
    full_url = urllib.parse.urljoin(base_cdn_url, rel_path)

    # Parse the resulting URL to validate its domain
    parsed = urllib.parse.urlparse(full_url)

    # Extract the hostname (netloc may include port)
    host = parsed.hostname
    if not host:
        raise ValueError(f"Malformed URL: {full_url}")

    # Reject URLs that do not belong to an allowed CDN domain
    if host.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"URL host '{host}' is not in the list of allowed CDN domains."
        )

    # Optional: ensure that the path does not contain any traversal patterns
    # (although urllib.parse.urljoin already normalizes the path)
    if ".." in parsed.path.split("/"):
        raise ValueError(f"URL path contains prohibited traversal segments: {parsed.path}")

    return full_url