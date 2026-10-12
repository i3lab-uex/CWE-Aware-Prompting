import urllib.parse

# Example list of allowed CDN domains. Adjust as needed.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.contenthost.org"
}

def generate_cdn_content_url(cdn_origin_url: str, content_id: str, content_kind: str) -> str:
    """
    Assemble a validated URL for accessing CDN resources.

    Parameters
    ----------
    cdn_origin_url : str
        Base URL of the CDN (e.g., "https://cdn.example.com").
    content_id : str
        Unique identifier for the resource (e.g., "12345").
    content_kind : str
        Type of resource, e.g., 'image', 'script'.

    Returns
    -------
    str
        Fully-qualified, validated URL pointing to the resource.

    Raises
    ------
    ValueError
        If the resulting URL points to a domain not in ``ALLOWED_CDN_DOMAINS``.
    """
    # Normalize the origin URL
    parsed_origin = urllib.parse.urlparse(cdn_origin_url.rstrip('/'))
    if not parsed_origin.scheme or not parsed_origin.netloc:
        raise ValueError(f"Invalid CDN origin URL: {cdn_origin_url}")

    # Validate domain
    if parsed_origin.netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Unauthorized CDN domain: {parsed_origin.netloc}")

    # Build the path safely
    # Ensure content_kind and content_id are URL-encoded to avoid injection issues.
    encoded_kind = urllib.parse.quote(content_kind.strip('/'))
    encoded_id = urllib.parse.quote(content_id.strip('/'))

    # Construct the new URL
    path = f"/{encoded_kind}/{encoded_id}"
    full_url = urllib.parse.urlunparse((
        parsed_origin.scheme,
        parsed_origin.netloc,
        path,
        '',  # params
        '',  # query
        ''   # fragment
    ))

    return full_url