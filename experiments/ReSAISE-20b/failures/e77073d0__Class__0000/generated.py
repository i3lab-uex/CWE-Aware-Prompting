import urllib.parse

# Example of allowed CDN domains (add your own as needed)
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.content-cdn.org",
}

def build_cdn_resource_url(cdn_url_base: str, file_id: str, file_type: str) -> str:
    """
    Assemble a fully-qualified CDN URL for a given resource.

    Parameters
    ----------
    cdn_url_base : str
        Base URL of the CDN (e.g. "https://cdn.example.com").
    file_id : str
        Unique identifier for the resource.
    file_type : str
        Type of the resource (e.g. "image", "script").

    Returns
    -------
    str
        The complete URL that can be used to fetch the resource.

    Raises
    ------
    ValueError
        If the resolved domain is not in :data:`ALLOWED_CDN_DOMAINS`.
    """
    # Ensure the base URL is absolute
    parsed_base = urllib.parse.urlparse(cdn_url_base)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid CDN base URL: {cdn_url_base!r}")

    # Validate the domain
    if parsed_base.netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Unauthorized CDN domain: {parsed_base.netloc!r}. "
            f"Allowed domains are: {', '.join(sorted(ALLOWED_CDN_DOMAINS))}"
        )

    # Safely encode the path components
    safe_file_type = urllib.parse.quote(file_type.strip(), safe="")
    safe_file_id = urllib.parse.quote(file_id.strip(), safe="")

    # Construct the path; preserve any existing path in base
    base_path = parsed_base.path.rstrip("/")
    resource_path = f"{base_path}/{safe_file_type}/{safe_file_id}"

    # Rebuild the full URL
    final_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            resource_path,
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    return final_url

# Example usage:
if __name__ == "__main__":
    try:
        url = build_cdn_resource_url(
            "https://cdn.example.com/assets",
            file_id="abc123.jpg",
            file_type="image"
        )
        print(url)  # https://cdn.example.com/assets/image/abc123.jpg
    except ValueError as e:
        print(f"URL construction failed: {e}")