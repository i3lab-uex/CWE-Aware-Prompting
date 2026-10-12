import urllib.parse

# Example of allowed CDN domains.
# In a real application this set would be defined elsewhere and imported.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.content.net"
}

def generate_external_resource_url(cdn_base: str, res_id: str, res_type: str) -> str:
    """
    Construct a fully-qualified URL for an external resource served by a CDN.

    Parameters
    ----------
    cdn_base : str
        The base URL of the Content Delivery Network (e.g. "https://cdn.example.com/assets").
    res_id : str
        The identifier of the resource (e.g. "logo.png" or "app.js").
    res_type : str
        The type of the resource (e.g. "image", "script").

    Returns
    -------
    str
        The fully constructed URL pointing to the requested external resource.

    Raises
    ------
    ValueError
        If the resulting URL does not target a domain that belongs to the allowed CDN domains.
    """
    # Parse the base URL to extract its components
    parsed_base = urllib.parse.urlparse(cdn_base)

    # Ensure the scheme is present; default to https if missing
    scheme = parsed_base.scheme or "https"

    # Validate that the domain is allowed
    netloc = parsed_base.netloc
    if not netloc:
        # If the base was a relative path, assume no domain provided
        raise ValueError("The CDN base URL must contain a valid network location (domain).")

    if netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain '{netloc}' is not in the list of allowed CDN domains.")

    # Build the path component: <res_type>/<res_id>
    # Ensure no leading/trailing slashes interfere
    res_path = urllib.parse.urljoin(parsed_base.path + "/", f"{res_type}/{res_id}")

    # Reconstruct the full URL
    full_url = urllib.parse.urlunparse((
        scheme,
        netloc,
        res_path,
        '',  # params
        '',  # query
        ''   # fragment
    ))

    return full_url