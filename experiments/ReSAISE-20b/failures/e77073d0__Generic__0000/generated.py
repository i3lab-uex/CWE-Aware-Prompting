import urllib.parse

# A set of CDN domains that are considered safe.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.prod.cdn.io",
}


def build_cdn_resource_url(cdn_url_base: str, file_id: str, file_type: str) -> str:
    """
    Construct a fully qualified URL for a resource hosted on an approved CDN.

    Parameters
    ----------
    cdn_url_base : str
        Base URL of the CDN, e.g. "https://cdn.example.com".
    file_id : str
        Unique identifier of the requested resource.
    file_type : str
        Resource type such as 'image', 'script', etc.

    Returns
    -------
    str
        The fully-qualified, validated URL for the requested resource.

    Raises
    ------
    ValueError
        If the resolved domain is not in :data:`ALLOWED_CDN_DOMAINS`.
    """
    # Normalise the base URL (strip trailing slashes)
    cdn_base = cdn_url_base.rstrip("/")

    # Build a relative path: e.g. "images/abcd1234"
    # We add an 's' suffix to the file_type to match common patterns
    # (e.g. "image" -> "images", "script" -> "scripts").
    # This is optional and can be adapted to the CDN's convention.
    relative_path = f"{file_type}s/{urllib.parse.quote(file_id)}"

    # Join base and relative path safely
    full_url = urllib.parse.urljoin(cdn_base + "/", relative_path)

    # Parse the constructed URL to inspect its components
    parsed = urllib.parse.urlparse(full_url)

    # Validate that the hostname is an allowed CDN domain
    if parsed.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Unauthorized CDN domain '{parsed.hostname}'. "
            f"Allowed domains: {', '.join(sorted(ALLOWED_CDN_DOMAINS))}"
        )

    # Return the fully-qualified URL
    return full_url


# Example usage (uncomment to test):
# if __name__ == "__main__":
#     url = build_cdn_resource_url(
#         "https://cdn.example.com", file_id="abc123", file_type="image"
#     )
#     print(url)