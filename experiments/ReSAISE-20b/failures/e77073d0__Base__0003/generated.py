import urllib.parse

# A whitelist of CDN domains that are considered safe.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.content.org",
}

def build_cdn_resource_url(cdn_url_base: str, file_id: str, file_type: str) -> str:
    """
    Construct a fully-qualified CDN URL for the requested resource.

    Parameters
    ----------
    cdn_url_base : str
        Base URL of the CDN, e.g. "https://cdn.example.com/"
    file_id : str
        Unique identifier for the resource.
    file_type : str
        Type of the resource, e.g. "image", "script".

    Returns
    -------
    str
        The fully-qualified, validated CDN URL.

    Raises
    ------
    ValueError
        If the constructed URL resolves to a domain that is not in
        :data:`ALLOWED_CDN_DOMAINS` or if the input is malformed.
    """
    # Ensure the base ends with a slash so that urljoin works as expected
    if not cdn_url_base.endswith("/"):
        base = f"{cdn_url_base}/"
    else:
        base = cdn_url_base

    # Build the relative path: e.g. "image/abc123.png"
    # For safety we percent‑encode the file_id
    safe_file_id = urllib.parse.quote(file_id, safe="")
    relative_path = f"{file_type}/{safe_file_id}"

    # Join the base and relative path
    full_url = urllib.parse.urljoin(base, relative_path)

    # Parse the resulting URL to inspect its components
    parsed = urllib.parse.urlparse(full_url)

    # Reject non‑HTTP/HTTPS schemes
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate that the hostname is in the whitelist
    host = parsed.hostname
    if host not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Unauthorized CDN domain: {host}")

    # Return the reconstructed URL (scheme + netloc + path + params + query + fragment)
    return urllib.parse.urlunparse(parsed)

# Example usage
if __name__ == "__main__":
    try:
        url = build_cdn_resource_url(
            "https://cdn.example.com",
            "my_image_123",
            "image"
        )
        print(url)  # https://cdn.example.com/image/my_image_123
    except ValueError as exc:
        print(f"URL construction failed: {exc}")