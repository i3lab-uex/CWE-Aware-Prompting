import urllib.parse

# Example set of allowed CDN domains. In real usage this should be configured elsewhere.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.somesite.org",
}

def construct_external_resource_url(cdn_base_url: str, resource_id: str, resource_type: str) -> str:
    """
    Construct a fully-qualified URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_base_url : str
        The base URL of the CDN (e.g., "https://cdn.example.com/").
    resource_id : str
        The unique identifier of the requested resource.
    resource_type : str
        The type/category of the resource (e.g., "image", "script").

    Returns
    -------
    str
        The fully-qualified URL pointing to the resource.

    Raises
    ------
    ValueError
        If the resolved domain is not in :data:`ALLOWED_CDN_DOMAINS`.
    """
    # Normalise the base URL and ensure it ends with a slash so that urljoin behaves predictably.
    parsed_base = urllib.parse.urlparse(cdn_base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid CDN base URL: {cdn_base_url}")

    # Ensure the domain is allowed
    if parsed_base.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"CDN domain '{parsed_base.hostname}' is not allowed")

    # Construct the relative path for the resource.
    # We canonicalise slashes and strip any leading/trailing whitespace.
    rel_path = f"{resource_type.strip('/')}/{resource_id.strip('/')}"
    # Join the base URL with the relative path
    full_url = urllib.parse.urljoin(parsed_base.geturl() + "/", rel_path)

    # Final safety check: ensure the resolved URL still points to an allowed domain
    final_parsed = urllib.parse.urlparse(full_url)
    if final_parsed.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Resulting URL domain '{final_parsed.hostname}' is not allowed")

    return full_url