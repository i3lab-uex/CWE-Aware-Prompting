import urllib.parse

# Predefined set of CDN domains considered safe
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.content.org",
}

def generate_external_resource_url(cdn_base: str, res_id: str, res_type: str) -> str:
    """
    Construct a fully-qualified URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_base : str
        Base URL of the CDN (e.g., "https://cdn.example.com").
    res_id : str
        Identifier of the resource (e.g., "12345" or "logo.png").
    res_type : str
        Type of resource, used to build a path segment (e.g., "image", "script").

    Returns
    -------
    str
        The fully constructed URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain that is not in `ALLOWED_CDN_DOMAINS`.
    """
    # Normalize the base URL to ensure it contains a scheme
    parsed_base = urllib.parse.urlparse(cdn_base)
    if not parsed_base.scheme:
        raise ValueError(f"cdn_base must include a scheme (http/https): {cdn_base}")

    # Build the relative path. Ensure no leading/trailing slashes to avoid
    # double slashes or unintended paths.
    rel_path = urllib.parse.urljoin(f"{res_type}/", res_id)

    # Resolve the full URL
    full_url = urllib.parse.urljoin(cdn_base.rstrip('/') + "/", rel_path)

    # Validate the domain
    netloc = urllib.parse.urlparse(full_url).netloc.split(':')[0]  # strip port if present
    if netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain '{netloc}' is not an allowed CDN domain.")

    return full_url