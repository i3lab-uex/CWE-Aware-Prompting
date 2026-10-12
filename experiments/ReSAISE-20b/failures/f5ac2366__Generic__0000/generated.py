import urllib.parse

# Allowed CDN domains – replace with real values for production.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
}

def construct_external_resource_url(cdn_base_url: str, resource_id: str, resource_type: str) -> str:
    """
    Construct a fully qualified URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_base_url : str
        Base URL of the CDN (e.g., "https://cdn.example.com/assets/").
    resource_id : str
        Identifier of the requested resource (e.g., "12345.png").
    resource_type : str
        Type of the resource (e.g., "image", "script").

    Returns
    -------
    str
        The complete URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resulting URL does not resolve to an allowed CDN domain or
        if the path contains unsafe components such as '..'.
    """
    # Parse the base CDN URL
    parsed_base = urllib.parse.urlparse(cdn_base_url)

    # Ensure the base has a scheme (http/https)
    if not parsed_base.scheme:
        raise ValueError(f"cdn_base_url must include a scheme: {cdn_base_url}")

    # Verify the domain is allowed
    if parsed_base.netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain '{parsed_base.netloc}' is not an allowed CDN domain")

    # Normalize and sanitize the path
    base_path = parsed_base.path.rstrip('/') + '/'  # ensure trailing slash

    # Prevent directory traversal by rejecting any '..' in the path components
    if ".." in urllib.parse.urlparse(resource_id).path.split('/'):
        raise ValueError("resource_id contains unsafe path components")

    # Build the new path
    resource_path = urllib.parse.urljoin(base_path, f"{resource_type}/{urllib.parse.quote(resource_id)}")

    # Reconstruct the final URL
    final_url = urllib.parse.urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        resource_path,
        "",  # params
        "",  # query
        ""   # fragment
    ))

    # Final safety check: ensure the final URL still resolves to an allowed domain
    if urllib.parse.urlparse(final_url).netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError("Resulting URL points to a disallowed domain")

    return final_url