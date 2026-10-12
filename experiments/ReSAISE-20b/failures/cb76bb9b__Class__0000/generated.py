import urllib.parse

# Set of domains that are considered safe CDNs.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.safe-cdn.org",
    "static.content.net",
}

def create_resource_url(base_cdn_url: str, res_id: str, res_type: str) -> str:
    """
    Build a fully qualified CDN URL for a given resource.

    Parameters
    ----------
    base_cdn_url : str
        Base URL of the CDN (e.g., "https://cdn.example.com").
    res_id : str
        Unique identifier for the resource (e.g., "12345").
    res_type : str
        Type of resource, e.g. 'image', 'script'.

    Returns
    -------
    str
        The complete CDN URL.

    Raises
    ------
    ValueError
        If the constructed URL points to a domain not in ``ALLOWED_CDN_DOMAINS``.
    """
    # Parse the base URL to normalise it and extract components
    parsed = urllib.parse.urlparse(base_cdn_url)

    # Ensure the scheme is present; default to https if missing
    scheme = parsed.scheme or "https"

    # Normalise the network location (domain)
    netloc = parsed.netloc.lower()

    # Validate domain against allowed list
    if not any(netloc == allowed or netloc.endswith("." + allowed) for allowed in ALLOWED_CDN_DOMAINS):
        raise ValueError(f"Domain '{netloc}' is not an allowed CDN domain.")

    # Clean up the path to avoid double slashes or traversal
    base_path = parsed.path.rstrip("/")
    # Ensure resource type and ID are URL‑encoded to avoid injection
    res_type_enc = urllib.parse.quote(res_type.strip("/"))
    res_id_enc = urllib.parse.quote(res_id.strip("/"))

    # Construct the full path
    full_path = f"{base_path}/{res_type_enc}/{res_id_enc}"

    # Rebuild the URL
    final_url = urllib.parse.urlunparse(
        (scheme, netloc, full_path, "", "", "")
    )
    return final_url