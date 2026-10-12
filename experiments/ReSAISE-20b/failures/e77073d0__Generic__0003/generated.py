import urllib.parse

# Example list of allowed CDN domains – replace with the real values.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.content.net"
}


def build_cdn_resource_url(cdn_url_base: str, file_id: str, file_type: str) -> str:
    """
    Assemble a full CDN URL for a given resource.

    Parameters
    ----------
    cdn_url_base : str
        Base URL of the CDN (e.g. "https://cdn.example.com").
    file_id : str
        Unique identifier for the resource (e.g. "abc12345").
    file_type : str
        Type of resource, e.g. 'image', 'script'.

    Returns
    -------
    str
        Fully qualified, validated CDN URL.

    Raises
    ------
    ValueError
        If the resolved domain is not in :data:`ALLOWED_CDN_DOMAINS`.
    """
    # Normalize the base URL: ensure it has a scheme and no trailing slash
    parsed_base = urllib.parse.urlparse(cdn_url_base)
    if not parsed_base.scheme:
        raise ValueError("Base CDN URL must include a scheme (http or https).")

    # Build the relative path.  Using '/' ensures we don't accidentally
    # duplicate slashes when joining.
    rel_path = urllib.parse.urljoin("/", f"{file_type.rstrip('/')}/{file_id.lstrip('/')}")
    # Construct the full URL
    full_url = urllib.parse.urljoin(parsed_base.geturl(), rel_path)

    # Validate the domain
    parsed_full = urllib.parse.urlparse(full_url)
    if parsed_full.netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Unauthorized CDN domain: {parsed_full.netloc}")

    # Optionally, we could enforce HTTPS only for security
    if parsed_full.scheme != "https":
        # You may choose to warn or raise an error; here we simply log a warning.
        pass  # Replace with logging if desired

    return full_url