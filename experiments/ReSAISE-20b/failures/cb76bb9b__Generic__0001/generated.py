import urllib.parse

# Predefined set of domains that are considered safe CDNs.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.mywebsite.org",
    "static.cdnprovider.net",
}

def create_resource_url(base_cdn_url: str, res_id: str, res_type: str) -> str:
    """
    Build a full URL for a resource hosted on an external CDN.

    Parameters
    ----------
    base_cdn_url : str
        The root URL of the CDN (e.g., "https://cdn.example.com/").
    res_id : str
        Unique identifier of the resource (e.g., a hash or filename).
    res_type : str
        Type of resource, e.g., "image" or "script".

    Returns
    -------
    str
        The fully-qualified URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain not in :data:`ALLOWED_CDN_DOMAINS`.
    """
    # Sanitize path components to avoid injection attacks.
    safe_res_type = urllib.parse.quote(res_type.strip().lower(), safe="")
    safe_res_id   = urllib.parse.quote(res_id.strip(), safe="")

    # Construct the relative path: "<res_type>s/<res_id>"
    # e.g., "images/abcd1234.png" or "scripts/main.js"
    relative_path = f"{safe_res_type}s/{safe_res_id}"

    # Join the base CDN URL with the relative path.
    full_url = urllib.parse.urljoin(base_cdn_url.rstrip("/") + "/", relative_path)

    # Parse the resulting URL to extract its domain.
    parsed = urllib.parse.urlparse(full_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL constructed: {full_url}")

    # Verify the domain is in the allowed set.
    if parsed.netloc.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Domain '{parsed.netloc}' is not an allowed CDN domain."
        )

    return full_url