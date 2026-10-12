import urllib.parse

# Allowed CDN domains – add the ones you trust here.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.cdnprovider.org",
}

def build_cdn_resource_url(cdn_url_base: str, file_id: str, file_type: str) -> str:
    """
    Assemble a fully qualified CDN URL for a given resource.

    Parameters
    ----------
    cdn_url_base : str
        Base URL of the CDN (e.g., "https://cdn.example.com/").
    file_id : str
        Unique identifier for the resource.
    file_type : str
        Type of the resource (e.g., "image", "script").

    Returns
    -------
    str
        A fully-qualified URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resolved URL points to a domain not in ALLOWED_CDN_DOMAINS.
    """
    # Normalise the base URL to ensure it ends with a slash
    if not cdn_url_base.endswith("/"):
        cdn_url_base += "/"

    # Construct the relative path
    relative_path = urllib.parse.urljoin(f"{file_type}/", file_id)

    # Build the full URL
    full_url = urllib.parse.urljoin(cdn_url_base, relative_path)

    # Parse the resulting URL to inspect its components
    parsed = urllib.parse.urlparse(full_url)

    # Ensure the scheme is HTTP or HTTPS
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate that the hostname is in the whitelist
    if parsed.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Unauthorized CDN domain: {parsed.hostname}. "
            f"Allowed domains are: {', '.join(sorted(ALLOWED_CDN_DOMAINS))}"
        )

    # Return the normalized URL
    return full_url

# Example usage (uncomment to test):
# if __name__ == "__main__":
#     url = build_cdn_resource_url(
#         "https://cdn.example.com/", "12345", "image"
#     )
#     print(url)  # -> https://cdn.example.com/image/12345