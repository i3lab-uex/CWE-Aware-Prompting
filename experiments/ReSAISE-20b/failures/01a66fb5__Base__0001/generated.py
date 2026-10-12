import urllib.parse

# Example allowed CDN domains – replace with real values as needed.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "static.myapp.net",
    "assets.safe-cdn.org"
}

def create_cdn_resource_link(cdn_url_base: str,
                              resource_identifier: str,
                              type_of_resource: str) -> str:
    """
    Construct a full CDN URL for a given resource.

    Parameters
    ----------
    cdn_url_base : str
        Base URL of the CDN (e.g., "https://cdn.example.com/assets/").
    resource_identifier : str
        Identifier of the requested resource (e.g., "logo.png").
    type_of_resource : str
        Type of the resource, e.g. 'image', 'script'.  This is appended
        as a sub‑path segment for organization.

    Returns
    -------
    str
        Fully qualified URL pointing to the external resource.

    Raises
    ------
    ValueError
        If the resolved CDN URL does not point to an allowed domain.
    """
    # Parse the base URL and verify it is HTTP(S) and has an allowed host.
    parsed_base = urllib.parse.urlparse(cdn_url_base)

    if parsed_base.scheme not in ("http", "https"):
        raise ValueError("CDN base URL must use http or https scheme")

    if parsed_base.netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain '{parsed_base.netloc}' is not in the list of allowed CDN domains")

    # Normalise base path to ensure it ends with a slash.
    base_path = parsed_base.path
    if not base_path.endswith("/"):
        base_path += "/"

    # Construct the relative path: type_of_resource/resource_identifier
    relative_parts = [
        urllib.parse.quote(type_of_resource.strip("/")),
        urllib.parse.quote(resource_identifier.strip("/"))
    ]
    relative_path = "/".join(relative_parts)

    # Build the final URL using urljoin to handle any accidental double slashes.
    full_url = urllib.parse.urljoin(
        f"{parsed_base.scheme}://{parsed_base.netloc}{base_path}",
        relative_path
    )

    # Final safety check: ensure the final URL still points to an allowed domain.
    final_parsed = urllib.parse.urlparse(full_url)
    if final_parsed.netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Generated URL points to disallowed domain '{final_parsed.netloc}'")

    return full_url