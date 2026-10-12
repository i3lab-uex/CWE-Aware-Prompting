import urllib.parse

# Example set of allowed CDN domains; replace with real values as needed.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.somesite.org",
    "static.myapp.net",
}

def generate_external_resource_url(cdn_base: str, res_id: str, res_type: str) -> str:
    """
    Construct a fully qualified URL to an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_base : str
        Base URL of the CDN (e.g., "https://cdn.example.com/").
    res_id : str
        Identifier for the resource (e.g., "12345").
    res_type : str
        Type of the resource, used as part of the path (e.g., "image", "script").

    Returns
    -------
    str
        The complete, validated URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the constructed URL resolves to a domain that is not in
        :data:`ALLOWED_CDN_DOMAINS`.
    """
    # Ensure the base ends with a slash to allow proper path concatenation.
    if not cdn_base.endswith("/"):
        cdn_base += "/"

    # Percent‑encode the resource id and type to avoid injection.
    safe_res_id = urllib.parse.quote(res_id, safe="")
    safe_res_type = urllib.parse.quote(res_type, safe="")

    # Build the relative path: e.g., "image/12345"
    relative_path = f"{safe_res_type}/{safe_res_id}"

    # Construct the full URL.
    full_url = urllib.parse.urljoin(cdn_base, relative_path)

    # Parse the URL to extract its domain (netloc).
    parsed = urllib.parse.urlparse(full_url)

    # Validate the hostname against allowed domains.
    host = parsed.hostname
    if not host or host.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Disallowed CDN domain '{host}'. "
            f"Allowed domains: {', '.join(sorted(ALLOWED_CDN_DOMAINS))}"
        )

    return full_url