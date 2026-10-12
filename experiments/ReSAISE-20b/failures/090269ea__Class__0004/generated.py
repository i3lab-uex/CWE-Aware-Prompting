import urllib.parse

# A whitelist of CDN domains that are considered safe.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.somesite.org",
    "static.myapp.net",
}

def create_external_resource_link(cdn_url: str, res_id: str, res_type: str) -> str:
    """
    Construct a fully-qualified URL for an external resource.

    Parameters
    ----------
    cdn_url : str
        Base CDN URL, e.g. "https://cdn.example.com/".
    res_id : str
        Unique identifier for the resource (e.g. a hash or UUID).
    res_type : str
        Resource type, e.g. "image" or "script".

    Returns
    -------
    str
        A validated URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain that is not in
        ``ALLOWED_CDN_DOMAINS``.
    """
    # Normalize the base URL to ensure it ends with a slash
    if not cdn_url.endswith("/"):
        cdn_url += "/"

    # Build the path component: <res_type>/<res_id>
    safe_res_type = urllib.parse.quote(res_type.strip(), safe="")
    safe_res_id = urllib.parse.quote(res_id.strip(), safe="")

    # Construct the full URL
    resource_path = f"{safe_res_type}/{safe_res_id}"
    full_url = urllib.parse.urljoin(cdn_url, resource_path)

    # Parse the URL to extract its domain
    parsed = urllib.parse.urlparse(full_url)
    hostname = parsed.hostname

    # Ensure the hostname is in the allowed list
    if not hostname or hostname.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Unauthorized CDN domain: {hostname!r}. "
            "Only the following domains are permitted: "
            f"{', '.join(sorted(ALLOWED_CDN_DOMAINS))}"
        )

    return full_url