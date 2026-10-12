import urllib.parse

# Allowed CDN domains (example list; adjust as needed)
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "static.myapp.net",
    "assets.contenthost.org",
}

def build_cdn_resource_url(cdn_url_base: str, file_id: str, file_type: str) -> str:
    """
    Construct a fully-qualified CDN URL for the given resource.

    Parameters
    ----------
    cdn_url_base : str
        Base URL of the CDN, e.g. "https://cdn.example.com/"
    file_id : str
        Unique identifier for the resource.
    file_type : str
        Type of resource (e.g. "image", "script").

    Returns
    -------
    str
        Fully-qualified URL that points to the requested resource.

    Raises
    ------
    ValueError
        If the resolved domain is not in :data:`ALLOWED_CDN_DOMAINS`.
    """
    # Parse the base URL to ensure it is well-formed
    parsed_base = urllib.parse.urlparse(cdn_url_base)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Invalid CDN base URL")

    # Ensure the domain is allowed
    if parsed_base.netloc.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Unauthorized CDN domain: {parsed_base.netloc}")

    # Normalise the path to avoid duplicate slashes
    base_path = parsed_base.path.rstrip("/")
    # Build a safe path segment for the file type and ID
    safe_file_type = urllib.parse.quote(file_type.strip(), safe="")
    safe_file_id = urllib.parse.quote(file_id.strip(), safe="")

    # Construct the final path
    resource_path = f"{base_path}/{safe_file_type}/{safe_file_id}"

    # Reassemble the full URL
    final_url = urllib.parse.urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        resource_path,
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return final_url

# Example usage:
if __name__ == "__main__":
    try:
        url = build_cdn_resource_url(
            "https://cdn.example.com/",
            file_id="12345",
            file_type="image"
        )
        print(url)
    except ValueError as e:
        print(f"Error: {e}")