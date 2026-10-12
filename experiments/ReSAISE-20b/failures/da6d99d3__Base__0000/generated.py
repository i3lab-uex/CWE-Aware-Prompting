import urllib.parse

# Example set of allowed CDN domains. In a real application, populate this with the actual safe domains.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.provider.org",
}

def build_external_resource_link(cdn_url: str, resource_key: str, res_category: str) -> str:
    """
    Construct a fully-qualified URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_url : str
        The base URL of the CDN (e.g. "https://cdn.example.com").
    resource_key : str
        Identifier of the specific resource (e.g. "logo.png").
    res_category : str
        Category/type of the resource (e.g. "image", "script").

    Returns
    -------
    str
        The fully constructed URL pointing to the requested external resource.

    Raises
    ------
    ValueError
        If the resulting URL does not resolve to an allowed CDN domain.
    """
    # Parse the base CDN URL
    parsed_base = urllib.parse.urlparse(cdn_url)

    # Ensure we have a scheme; default to https if missing
    scheme = parsed_base.scheme or "https"
    netloc = parsed_base.netloc

    if not netloc:
        # If the cdn_url was just a hostname without scheme
        netloc = parsed_base.path
        path_prefix = ""
    else:
        path_prefix = parsed_base.path

    # Normalize the base path
    base_path = urllib.parse.urljoin(path_prefix + "/", "")

    # Build the relative path for the resource
    relative_path = urllib.parse.urljoin(f"{res_category}/", resource_key)

    # Construct the full URL
    full_url = urllib.parse.urlunparse(
        (scheme, netloc, urllib.parse.urljoin(base_path, relative_path), "", "", "")
    )

    # Validate that the domain is in the allowed set
    if netloc.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Domain '{netloc}' is not in the list of allowed CDN domains."
        )

    return full_url