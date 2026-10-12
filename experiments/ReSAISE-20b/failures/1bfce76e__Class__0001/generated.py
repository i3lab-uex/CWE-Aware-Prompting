import urllib.parse

# Example set of safe CDN domains.  In a real project this would be
# defined in configuration or an environment variable.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.safe-cdn.org",
    "images.contentdelivery.net",
}

def generate_external_resource_url(cdn_base: str, res_id: str, res_type: str) -> str:
    """
    Construct a URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_base : str
        Base URL of the CDN (e.g. "https://cdn.example.com").
    res_id : str
        Identifier of the resource (e.g. "logo.png").
    res_type : str
        Resource type to be inserted into the path (e.g. "image").

    Returns
    -------
    str
        Fully resolved URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the target domain is not in :data:`ALLOWED_CDN_DOMAINS` or
        if the constructed URL is invalid.
    """
    # Ensure we have a scheme; default to https if missing
    parsed = urllib.parse.urlparse(cdn_base)
    if not parsed.scheme:
        cdn_base = "https://" + cdn_base
        parsed = urllib.parse.urlparse(cdn_base)

    # Validate domain against the allowed list
    hostname = parsed.hostname
    if not hostname or hostname.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not an allowed CDN domain")

    # Build the path safely, preventing traversal attacks
    safe_res_type = urllib.parse.quote(res_type.strip("/"))
    safe_res_id   = urllib.parse.quote(res_id.strip("/"))

    # Construct the final URL
    path = f"/{safe_res_type}/{safe_res_id}"
    full_url = urllib.parse.urlunparse((
        parsed.scheme,
        parsed.netloc,
        path,
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return full_url