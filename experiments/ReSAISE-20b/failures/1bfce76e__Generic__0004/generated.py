import urllib.parse

# Example set of allowed CDN domains; in real code this would be defined elsewhere
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.content.org",
}

def generate_external_resource_url(cdn_base: str, res_id: str, res_type: str) -> str:
    """
    Construct a secure URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_base : str
        Base URL of the CDN (e.g., "https://cdn.example.com").
    res_id : str
        Identifier of the resource to fetch.
    res_type : str
        Type/category of the resource (e.g., "image", "script").

    Returns
    -------
    str
        Fully-qualified URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the CDN domain is not in `ALLOWED_CDN_DOMAINS` or if inputs are invalid.
    """
    # Parse the base URL
    parsed = urllib.parse.urlparse(cdn_base)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid CDN base URL: {cdn_base!r}")

    # Ensure the domain is allowed
    if parsed.netloc.lower() not in {d.lower() for d in ALLOWED_CDN_DOMAINS}:
        raise ValueError(f"CDN domain '{parsed.netloc}' is not allowed")

    # Sanitize and encode the resource identifier
    safe_res_id = urllib.parse.quote(res_id, safe="")

    # Construct the new path
    # Normalise res_type to avoid leading/trailing slashes
    safe_res_type = res_type.strip("/")
    new_path = f"/{safe_res_type}/{safe_res_id}"

    # Build the final URL (preserve scheme and netloc, discard query/fragment)
    result = urllib.parse.urlunparse((
        parsed.scheme,
        parsed.netloc,
        new_path,
        "",  # params
        "",  # query
        ""   # fragment
    ))
    return result

# Example usage:
if __name__ == "__main__":
    print(generate_external_resource_url(
        "https://cdn.example.com",
        "logo.png",
        "image"
    ))