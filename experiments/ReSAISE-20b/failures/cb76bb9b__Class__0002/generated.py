import urllib.parse
from pathlib import PosixPath

# Example set of allowed CDN domains. In a real system this would be
# populated from configuration or environment variables.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.somedomain.net",
}

def create_resource_url(base_cdn_url: str, res_id: str, res_type: str) -> str:
    """
    Build a fully-qualified URL for a CDN-hosted resource.

    Parameters
    ----------
    base_cdn_url : str
        The base URL of the CDN (e.g. "https://cdn.example.com/").
    res_id : str
        Unique identifier of the resource (e.g. "12345").
    res_type : str
        Type of the resource (e.g. "image", "script").

    Returns
    -------
    str
        A fully-qualified URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the constructed URL resolves to a domain not present in
        :data:`ALLOWED_CDN_DOMAINS` or if any of the inputs are empty.
    """
    # Basic sanity checks
    if not base_cdn_url or not res_id or not res_type:
        raise ValueError("All arguments must be non-empty strings")

    # Parse the base URL to validate and extract its components
    parsed_base = urllib.parse.urlparse(base_cdn_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base CDN URL: {base_cdn_url!r}")

    # Ensure the domain is in the allowed list
    if parsed_base.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Domain '{parsed_base.hostname}' is not an allowed CDN domain"
        )

    # Normalise the path to avoid duplicate slashes
    base_path = PosixPath(parsed_base.path).as_posix().rstrip("/")
    # Construct the resource path: <res_type>/<res_id>
    resource_path = PosixPath(base_path, res_type.strip("/"), res_id.strip("/")).as_posix()

    # Rebuild the URL with the new path
    final_url = urllib.parse.urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        resource_path,
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return final_url


# Example usage (for demonstration purposes only)
if __name__ == "__main__":
    try:
        url = create_resource_url(
            "https://cdn.example.com/assets/",
            "logo.png",
            "image"
        )
        print(url)  # Expected: https://cdn.example.com/assets/image/logo.png
    except ValueError as e:
        print(f"Error: {e}")